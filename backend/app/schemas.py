from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

class FileInput(BaseModel):
    file_path: str
