from functions import *

def load_file_to_string(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        return None
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{file_path}' with UTF-8 encoding.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        return None

html = load_file_to_string("test.txt")

jobj = extract_jobcards_data(html)
print(jobj)