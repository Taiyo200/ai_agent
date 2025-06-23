import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_file_content, get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

load_dotenv("env/gemini_api.env")
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        },
    )
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to read."
            )
        },
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to execute."
            )
        },
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to write."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            )
        },
    )
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args or {}

    args["working_directory"] = "./calculator"

    if function_name == "get_files_info":
        args.setdefault("directory", ".")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )

    try:
        result = function_map[function_name](**args)
    except Exception as e:
        result = f"Error during execution: {str(e)}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result}
            )
        ]
    )


if len(sys.argv) > 1:
    prompt = sys.argv[1]
else:
    raise ValueError("Please provide a prompt as a command line argument.")

verbose = "--verbose" in sys.argv or "-v" in sys.argv

messages = [
    types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
]

for i in range(20):
    answer = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    for candidate in answer.candidates:
        messages.append(candidate.content)

    function_call_part = next(
        (part.function_call for part in answer.candidates[0].content.parts if part.function_call),
        None
    )

    if function_call_part:
        function_result = call_function(function_call_part, verbose=verbose)
        messages.append(function_result)

        if verbose:
            response_data = function_result.parts[0].function_response.response
            print(f"-> {response_data}")
    else:
        print("Final response:")
        if answer.candidates[0].content.parts:
            final_text = answer.candidates[0].content.parts[0].text
            print(final_text)
        else:
            print("No final text response from the model.")

        break

if verbose:
    token_count = answer.usage_metadata.prompt_token_count
    candidates_count = answer.usage_metadata.candidates_token_count
    print(f"\nPrompt tokens: {token_count}")
    print(f"Response tokens: {candidates_count}")



