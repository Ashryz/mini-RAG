import aiofiles
from fastapi import APIRouter , Depends, UploadFile , status, Request
from fastapi.responses import JSONResponse
from app.core.config import Settings, get_settings
from app.schemas import  ProcessRequest
from app.schemas import DataChunk
from app.services import FileService , ProcessService , ProjectService, ChunkService
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/api/v1/data",
    tags=["data"],
)

@router.post("/upload/{project_id}")
async def upload_file(request: Request, project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    is_valid = FileService().validate_file(file=file)

    project_service = await ProjectService.initialize(db=request.app.database)

    project = await project_service.get_project_or_create(project_id=project_id)

    if not is_valid['success']:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": is_valid["message"]
            }
        )
    
    project_path = FileService().get_project_path(project_id=project_id)
    new_filename = FileService().generate_unique_filename(filename=file.filename, project_id=project_id)
    file_path = project_path / new_filename

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "An error occurred while uploading the file."
            }
        )


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "File uploaded successfully.",
            "file_id": new_filename,
            "project_id": str(project._id)
        }
    )

@router.post("/process/{project_id}")
async def process_file(request: Request,project_id: str, process_request: ProcessRequest):
    process_service = ProcessService(project_id=project_id)
    file_content = process_service.get_file_content(file_id=process_request.file_id)

    project_service = await ProjectService.initialize(db=request.app.database)

    project = await project_service.get_project_or_create(project_id=project_id)

    if file_content is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "Unsupported file type or error loading file content."
            }
        )
    
    file_chunks = process_service.process_file_content(
        file_content=file_content, 
        file_id=process_request.file_id, 
        chunk_size=process_request.chunk_size, 
        chunk_overlap=process_request.overlap_size
    )

    data_chunks = [DataChunk(
        chunk_text=chunk.page_content, 
        chunk_metadata=chunk.metadata, 
        chunk_order=i + 1, 
        chunk_project_id=project.id
    ) for i, chunk in enumerate(file_chunks)]

    chunk_service = await ChunkService.initialize(db=request.app.database)

    if process_request.reset:
        await chunk_service.delete_chunks_by_project_id(project_id=project.id)
        
    result = await chunk_service.insert_many_chunks(chunks=data_chunks)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "File processed successfully.",
            "inserted_chunks": result
        }
    )