"""Create the Gradio demo Space (Sayuj63/Vapt-Env-Demo) and push gradio_ui/* to it.

Run:
    HF_TOKEN=<write> uv run python scripts/deploy_gradio_space.py
"""
import os
from pathlib import Path

REPO_ID = "Sayuj63/Vapt-Env-Demo"
GRADIO_DIR = Path(__file__).resolve().parent.parent / "gradio_ui"


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("HF_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    break
    if not token:
        raise SystemExit("HF_TOKEN not set in env or .env")

    from huggingface_hub import HfApi

    api = HfApi(token=token)

    # Create the Space (idempotent)
    print(f"creating space {REPO_ID} ...")
    api.create_repo(
        repo_id=REPO_ID,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True,
    )

    # Upload gradio_ui/* contents
    print(f"uploading {GRADIO_DIR} -> {REPO_ID} ...")
    api.upload_folder(
        folder_path=str(GRADIO_DIR),
        repo_id=REPO_ID,
        repo_type="space",
        commit_message="Initial deploy: VAPT-Env Live Operations Center (Gradio)",
    )

    url = f"https://huggingface.co/spaces/{REPO_ID}"
    print(f"OK pushed -> {url}")
    print("Space will build in ~2 min. Watch the Logs tab.")


if __name__ == "__main__":
    main()
