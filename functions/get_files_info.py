import os

MAX_CHARS = 10000

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
    
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_directory = os.path.abspath(os.path.join(working_directory, directory))

        if not abs_target_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target_directory):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for entry in os.listdir(abs_target_directory):
            entry_path = os.path.join(abs_target_directory, entry)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                entries.append(f'- {entry}: file_size={size} bytes, is_dir={is_dir}')
            except Exception as e:
                return f'Error: Could not get info for "{entry}": {str(e)}'

        return "\n".join(entries)
    
    except Exception as e:
        return f'Error: {str(e)}'


def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_file.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        try:
            with open(abs_target_file, "r", encoding="utf-8") as f:
                content = f.read(MAX_CHARS + 1)
                if len(content) > MAX_CHARS:
                    return content[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
                return content
        except Exception as e:
            return f'Error: Could not read file "{file_path}": {str(e)}'
            
    except Exception as e:
        return f'Error: {str(e)}'