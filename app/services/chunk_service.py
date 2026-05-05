from pymongo import InsertOne

from app.schemas import DataChunk
from bson import ObjectId

class ChunkService:

    def __init__(self, db):
        self.collection = db["chunks"]

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_none=True))
        chunk._id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str):
        chunk = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if not chunk:
            return None
        return DataChunk(**chunk)
    

    async def insert_many_chunks(self, chunks: list[DataChunk], batch_size: int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [InsertOne(chunk.model_dump(by_alias=True, exclude_none=True)) for chunk in batch]
            await self.collection.bulk_write(operations)
        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count