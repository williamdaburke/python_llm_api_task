"""This module takes a file path as input, reads the text, splits into sections by paragraph,
    creates a summary of each paragraph, and saves a json file."""
import sys
import re
import json

from collections import defaultdict


def get_llm_summary(text_section: str,
                    api_key:str = 'MOCK',
                    mock_api:bool = True) -> str:
    """
    This function takes a text section as input and returns a summary of the text section.
    """
    try:
        # Call the LLM to generate the summary
        if not mock_api:
            # summary = call_llm_api(text_section, api_key)
            raise NotImplementedError("call_llm_api not implemented yet")
        else:
            summary = simulate_llm_summary(text_section)
            return summary
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to generate summary"


def simulate_llm_summary(text_section: str) -> str:
    """
    This is a mock function and in the future, we will use a real LLM to generate the summary.
    """
    words = text_section.split()
    return ' '.join(reversed(words))
    

def preprocess_text(text : str) -> str:
    """
    Preprocesses the input text by removing unwanted characters, converting to lowercase,
    and normalizing whitespace.
    Args:
        text (str): The input text to be preprocessed.
    Returns:
        str: The preprocessed text.
    """
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing whitespace
    text = text.strip()
    return text


def read_file(file_path : str) -> str:
    """
    This function takes a file path as input and returns the contents of the file as a string.
    It handles various types of errors that may occur during file reading, 
    such as file not found, permission denied, directory error, OS-related errors, 
    and type-related errors.
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        print(f"Error: File not found at {file_path}.: {e}")
        return ""
    except PermissionError as e:
        print(f"Error: Permission denied to read file at {file_path}.: {e}")
        return ""
    except IsADirectoryError as e:
        print(f"Error: {file_path} is a directory, not a file.: {e}")
        return ""
    except OSError as e:
        print(f"Error: An OS-related error occurred while reading file at {file_path}: {e}")
        return ""
    except TypeError as e:
        # if file path is not a string
        print(f"Error: A type-related error occurred: {e}")
        return ""


def main(file_path : str) -> None:
    """
    This function takes a file path as input, reads the text, splits into sections by paragraph,
    creates a summary of each paragraph, and saves a json file with the following structure:
    {
        0: {
            'text': '...',
            'summary': '...'
        },
        1: {
            'text': '...',
            'summary': '...'
        },
        ...
    }
    NOTE: currently, the summary is just a mock function and in the future, 
    we will use a real LLM to generate the summary.
    """
    file_txt = read_file(file_path)
    file_txt = preprocess_text(file_txt)
    if not file_txt:
        print("Error: File not found, file empty, or permission denied.")
        return

    paragraphs = file_txt.split('\n\n')
    output_object = defaultdict(dict)

    for i, paragraph in enumerate(paragraphs):
        output_object[i]['text'] = paragraph
        output_object[i]['summary'] = get_llm_summary(paragraph)

    with open('extracted_requirements.json', 'w') as f:
        json.dump(output_object, f, indent=4)


if "__main__" == __name__:
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
