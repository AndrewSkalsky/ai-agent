import os
from config import FILE_MAX_LIMIT 
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return content of the file from file_path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the read file, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    wd_abs_path = os.path.abspath(working_directory)
    target_file = os.path.join(wd_abs_path,file_path)

    if os.path.commonpath([target_file,wd_abs_path]) != wd_abs_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    content = ""
    try:
        with open(target_file,'r') as file:
            content = file.read(FILE_MAX_LIMIT)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {FILE_MAX_LIMIT} characters]'
    except Exception as e:
        return f"Error: {e}"

    return content
