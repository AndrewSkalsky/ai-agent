import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write a file to the file_path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path","content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            )
            ,"content": types.Schema(
                type=types.Type.STRING,
                description="Content that will be written to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    wd_abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(wd_abs_path,file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([wd_abs_path, target_path]) == wd_abs_path
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    os.makedirs(os.path.dirname(target_path),exist_ok=True)
    try:
        with open(target_path,'w') as file:
            file.write(content)
    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
