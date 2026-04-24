import json
import subprocess
import sys
from pathlib import Path

def add_submodules():
    """
    Reads a JSON file with repository information and adds them as Git submodules.
    """
    repo_root = Path(__file__).resolve().parents[1]
    repos_file = repo_root / "data" / "repos.json"

    if not repos_file.exists():
        print(f"Error: Repositories file not found at {repos_file}")
        sys.exit(1)

    with open(repos_file, 'r') as f:
        data = json.load(f)

    for repo in data.get("repositories", []):
        url = repo.get("url")
        path = repo.get("path")

        if not url or not path:
            print(f"Skipping invalid repository entry: {repo}")
            continue

        submodule_path = repo_root / path
        
        gitmodules_path = repo_root / ".gitmodules"
        already_added = False
        if gitmodules_path.exists():
            with open(gitmodules_path, 'r') as gm_file:
                if path in gm_file.read():
                    print(f"Submodule for path '{path}' already exists. Skipping.")
                    already_added = True

        if not already_added:
            print(f"Adding submodule: {url} to {path}")
            try:
                subprocess.run(
                    ["git", "submodule", "add", "--force", url, path],
                    check=True,
                    cwd=repo_root
                )
            except subprocess.CalledProcessError as e:
                print(f"Failed to add submodule {url}. Error: {e}")
            except FileNotFoundError:
                print("Error: 'git' command not found. Is Git installed and in your PATH?")
                sys.exit(1)

if __name__ == "__main__":
    add_submodules()
