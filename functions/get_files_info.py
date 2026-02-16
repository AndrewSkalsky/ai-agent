import os
import os.path
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    
    wd_abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(wd_abs_path,directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([wd_abs_path, target_path]) == wd_abs_path
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path):
        return f'Error: "{target_path}" is not a directory'
    
    dir_listing = os.listdir(target_path)
    dir_desc = []

    for file in dir_listing:
        full_path = os.path.join(target_path,file)
        file_desc = f"- {file}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
        dir_desc.append(file_desc)
    
    return "\n".join(dir_desc)

