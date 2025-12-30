#!/usr/bin/env python3
"""Render Meza's Extensions.php.j2 locally.

This is a fast feedback tool for iterating on the Jinja template
[src/roles/mediawiki/templates/Extensions.php.j2](src/roles/mediawiki/templates/Extensions.php.j2)
without needing to run an Ansible deploy.

It loads real core data from:
- config/MezaCoreExtensions.yml
- config/MezaCoreSkins.yml

Local extensions/skins are optional; if you omit them the script uses empty lists
so you can validate formatting and structure.

Requirements:
    pip install jinja2 pyyaml
    From my .venv during development I used
    pip3.6 install 'jinja2<3' 'markupsafe<2.1' pyyaml

Usage:
    ./src/scripts/render_extensions_php.py \
      --out logs/Extensions.php.simulated.php

    # Include local config files (optional)
    ./src/scripts/render_extensions_php.py \
      --local-extensions /opt/conf-meza/public/MezaLocalExtensions.yml \
      --local-skins /opt/conf-meza/public/MezaLocalSkins.yml \
      --out /tmp/Extensions.php

Notes:
    - This script does not attempt to resolve nested Jinja variables that might
      appear inside YAML values (e.g. "{{ mediawiki_default_branch }}"). The
      Extensions.php template typically does not use those fields.
"""

import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

import jinja2
import yaml


def load_yaml(path: Path) -> dict:
    """Load a YAML file and return its parsed representation."""
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise TypeError(f"Expected YAML mapping at {path}, got {type(data).__name__}")
    return data


def detect_repo_root() -> Path:
    """Detect the meza repo root by walking up from this file."""
    start = Path(__file__).resolve()
    for candidate in [start.parent] + list(start.parents):
        if (candidate / "config").is_dir() and (candidate / "src").is_dir():
            return candidate
    # Fallback: this file is typically at <repo>/src/scripts/<file>
    return start.parents[3]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Extensions.php.j2 locally")
    parser.add_argument(
        "--repo",
        default=str(detect_repo_root()),
        help="Path to the meza repo root (default: auto-detected)",
    )
    parser.add_argument(
        "--template",
        default="src/roles/mediawiki/templates/Extensions.php.j2",
        help="Path to Extensions.php.j2 relative to --repo",
    )
    parser.add_argument(
        "--core-extensions",
        default="config/MezaCoreExtensions.yml",
        help="Path to MezaCoreExtensions.yml relative to --repo",
    )
    parser.add_argument(
        "--core-skins",
        default="config/MezaCoreSkins.yml",
        help="Path to MezaCoreSkins.yml relative to --repo",
    )
    parser.add_argument(
        "--local-extensions",
        default=None,
        help="Optional path to MezaLocalExtensions.yml (absolute or relative to --repo)",
    )
    parser.add_argument(
        "--local-skins",
        default=None,
        help="Optional path to MezaLocalSkins.yml (absolute or relative to --repo)",
    )
    parser.add_argument(
        "--out",
        default="logs/Extensions.php.simulated.php",
        help="Output path (absolute or relative to --repo)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write rendered output to stdout instead of a file",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on undefined Jinja variables (default: strict)",
    )
    return parser.parse_args()


def resolve_path(repo_root: Path, maybe_path: Optional[str]) -> Optional[Path]:
    if maybe_path is None:
        return None
    candidate = Path(maybe_path)
    if candidate.is_absolute():
        return candidate
    return repo_root / candidate


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).resolve()

    template_path = resolve_path(repo_root, args.template)
    core_extensions_path = resolve_path(repo_root, args.core_extensions)
    core_skins_path = resolve_path(repo_root, args.core_skins)
    local_extensions_path = resolve_path(repo_root, args.local_extensions)
    local_skins_path = resolve_path(repo_root, args.local_skins)
    out_path = resolve_path(repo_root, args.out)

    if template_path is None or out_path is None:
        raise RuntimeError("Internal error resolving required paths")

    meza_core_extensions = load_yaml(core_extensions_path)
    meza_core_skins = load_yaml(core_skins_path)

    if local_extensions_path is None:
        meza_local_extensions = {"list": []}
    else:
        meza_local_extensions = load_yaml(local_extensions_path)

    if local_skins_path is None:
        meza_local_skins = {"list": []}
    else:
        meza_local_skins = load_yaml(local_skins_path)

    undefined_cls = jinja2.StrictUndefined if args.strict else jinja2.Undefined
    env = jinja2.Environment(
        undefined=undefined_cls,
        autoescape=False,
        keep_trailing_newline=True,
    )

    raw_template = template_path.read_text(encoding="utf-8")
    template = env.from_string(raw_template)

    context = {
        "ansible_managed": "SIMULATED OUTPUT (not generated by Ansible)",
        "template_run_date": datetime.now().isoformat(timespec="seconds"),
        "meza_core_extensions": meza_core_extensions,
        "meza_core_skins": meza_core_skins,
        "meza_local_extensions": meza_local_extensions,
        "meza_local_skins": meza_local_skins,
        # Some templates assume this exists for wiki gating; leaving as a sensible
        # default here is helpful even when local lists are empty.
        "wikiId": "demo",
    }

    rendered = template.render(**context)

    if args.stdout:
        print(rendered, end="")
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
