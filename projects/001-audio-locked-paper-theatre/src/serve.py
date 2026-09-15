"""Local-only preview server with byte ranges for reliable video chapter seeking."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import re

ROOT=Path(__file__).resolve().parents[1]

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Accept-Ranges","bytes")
        super().end_headers()

    def send_head(self):
        self.remaining=None
        value=self.headers.get("Range")
        path=Path(self.translate_path(self.path))
        if not value or not path.is_file():return super().send_head()
        match=re.fullmatch(r"bytes=(\d*)-(\d*)",value)
        size=path.stat().st_size
        if not match or not any(match.groups()):
            self.send_error(416,"Invalid range")
            return None
        left,right=match.groups()
        start=int(left) if left else max(0,size-int(right))
        end=min(size-1,int(right)) if left and right else size-1
        if start>end or start>=size:
            self.send_response(416)
            self.send_header("Content-Range",f"bytes */{size}")
            self.send_header("Content-Length","0")
            self.end_headers()
            return None
        handle=path.open("rb")
        handle.seek(start)
        self.remaining=end-start+1
        self.send_response(206)
        self.send_header("Content-Type",self.guess_type(str(path)))
        self.send_header("Content-Length",str(self.remaining))
        self.send_header("Content-Range",f"bytes {start}-{end}/{size}")
        self.end_headers()
        return handle

    def copyfile(self,source,outputfile):
        try:
            if self.remaining is None:return super().copyfile(source,outputfile)
            while self.remaining>0:
                chunk=source.read(min(self.remaining,65536))
                if not chunk:break
                outputfile.write(chunk)
                self.remaining-=len(chunk)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):
            pass

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--port",type=int,default=8766)
    args=parser.parse_args()
    print(f"Preview: http://127.0.0.1:{args.port}/web/index.html",flush=True)
    ThreadingHTTPServer(("127.0.0.1",args.port),partial(Handler,directory=str(ROOT))).serve_forever()
