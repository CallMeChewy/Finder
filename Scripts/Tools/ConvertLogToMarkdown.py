

import json
from datetime import datetime

def convert_jsonl_to_markdown(jsonl_file_path):
    """
    Converts a JSONL chat log to a clean, readable Markdown file.

    This function processes a JSONL file containing chat interactions,
    extracts only the user and assistant messages, and formats them
    into a Markdown file. It intelligently handles various content
    formats, including multi-part messages and code blocks, while
    stripping out all metadata, tool calls, and system messages.

    Args:
        jsonl_file_path (str): The absolute path to the input JSONL file.

    Returns:
        str: The name of the generated Markdown file.
    """
    markdown_lines = []
    
    try:
        with open(jsonl_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    
                    # Skip entries without a 'message' field or with non-text roles
                    if 'message' not in data or 'role' not in data['message']:
                        continue
                        
                    role = data['message'].get('role')
                    content = data['message'].get('content')

                    # Skip system messages, tool calls/results, and empty content
                    if role not in ['user', 'assistant'] or not content:
                        continue

                    # Determine the speaker label
                    speaker = ""
                    if role == 'user':
                        speaker = "**User:**"
                    elif role == 'assistant':
                        speaker = "**Claude:**"

                    # Process content, which can be a list of dicts or a simple string
                    if isinstance(content, list):
                        full_content = []
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                text = item.get('text', '').strip()
                                if text:
                                    full_content.append(text)
                        
                        if full_content:
                            markdown_lines.append(f"{speaker}\n" + "\n\n".join(full_content) + "\n")
                    
                    elif isinstance(content, str) and content.strip():
                        markdown_lines.append(f"{speaker}\n{content.strip()}\n")

                except (json.JSONDecodeError, KeyError) as e:
                    # Silently ignore lines that are not valid JSON or lack expected keys
                    continue

    except FileNotFoundError:
        print(f"Error: The file '{jsonl_file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    # Generate a timestamped filename for the output
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{timestamp}_Conversation.md"
    output_filepath = os.path.join(os.path.dirname(jsonl_file_path), output_filename)

    # Write the cleaned conversation to the Markdown file
    try:
        with open(output_filepath, 'w', encoding='utf-8') as md_file:
            md_file.write("\n".join(markdown_lines))
        
        return output_filename
    except IOError as e:
        print(f"Error writing to file '{output_filepath}': {e}")
        return None

if __name__ == '__main__':
    # The script is designed to be called with the target JSONL file as an argument,
    # but for direct execution, we can hardcode the path relative to the script's location.
    import os
    
    # Assuming the script is in a subdirectory, navigate to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    jsonl_path = os.path.join(project_root, 'Finder.jsonl')
    
    if os.path.exists(jsonl_path):
        generated_file = convert_jsonl_to_markdown(jsonl_path)
        if generated_file:
            print(f"Successfully converted log to '{generated_file}'")
    else:
        print(f"Error: 'Finder.jsonl' not found at the expected path: {jsonl_path}")


