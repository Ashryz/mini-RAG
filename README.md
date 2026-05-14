# Mini RAG (Retrieval-Augmented Generation)

A FastAPI-based application for managing file uploads, processing, and retrieval for RAG (Retrieval-Augmented Generation) systems with MongoDB integration.

## Current Status

🚀 **Active Development** - File tracking and metadata management system added

**Last Updated**: May 14, 2026 - File metadata storage in MongoDB with indexing implemented

## Project Structure

```
Mini-Rag/
├── app/
│   ├── main.py              # FastAPI application entry point with MongoDB lifespan
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuration and settings management
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── base.py          # Base/welcome endpoints (v1)
│   │   └── data.py          # Data/file upload and process endpoints (v1)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── proccess.py      # File processing request/response schemas
│   │   ├── project.py       # Project schema with indexing configuration
│   │   ├── data_chunk.py    # Data chunk schema with indexing configuration
│   │   └── file.py          # File metadata schema for file tracking
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_service.py  # File management and metadata storage in MongoDB
│   │   ├── proccess_service.py # Document processing and chunking service
│   │   ├── project_service.py  # Project CRUD operations with automatic indexing
│   │   └── chunk_service.py   # Chunk operations with bulk writes and indexing
│   ├── utils/
│   │   └── file_utils.py    # Utility functions
│   └── assets/
│       └── files/           # Storage for uploaded files (organized by project)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features Implemented

### ✅ Complete
- **File Upload Endpoint**: POST `/api/v1/data/upload/{project_id}`
  - Validates file type and size
  - Generates unique filenames with random keys
  - Stores file metadata in MongoDB (name, type, size, upload timestamp)
  - Returns file_id and project_id in response
  - Async file writing support

- **File Metadata Storage**:
  - Tracks all uploaded files with metadata (file_name, file_type, file_size, create_at)
  - Unique constraint on (file_name, project_id) to prevent duplicate filenames
  - Index on file_project_id for efficient file retrieval per project
  - Timestamps for audit trail
  - File association with projectsecific directories
  - Async file writing support

- **File Processing Endpoint**: POST `/api/v1/data/process/{project_id}`
  - Loads and parses PDF and TXT files
  - Chunks files with configurable chunk size and overlap
  - Returns file chunks with metadata
  - Supports custom chunk parameters via request body

- **Project Management System**:
  - Create and retrieve projects
  - Project validation (alphanumeric project IDs)
  - MongoDB integration for data persistence
  - Paginated project listing

- **Data Chunk Storage**:
  - Store processed file chunks in MongoDB
  - Chunk metadata preservation
  - Project association and referencing
  - Chunk ordering within projects
  - Bulk write operations for efficient batch inserts
  - Automatic index creation on collection initialization

- **File Metadata Storage**:
  - Tracks all uploaded files with metadata (file_name, file_type, file_size, create_at)
  - Unique constraint on (file_name, project_id) to prevent duplicate filenames
  - Index on file_project_id for efficient file retrieval per project
  - Timestamps for audit trail
  - File association with projects

- **Database Indexing**:
  - Automatic index creation on service initialization
  - Unique index on project_id for fast lookups and uniqueness
  - Compound unique index on (file_name, file_project_id) for file uniqueness
  - Foreign key index on chunk_project_id for efficient project queries
  - Indexing configuration defined in schema classes
  - Collection initialization with index creation on startup

- **Bulk Operations**:
  - Batch insert chunks with configurable batch size
  - Bulk write operations using InsertOne for efficiency
  - Delete chunks by project ID in bulk operations

- **Base Welcome Endpoint**: GET `/api/v1/`
  - Returns app name and version

- **Configuration System**: Environment-based settings
  - APP_NAME and APP_VERSION
  - File size limits and allowed extensions
  - MongoDB connection settings
  - Chunk size configuration

- **File Management Utilities**:
  - File validation (type and size checks)
  - Unique filename generation
  - Project path management
  - Filename sanitization

- **Document Processing Service**:
  - Multi-format file loader support (PDF, TXT)
  - Recursive character-based text splitting
  - Configurable chunk size and overlap
  - Metadata preservation during processing

## Technologies

- **FastAPI**: Modern async web framework
- **Pydantic**: Data validation with BSON support
- **Motor**: Async MongoDB driver
- **LangChain**: Document loading and text splitting
- **PyMuPDF**: PDF file processing
- **aiofiles**: Async file operations
- **Uvicorn**: ASGI server
- **MongoDB**: NoSQL database for project and chunk storage
- **Python 3.x**: Language

## Dependencies

```
fastapi==0.131.0
pydantic==2.13.3
pydantic-settings==2.14.0
aiofiles==25.1.0
python-dotenv==1.2.2
python-multipart==0.0.22
uvicorn==0.41.0
langchain==1.2.16
langchain-community==0.4.1
langchain-text-splitters==1.1.2
PyMuPDF==1.27.2.3
motor==3.3.2
pymongo==4.6.0
```

See `requirements.txt` for complete list.

## Setup & Installation

### Prerequisites
- Python 3.8+
- MongoDB 4.0+ (running locally or remote)
- Virtual environment (optional but recommended)

### Installation

1. Clone/navigate to project directory
```bash
cd Mini-Rag
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Create `.env` file with configuration
```bash
cat .env.example > .env
```
- set your environment variables in `.env` file

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Ensure MongoDB is running
```bash
# If using Docker
cd docker
cat .env.example > .env
```
- update you `.env` with your credentials
```bash
docker-compose up -d
```



