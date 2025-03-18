import os
from langchain.tools import Tool

def generate_filename(code: str, language: str) -> str:
    # Extract the first few words or a specific identifier from the code
    lines = code.splitlines()
    function_name = "generated_code"  # Default name if no function is found

    for line in lines:
        if line.strip().startswith("def ") or line.strip().startswith("function "):
            function_name = line.split("(")[0].split()[1].strip()  # Adjust for different languages
            break

    # Clean the function name to create a valid filename
    function_name = function_name.replace(" ", "_").replace("(", "").replace(")", "")
    
    # Avoid using special names like __init__ or __str__
    if function_name in ["__init__", "__str__", "__repr__"]:
        function_name = "custom_function"

    # Define a mapping of languages to file extensions
    extension_map = {
        "python": "py",
        "javascript": "js",
        "java": "java",
        "csharp": "cs",
        "ruby": "rb",
        "go": "go",
        "php": "php",
        # Add more languages as needed
    }

    # Get the file extension based on the language, default to 'txt' if not recognized
    extension = extension_map.get(language.lower(), "txt")  # Default to .txt if language not recognized

    return f"{function_name}_code.{extension}"

def save_to_txt(data: str, language: str):
    filename = generate_filename(data, language)  # Generate a unique filename based on the code and language
    try:
        formatted_text = f"# Generated Code\n\n{data}\n"

        with open(filename, "a", encoding="utf-8") as f:
            f.write(formatted_text)

        print(f"Code successfully saved to {filename}")
        return f"Code successfully saved to {filename}"
    except Exception as e:
        print(f"Error writing to file: {e}")
        return f"Error writing to file: {e}"

save_tool = Tool(
    name="save_code_to_file",
    func=save_to_txt,
    description="Saves generated code to a file with a meaningful name based on the programming language.",
)