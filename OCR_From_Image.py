import logging
import re
from itertools import combinations
from time import sleep

import cv2
import pytesseract

# Configure logging
logging.basicConfig(filename='ocr_errors.log', level=logging.ERROR)


def set_tesseract_cmd(tesseract_cmd_path):
    """Set the path for the Tesseract command."""
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path


def extract_text_from_image(filename):
    """Extract text from an image using Tesseract."""
    return pytesseract.image_to_string(filename)


def clean_text(raw_text):
    """Remove non-alphanumeric characters from the text."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', raw_text)


def get_unique_combinations(texts):
    """Get unique combinations of the given texts.

    Args:
        texts (list of str): The list of texts to find unique combinations for.

    Returns:
        set: A set of unique combinations of the input texts.
    """
    return {''.join(sorted(comb)) for comb in combinations(texts, 2)}


def process_image(file_path):
    """Process the image and return its RGB, grayscale, and inverted versions."""
    try:
        img = cv2.imread(file_path)
        sleep(1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        grayscale = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(grayscale)
        return img_rgb, grayscale, inverted
    except Exception as e:
        print(f"Failed to process image {file_path} due to {e}")
        return None


def run_OCR(file_path, tesseract_cmd_path, output_filename):
    """Run OCR on the image and save the result to a file.

    Args:
        file_path (str): The path to the image file.
        tesseract_cmd_path (str): The path to the Tesseract executable.
        output_filename (str): The name of the output file to save the OCR results.

    Returns:
        str: The OCR result string, or None if an error occurs.
    """
    set_tesseract_cmd(tesseract_cmd_path)
    processed_images = process_image(file_path)

    if not processed_images:
        logging.error(f"Failed to process image {file_path}")
        return None

    extracted_texts = [extract_text_from_image(img) for img in processed_images]
    unique_combinations = get_unique_combinations(extracted_texts)

    result_string = ''.join(unique_combinations)

    if result_string:
        return result_string
    else:
        logging.error(f"Failed to perform OCR on image {file_path}")
        return None
