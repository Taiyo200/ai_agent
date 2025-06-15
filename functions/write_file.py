import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_file.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        parent_dir = os.path.dirname(abs_target_file)
        if not os.path.exists(parent_dir):
            try:
                os.makedirs(parent_dir)
            except Exception as e:
                return f'Error: Could not create directory for "{file_path}": {str(e)}'

        try:
            with open(abs_target_file, "w", encoding="utf-8") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error: Could not write to "{file_path}": {str(e)}'

    except Exception as e:
        return f'Error: {str(e)}'
