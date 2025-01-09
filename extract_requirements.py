"""This module takes a file path as input, reads the text, splits into sections by paragraph,
    creates a summary of each paragraph, and saves a json file."""
import sys
import os
import re
import json
import logging

from collections import defaultdict

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


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
        log.error(f"Error: File not found at {file_path}.: {e}")
        return ""
    except PermissionError as e:
        log.error(f"Error: Permission denied to read file at {file_path}.: {e}")
        return ""
    except IsADirectoryError as e:
        log.error(f"Error: {file_path} is a directory, not a file.: {e}")
        return ""
    except OSError as e:
        log.error(f"Error: An OS-related error occurred while reading file at {file_path}: {e}")
        return ""
    except TypeError as e:
        # if file path is not a string
        log.error(f"Error: A type-related error occurred: {e}")
        return ""


def split_text(txt) -> list:
    res = []
    for x in txt.split(os.linesep + os.linesep):
        for y in x.split('\n'):
            for j in re.split(r"(?:\r?\n){2,}", y.strip()):
                if j:
                    res.append(j)
    return res


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
    log.info(f'Extractiong requirements from {file_path}')
    txt = read_file(file_path)
    log.info(f'Found text len {len(txt)} in file.')

    raw_sections = split_text(txt)
    sections = [preprocess_text(x) for x in raw_sections]
    if not sections:
        log.error("Error: File not found, file empty, or permission denied.")
        return
    log.info(f'Found {len(sections)} separate sections.')
    output_object = defaultdict(dict)

    for i, section in enumerate(sections):
        output_object[i]['text'] = section
        output_object[i]['summary'] = get_llm_summary(section)

    with open('extracted_requirements.json', 'w') as f:
        json.dump(output_object, f, indent=4)

    log.info(f'Saved summaries to extracted_requirements.json')


if "__main__" == __name__:
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
    else:
        log.error('Please add filepath argument')
