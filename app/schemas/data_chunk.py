from pydantic import BaseModel, Field 
from typing import Optional
from bson import ObjectId

class DataChunk(BaseModel):

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    chunk_text: str = Field(..., min_length=1, description="Text content of the data chunk")
    chunk_metadata: Optional[dict] = Field(None, description="Metadata associated with the data chunk")
    chunk_order: int = Field(..., gt=0, description="Order of the chunk within the project")
    chunk_project_id: ObjectId = Field(..., description="Reference to the project this chunk belongs to")
    

    
    class Config:
        arbitrary_types_allowed = True