## API Endpoints

### Welcome Endpoint
- **GET** `/api/v1/`
  - Returns application name and version

### File Upload
- **POST** `/api/v1/data/upload/{project_id}`
  - **Request**: Multipart form data with file
  - **Response**: File ID, Project ID, and upload status
  - **Supported formats**: PDF, TXT (configurable)
  
```json
{
  "success": true,
  "message": "File uploaded successfully.",
  "file_id": "507f1f77bcf86cd799439011",
  "project_id": "507f1f77bcf86cd799439012"
}
```

### File Processing
- **POST** `/api/v1/data/process/{project_id}`
  - **Request Body**:
    ```json
    {
      "file_id": "string",
      "chunk_size": 100,
      "overlap_size": 20,
      "reset": false
    }
    ```
## Database Indexing Strategy

The application implements automatic index creation for optimal query performance:

### Project Collection
- **Unique Index on project_id**: Ensures each project has a unique identifier
  - Prevents duplicate projects
  - Accelerates project lookups

### File Collection
- **Index on file_project_id**: Enables efficient queries filtering files by project
  - Speeds up retrieval of all files for a specific project
  - Foreign key relationship support
- **Compound Unique Index on (file_name, file_project_id)**: Ensures unique filenames within a project
  - Prevents duplicate file names in same project
  - Accelerates file lookups by name

### Chunk Collection
- **Index on chunk_project_id**: Enables efficient queries filtering chunks by project
  - Speeds up retrieval of all chunks for a specific project
  - Supports bulk operations on chunks

### Index Creation
- Indexes are automatically created when collections are initialized
- Schema classes define index configuration via `get_indexes()` method
- Services call `initialize()` during app startup to ensure indexes exist
- Non-blocking async index creation

## Services Architecture

### FileService
- Async initialization with automatic index creation on files collection
- CRUD operations for file metadata management
- File validation (type and size checks)
- File metadata storage with timestamps
- Efficient file retrieval by project ID
- Automatic collection creation on first use

### ProjectService
- Async initialization with automatic index creation
- CRUD operations for project management
- Paginated project listing
- Automatic collection creation on first use

### ChunkService  
- Async initialization with automatic index creation
- Bulk write operations for efficient batch processing
- Chunk retrieval by ID
- Delete chunks by project ID
- Metadata support in chunks

## API Endpoints

### Welcome Endpoint
- **GET** `/api/v1/`
  - Returns application name and version

### File Upload
- **POST** `/api/v1/data/upload/{project_id}`
  - **Request**: Multipart form data with file
  - **Response**: File ID, Project ID, and upload status
  - **Supported formats**: PDF, TXT (configurable)
  
```json
{
  "success": true,
  "message": "File uploaded successfully.",
  "file_id": "507f1f77bcf86cd799439011",
  "project_id": "507f1f77bcf86cd799439012"
}
```

### File Processing
- **POST** `/api/v1/data/process/{project_id}`
  - **Request Body**:
    ```json
    {
      "file_id": "string",
      "chunk_size": 100,
      "overlap_size": 20,
      "reset": false
    }
    ```
  - **Response**: Processed file chunks with metadata
    ```json
    {
      "success": true,
      "message": "File processed successfully.",
      "file_chunks": [
        {
          "page_content": "text content...",
          "metadata": {"source": "file.pdf", "page": 0}
        }
      ]
    }
    ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **Base URL**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## File Storage

Uploaded files are organized by project:
```
app/assets/files/
├── project_01/
│   ├── random_key_filename1.txt
│   └── random_key_filename2.txt
├── project_02/
│   └── random_key_document.pdf
```

Each filename is prefixed with a random key to ensure uniqueness.

## Planned Features

- [ ] File retrieval endpoints
- [ ] RAG embedding integration
- [ ] Vector search functionality
- [ ] Advanced project management
- [ ] Authentication & Authorization
- [ ] Rate limiting
- [ ] Batch processing
- [ ] WebSocket support for real-time processing

## Development Notes

- Uses async/await patterns for better performance
- Implements dependency injection for configuration
- File uploads use chunked streaming for memory efficiency
- Filename sanitization to prevent security issues
- MongoDB for scalable data persistence
- Type hints throughout for better IDE support and code quality

## Error Handling

The API returns standardized error responses:
- `400 Bad Request`: File validation failed or invalid request
- `404 Not Found`: Project or file not found
- `500 Internal Server Error`: Server-side processing error

All errors include a descriptive message and success flag for easy client-side handling.
