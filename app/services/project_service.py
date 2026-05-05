import math

from app.schemas import Project


class ProjectService:

    def __init__(self, db):
        self.collection = db["projects"]

    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_none=True))
        project._id = result.inserted_id
        return project

    async def get_project_or_create(self, project_id: str):
        project = await self.collection.find_one({"project_id": project_id})
        if not project:
            new_project = Project(project_id=project_id)
            return await self.create_project(new_project)
        return Project(**project)
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        total_projects = await self.collection.count_documents({})
        total_pages = math.ceil(total_projects / page_size)
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = [Project(**project) async for project in cursor]
        return projects, total_pages