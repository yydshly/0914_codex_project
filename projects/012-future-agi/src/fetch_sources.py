"""Download selected public upstream files at the recorded commit for local study."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    "README.md", "LICENSE", "LICENSE-EE", "NOTICE", "INSTALLATION.md",
    "docker-compose.yml", "Dockerfile.oss", "fi-collector/README.md",
    "agentcc-gateway/README.md", "agentcc-gateway/internal/routing/router.go",
    "agentcc-gateway/internal/guardrails/engine.go",
    "agentcc-gateway/internal/guardrails/injection/injection.go",
    "futureagi/tfc/ee_loader.py",
    "futureagi/model_hub/services/optimization_service.py",
    "futureagi/model_hub/tasks/optimisation_runner.py",
    "futureagi/agentic_eval/core_evals/fi_evals/function/function_evaluator.py",
    "futureagi/agentic_eval/core_evals/fi_evals/llm/custom_prompt_evaluator/evaluator.py",
    "futureagi/simulate/services/chat_engine.py",
    "futureagi/simulate/tasks/chat_sim.py",
    "futureagi/tfc/deployment_telemetry/config.py",
    "futureagi/model_hub/views/develop_optimiser.py",
    "futureagi/model_hub/tasks/prompt_template_optimizer.py",
    "futureagi/simulate/services/prompt_based_agent_adapter.py",
    ".dockerignore",
]


def fetch(path):
    version = json.loads((ROOT / "notes/upstream-version.json").read_text(encoding="utf-8-sig"))
    sha = version["commit"]
    url = f"https://raw.githubusercontent.com/future-agi/future-agi/{sha}/{path}"
    request = Request(url, headers={"User-Agent": "FutureAGI-research"})
    with urlopen(request, timeout=45) as response:
        content = response.read()
    destination = ROOT / ".cache/upstream" / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return {"path": path, "url": f"https://github.com/future-agi/future-agi/blob/{sha}/{path}",
            "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(fetch, PATHS))
    (ROOT / "notes/source-manifest.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Fetched {len(records)} source files at the pinned commit; no upstream code executed.")
