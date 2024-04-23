import re

def extract_numbers(s):
    """
    Extracts all integers from a given string and returns them as a list.

    Args:
    s (str): The string from which to extract numbers.

    Returns:
    List[int]: A list of integers found in the string.
    """

    # Convert all extracted numbers to integers
     # Use regular expression to find the first occurrence of one or more digits
    match = re.search(r'\d+', s)
    # If a match is found, convert it to integer, otherwise return None
    return int(match.group()) if match else None

