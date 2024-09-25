from pathlib import Path

def create_folder(user_id: str, base_dir: Path) -> Path:
    user_folder = base_dir / user_id
    user_folder.mkdir(parents=True, exist_ok=True)
    return user_folder