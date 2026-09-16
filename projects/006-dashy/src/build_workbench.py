"""Build our configured workbench for GitHub Pages from pinned Dashy sources."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import zipfile
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
REVISION = '6c56436d5f044d3c53371891c9d9a8c8df8c4606'
SOURCE = ROOT / '.cache' / 'source' / ('dashy-' + REVISION)
OUT = ROOT / '.cache' / 'public-workbench'
BASE = '/0914_codex_project/006-dashy/workbench/'


def main():
    if not (SOURCE / 'package.json').exists():
        archive = ROOT / '.cache' / 'dashy.zip'
        archive.parent.mkdir(parents=True, exist_ok=True)
        if not archive.exists():
            urlretrieve(f'https://codeload.github.com/Lissy93/dashy/zip/{REVISION}', archive)
        with zipfile.ZipFile(archive) as bundle:
            target = SOURCE.parent.resolve()
            for entry in bundle.namelist():
                if not (target / entry).resolve().is_relative_to(target):
                    raise ValueError('Archive entry outside source directory')
            bundle.extractall(target)
    local_node = ROOT / '.cache' / 'runtime' / 'node.exe'
    node = str(local_node) if local_node.exists() else shutil.which('node')
    if not node:
        raise RuntimeError('Node.js 24 is required')
    env = dict(os.environ)
    env['PATH'] = str(Path(node).parent) + os.pathsep + env['PATH']
    env['VITE_APP_ROUTING_MODE'] = 'hash'
    env['VITE_APP_CONFIG_PATH'] = BASE + 'conf.yml'
    if not (SOURCE / 'node_modules' / 'vite').exists():
        local_yarn = ROOT / '.cache' / 'tools' / 'node_modules' / 'yarn' / 'bin' / 'yarn.js'
        yarn = [node, str(local_yarn)] if local_yarn.exists() else [shutil.which('yarn') or 'yarn']
        subprocess.run(yarn + ['install', '--frozen-lockfile', '--non-interactive', '--network-timeout', '120000'], cwd=SOURCE, env=env, check=True)
    # Keep the local backend build untouched. Adapt only this public build.
    config = SOURCE / '.codex-pages.config.mjs'
    config.write_text('''import upstream from './vite.config.mjs';
export default {
  ...upstream,
  base: %s,
  plugins: [
    ...upstream.plugins.flat(Infinity).filter(p => !p.name.startsWith('vite-plugin-pwa') && p.name !== 'copy-user-data-config'),
    { name: 'public-workbench-adapter', enforce: 'pre', transform(code, id) {
      // This static demo neither registers nor unregisters workers on the shared origin.
      if (id.replaceAll('\\\\', '/').endsWith('/src/utils/InitServiceWorker.js')) return 'export default async () => {};';
      // Local edits belong to this demo; do not collide with other apps on this origin.
      if (id.replaceAll('\\\\', '/').endsWith('/src/utils/config/defaults.js')) {
        return code.replace(/localStorageKeys: \\{([\\s\\S]*?)\\n  \\}/, (_, keys) => 'localStorageKeys: {' + keys.replace(/: '([^']+)'/g, ": 'dashy006:$1'") + '\\n  }');
      }
    } },
  ],
  build: { ...upstream.build, outDir: %s, emptyOutDir: true },
};
''' % (json.dumps(BASE), json.dumps(str(OUT).replace('\\', '/'))), encoding='utf-8')
    subprocess.run([node, 'node_modules/vite/bin/vite.js', 'build', '--config', str(config)], cwd=SOURCE, env=env, check=True)
    fonts = OUT / 'theme-fonts.css'
    fonts.write_text(fonts.read_text(encoding='utf-8').replace("url('/", "url('" + BASE), encoding='utf-8')
    for p in (ROOT / 'web' / 'workbench').iterdir():
        if p.is_file():
            shutil.copy2(p, OUT / p.name)
    shutil.copy2(ROOT / 'notes' / 'UPSTREAM-LICENSE.txt', OUT / 'UPSTREAM-LICENSE.txt')
    if '127.0.0.1' in (OUT / 'conf.yml').read_text(encoding='utf-8'):
        raise ValueError('Online configuration must not reference localhost')
    print(f'Public workbench ready: {OUT}')


if __name__ == '__main__':
    main()
