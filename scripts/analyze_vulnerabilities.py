import argparse
import json
import logging
import subprocess
from pathlib import Path
import shutil

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Analyze SBOMs with Grype.")
    parser.add_argument("--sboms-path", default="data/results", help="Path to SBOMs.")
    parser.add_argument(
        "--output-path",
        default="data/vulnerabilities",
        help="Path to save vulnerability reports.",
    )
    args = parser.parse_args()

    sboms_dir = Path(args.sboms_path)
    output_dir = Path(args.output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    grype_bin = shutil.which("grype")
    if not grype_bin:
        LOGGER.error("Grype is not installed or not in PATH.")
        return 1

    sboms = list(sboms_dir.glob("*.json"))
    LOGGER.info(f"Found {len(sboms)} SBOMs to analyze.")

    for i, sbom_path in enumerate(sboms, 1):
        LOGGER.info(f"[{i}/{len(sboms)}] Analyzing {sbom_path.name}")
        output_file = output_dir / sbom_path.name

        # Run Grype with sbom input and json output
        cmd = [grype_bin, f"sbom:{sbom_path}", "-o", "json"]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            LOGGER.error(f"Failed to analyze {sbom_path.name}: {result.stderr}")
            continue

        with open(output_file, "w") as f:
            f.write(result.stdout)

    LOGGER.info("Analysis complete.")
    return 0


if __name__ == "__main__":
    exit(main())
