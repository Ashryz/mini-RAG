
from .file_service import FileService
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



class ProcessService:
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_path = FileService().get_project_path(project_id=project_id)

    def get_file_loader(self, file_id: str):
        file_ext = FileService().get_file_extention(file_id)
        file_path = self.project_path / file_id

        if file_ext == 'txt':
            return TextLoader(file_path, encoding='utf-8')
        if file_ext == 'pdf':
            return PyMuPDFLoader(file_path)
        return None
    
    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        if loader :
            return loader.load()
        return None
    
    def process_file_content(self, file_content:list, file_id: str, chunk_size: int = 100, chunk_overlap: int = 20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,length_function=len)
        file_page_content = [doc.page_content for doc in file_content]
        file_meta = [doc.metadata for doc in file_content]
        file_chunks = text_splitter.create_documents(file_page_content, metadatas=file_meta)
        return file_chunks
