# Mini RAG (Retrieval-Augmented Generation)

A FastAPI-based application for managing file uploads and retrieval for RAG (Retrieval-Augmented Generation) systems.

## Current Status

⚠️ **In Development** - Implementation paused and will continue later.

## Project Structure

```
Mini-Rag/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuration and settings management
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── base.py          # Base/welcome endpoints (v1)
│   │   └── data.py          # Data/file upload and process endpoints (v1)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── proccess.py      # Request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_service.py  # File management and validation service
│   │   └── proccess_service.py # Document processing and chunking service
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
  - Stores files in project-specific directories
  - Async file writing support

- **File Processing Endpoint**: POST `/api/v1/data/process/{project_id}`
  - Loads and parses PDF and TXT files
  - Chunks files with configurable chunk size and overlap
  - Returns file chunks with metadata
  - Supports custom chunk parameters via request body

- **Base Welcome Endpoint**: GET `/api/v1/`
  - Returns app name and version

- **Configuration System**: Environment-based settings
  - APP_NAME and APP_VERSION
  - File size limits
  - Allowed file extensions
  - Chunk size for file uploads

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
- **Pydantic**: Data validation
- **LangChain**: Document loading and text splitting
- **PyMuPDF**: PDF file processing
- **aiofiles**: Async file operations
- **Uvicorn**: ASGI server
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
```

See `requirements.txt` for complete list.

## Setup & Installation

### Prerequisites
- Python 3.8+
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

3. Install dependencies
```bash
pip install -r requirements.txt
```

## API Endpoints

### Welcome Endpoint
- **GET** `/api/v1/`
  - Returns application name and version

### File Upload
- **POST** `/api/v1/data/upload/{project_id}`
  - **Request**: Multipart form data with file
  - **Response**: File ID for uploaded file
  - **Supported formats**: PDF, TXT (configurable)
  
```json
{
  "success": true,
  "message": "File uploaded successfully.",
  "file_id": "random_key_filename.pdf"
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

The API will be available at `http://localhost:8000`
API documentation (Swagger UI): `http://localhost:8000/docs`
Alternative docs (ReDoc): `http://localhost:8000/redoc`


```

4. Create `.env` file in `app/` directory with your configuration:
```env
APP_NAME=Mini RAG
APP_VERSION=0.1.0
FILE_ALLOWED_EXTENSIONS=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10485760  # 10MB
FILE_CHUNK_SIZE=1048576  # 1MB
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## API Endpoints

### Base API (v1)
- `GET /api/v1/` - Welcome message with app info

### Data API (v1)
- `POST /api/v1/data/upload/{project_id}` - Upload file to a project

## Planned Features

- [ ] File retrieval endpoints
- [ ] RAG integration
- [ ] Vector embeddings
- [ ] Search functionality
- [ ] Project management
- [ ] Authentication & Authorization
- [ ] API documentation enhancements
- [ ] Error handling improvements

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

## Development Notes

- Uses async/await patterns for better performance
- Implements dependency injection for configuration
- File uploads use chunked streaming for memory efficiency
- Filename sanitization to prevent security issues


**Last Updated**: 2026-05-04  
**Status**: In Progress - Implementation Paused
