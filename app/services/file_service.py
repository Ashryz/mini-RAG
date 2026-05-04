from fastapi import UploadFile
from app.core.config import get_settings
from pathlib import Path
import re
from app.utils.file_utils import generate_random_string

BASE_DIR = Path(__file__).resolve().parent.parent

class FileService:

    def __init__(self):
        self.app_settings = get_settings()
        self.files_dir = BASE_DIR / "assets" / "files"
        self.files_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return{
                "success": False,
                "message": f"File type {file.content_type} is not allowed."
            }
        if file.size > self.app_settings.FILE_MAX_SIZE:
            return {
                "success": False,
                "message": f"File size {file.size} is too large."
            }
        return {
            "success": True,
            "message": "File is valid."
        }
    
    def get_project_path(self, project_id: str):
        project_path = self.files_dir / project_id
        project_path.mkdir(parents=True, exist_ok=True)
        return project_path        

    def clean_filename(self, filename: str) -> str:
        filename = re.sub(r'[^\w\.-]', '_', filename.strip())
        filename = re.sub(r'_{2,}', '_', filename)
        return filename

    def get_file_extention(self, filename: str) -> str:
        ext = Path(filename).suffix.lstrip(".")
        return ext

    def generate_unique_filename(self,filename: str , project_id: str) -> str:
        random_key = generate_random_string()
        clean_name = self.clean_filename(filename)
        project_path = self.get_project_path(project_id=project_id)
        unique_filename = f"{random_key}_{clean_name}"

        while (project_path / unique_filename).exists():
            random_key = generate_random_string()
            unique_filename = f"{random_key}_{clean_name}"
            
        return unique_filename
    