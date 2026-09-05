from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT_FILES = ("README.md", "PROGRESS.md", "requirements-render.txt")
ROOT_DIRS = ("charts", "docs", "scripts", "site")


def copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".playwright-cli"),
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build a complete dated release bundle.")
    parser.add_argument("--repository-root", type=Path, default=root)
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--benchmark", choices=("general", "terminal-bench"), default="general")
    parser.add_argument("--release-root", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.repository_root.resolve()
    manifest = json.loads(
        (root / "site" / "data" / "snapshots.json").read_text(encoding="utf-8")
    )
    terminal_manifest = json.loads((root / "site/data/terminal-bench.json").read_text(encoding="utf-8")) if args.benchmark == "terminal-bench" else None
    terminal_current = next(item for item in terminal_manifest["versions"] if item["id"] == terminal_manifest["current_version"]) if terminal_manifest else None
    snapshot = args.snapshot or (terminal_current["current_snapshot"] if terminal_current else manifest["current"])
    prefix = "terminal-bench" if terminal_manifest else "llm-efficiency-cost-charts"
    release_root = (
        args.release_root.resolve()
        if args.release_root
        else root / "dist" / (f"release-terminal-bench-{snapshot}" if terminal_manifest else f"release-{snapshot}")
    )
    bundle_name = f"{prefix}-{snapshot}"
    staging = release_root / bundle_name
    archive = release_root / f"{bundle_name}-full.zip"
    checksum = release_root / "SHA256SUMS.txt"
    if release_root.exists():
        raise FileExistsError(f"Release output already exists: {release_root}")

    staging.mkdir(parents=True)
    for name in ROOT_FILES:
        shutil.copy2(root / name, staging / name)
    for name in ROOT_DIRS:
        copy_tree(root / name, staging / name)

    snapshot_ids = [entry["id"] for entry in manifest["snapshots"]]
    if not terminal_manifest and snapshot not in snapshot_ids:
        raise AssertionError(f"Release snapshot is absent from manifest: {snapshot}")
    for snapshot_id in snapshot_ids:
        copy_tree(root / "data" / snapshot_id, staging / "data" / snapshot_id)
        copy_tree(root / "rankings" / snapshot_id, staging / "rankings" / snapshot_id)
    copy_tree(
        root / "data" / "coding-agents",
        staging / "data" / "coding-agents",
    )
    if terminal_manifest:
        copy_tree(root / "data/terminal-bench", staging / "data/terminal-bench")
        copy_tree(root / "rankings/terminal-bench", staging / "rankings/terminal-bench")
    price_update = root / "data" / f"api_price_updates_{snapshot}.csv"
    if price_update.exists():
        shutil.copy2(price_update, staging / "data" / price_update.name)

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for path in sorted(staging.rglob("*")):
            if path.is_file():
                handle.write(path, path.relative_to(release_root), compress_type=zipfile.ZIP_STORED if path.suffix.lower() == ".png" else zipfile.ZIP_DEFLATED, compresslevel=6)

    digest = sha256(archive)
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    with zipfile.ZipFile(archive) as handle:
        names = handle.namelist()
        if len(names) < 50:
            raise AssertionError(f"Release archive unexpectedly sparse: {len(names)} files")
        if terminal_manifest:
            for version in terminal_manifest["versions"]:
                for item in version["snapshots"]:
                    required = f"{bundle_name}/data/terminal-bench/{version['id']}/{item['id']}/source.json"
                    if required not in names:
                        raise AssertionError(f"Release archive missing {required}")
        elif f"{bundle_name}/data/{snapshot}/model_efficiency.csv" not in names:
            raise AssertionError("Release archive is missing the dated model data")
        if f"{bundle_name}/site/data/rankings.json" not in names:
            raise AssertionError("Release archive is missing the interactive ranking payload")
        if not any(
            name.startswith(f"{bundle_name}/data/coding-agents/")
            and name.endswith("/coding_agent_results.csv")
            for name in names
        ):
            raise AssertionError("Release archive is missing coding-agent data")
        for snapshot_id in snapshot_ids:
            if f"{bundle_name}/data/{snapshot_id}/model_efficiency.csv" not in names:
                raise AssertionError(f"Release archive is missing snapshot {snapshot_id}")
    print(
        f"release={release_root}; files={len(names)}; "
        f"archive_bytes={archive.stat().st_size}; sha256={digest}"
    )


if __name__ == "__main__":
    main()
