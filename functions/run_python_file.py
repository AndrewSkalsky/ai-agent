import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python code from pointed file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the executed python file, relative to the working directory.",
            )
            ,"args": types.Schema(
                type=types.Type.ARRAY,
                items= types.Schema( type= types.Type.STRING, ),
                description="List of the parameters passed to executed python file (Default value None).",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    wd_abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(wd_abs_path,file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([wd_abs_path, target_path]) == wd_abs_path
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_path]
    if args != None:
        command.extend(args)

    outputString = ""
    try:
        completed_process = subprocess.run(
            command,
            cwd=working_directory,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
            )
        
        if completed_process.returncode != 0:
            outputString += f"Process exited with code {completed_process.returncode}"
        if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
            outputString = "\n".join([outputString,"No output produced"])
        if len(completed_process.stdout) > 0:
            outputString = "\n".join([outputString,f"STDOUT: {completed_process.stdout}"])
        if len(completed_process.stderr) > 0:
            outputString = "\n".join([outputString,f"STDERR: {completed_process.stderr}"])
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return outputString
    