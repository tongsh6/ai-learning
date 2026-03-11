#!/usr/bin/env python3
"""跨平台开发脚本。"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]



def run(command: list[str]) -> None:
    env = os.environ.copy()
    python_path = env.get("PYTHONPATH")
    project_root = str(PROJECT_ROOT)
    env["PYTHONPATH"] = (
        project_root if not python_path else os.pathsep.join([project_root, python_path])
    )
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    subprocess.run(command, cwd=PROJECT_ROOT, check=True, env=env)



def in_virtualenv() -> bool:
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)



def install() -> None:
    pip_install = [sys.executable, "-m", "pip", "install"]
    if in_virtualenv():
        run(pip_install + ["--upgrade", "pip"])
        run(pip_install + ["-e", ".[dev]"])
        return

    run(pip_install + ["--user", "-e", ".[dev]"])



def init_env() -> None:
    source = PROJECT_ROOT / ".env.example"
    target = PROJECT_ROOT / ".env"
    if target.exists():
        print(".env 已存在，跳过初始化。")
        return
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    print("已创建 .env。")



def lint() -> None:
    run([sys.executable, "-m", "ruff", "check", "."])



def test() -> None:
    run([sys.executable, "-m", "pytest"])



def check() -> None:
    lint()
    test()



def week1() -> None:
    run([sys.executable, str(PROJECT_ROOT / "week1-embedding" / "01_embedding_basics.py")])



def week2() -> None:
    run([sys.executable, str(PROJECT_ROOT / "week2-chunking" / "02_chunking_and_models.py")])


TASKS = {
    "install": install,
    "init-env": init_env,
    "lint": lint,
    "test": test,
    "check": check,
    "week1": week1,
    "week2": week2,
}



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Learning 项目开发脚本")
    parser.add_argument("task", choices=TASKS.keys(), nargs="?", default="check")
    return parser.parse_args()



def main() -> int:
    args = parse_args()
    TASKS[args.task]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
