import os
from flask import Flask, send_file

app = Flask (__name__)
files_folder = os.path.join(os.path.dirname (__file__), "files")
code_extensions = {
    ".php": "PHP code",
    "license": "legal details",
    ".html": "HTML code",
    ".json": "JSON data file",
    ".sql": "SQL database queries",
    ".js": "JavaScript code",
    ".css": "CSS styles",
}

image_extensions = [".png", ".jpg", ".gif", ".svg", ".ico", ".jpeg"]

def format_path (path):
    path = path.replace (str(files_folder), "").replace('\\', '>')[1:]
    return path


@app.route ("/")
def index ():
    # Show available projects and files

    # Get projets paths
    projects_paths = os.listdir (files_folder)

    # Get all file paths
    file_paths = []
    dir_paths = []
    for root, dirs, files in os.walk (files_folder):

        # Format and save files
        for file in files:
            file_path = os.path.join (root, file)
            file_path = format_path(file_path)
            file_paths.append (file_path)

        # Format and save folders
        for dir in dirs:
            dir_path = os.path.join (root, dir)
            dir_path = format_path(dir_path)
            dir_paths.append (dir_path)


    return {"projects": projects_paths, "all_files": file_paths, "all_dirs": dir_paths}

@app.route ("/<path>/")
def get_file_folder (path):

    # Get path
    path_elems = path.split (">")
    path_regular = os.path.join (files_folder, *path_elems)

    
    # Return content of path its folder
    if os.path.isdir (path_regular):
        file_paths = []
        folder_paths = []

        # Get files and folder for the path
        files = os.listdir (path_regular)
        for file in files:

            # Format
            file_path = os.path.join (path_regular, file)
            file_path = format_path (file_path)

            # Save in separated lists
            if os.path.isdir(file_path):
                file_paths.append (file_path)
            else:
                folder_paths.append (file_path)

        return {"content": {"files": file_paths, "folders": folder_paths}}

    if os.path.isfile (path_regular):
        
        # Return images
        for image_extension in image_extensions:
            if image_extension in path_regular:
                return send_file(path_regular, mimetype=f'image/{image_extension.replace(".", "")}')
        
        # Read text file
        content = ""
        with open (path_regular, encoding='utf-8') as file:
            content = file.read()

        # get code extension details
        file_type = "unknown"
        for extension, details in code_extensions.items():
            if extension in path_regular:
                file_type = details


        # Return file content
        return {"file path": path, "content": content, "file type": file_type}

    # Error file not found
    return {"error": "File not found"}