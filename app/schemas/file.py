from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId


class File(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    file_project_id: ObjectId
    file_name: str = Field(..., min_length=1, description="Name of the file")
    file_type: str = Field(..., min_length=1)
    file_size: int = Field(gt=0, default=None, description="Size of the file in bytes")
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("file_project_id", 1)],
                "name": "file_project_id_index",
                "unique": False,
            },
            {
                "key": [("file_name", 1), ("file_project_id", 1)],
                "name": "file_project_id_file_name_index",
                "unique": True,
            },
        ]
