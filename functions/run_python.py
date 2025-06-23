import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_file.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_target_file):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(
                ["python3", abs_target_file],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=abs_working_directory
            )
            
            output = ""
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            if result.returncode != 0:
                output += f"\nProcess exited with code {result.returncode}"

            if not output.strip():
                return "No output produced."

            return output.strip()

        except subprocess.TimeoutExpired:
            return f'Error: Execution of "{file_path}" timed out after 30 seconds'
        except Exception as e:
            return f'Error: executing Python file: {str(e)}'

    except Exception as e:
        return f'Error: {str(e)}'
