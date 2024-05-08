import re
from bs4 import BeautifulSoup

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
    match = re.search(r"\d+", s)
    # If a match is found, convert it to integer, otherwise return None
    return int(match.group()) if match else None


def calculateTotalPages(totalJobs, jobsPerPage):
    if jobsPerPage <= 0:
        return 0  # Edge case: Avoid division by zero and nonsensical negative jobs per page.

    pageCount = (totalJobs + jobsPerPage - 1) // jobsPerPage
    return pageCount


# Define a function that extracts an attribute with case-insensitive matching
def extract_attribute(html_content, tag, search_text, attribute):
    """
    Extracts the specified attribute from a given tag containing the specified text (case-insensitive).

    :param html_content: The HTML string to parse
    :param tag: The HTML tag to search for (e.g., 'label', 'div', 'input', etc.)
    :param search_text: The text to find in the tag's content (case-insensitive)
    :param attribute: The attribute to extract from the found tag
    :return: The attribute value if found, or None if not found
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Convert search text to lowercase
    lower_search_text = search_text.lower()

    # Find the tag with case-insensitive text matching
    element = soup.find(
        tag,
        string=lambda s: lower_search_text in s.lower() if s else False  # Case-insensitive matching
    )

    # Return the attribute value if found, otherwise None
    return element.get(attribute, None) if element else None