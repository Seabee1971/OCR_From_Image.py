import re
from time import sleep

import cv2
import pytesseract


def set_tesseract_cmd(tesseract_cmd_path):
    """Set the path for the Tesseract command."""
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path


def extract_text_from_image(filename):
    """Extract text from an image using Tesseract."""
    return pytesseract.image_to_string(filename)


def clean_text(raw_text):
    """Remove non-alphanumeric characters from the text."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', raw_text)





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
    """Run OCR on the image and save the result to a file."""
    cleaned_text = ""
    set_tesseract_cmd(tesseract_cmd_path)
    processed_images = process_image(file_path)

    if not processed_images:
        print(f"Failed to process image {file_path}")
        return None

    extracted_texts = [extract_text_from_image(img) for img in processed_images]
    unique_combinations = set()

    for i, text1 in enumerate(extracted_texts):
        for j, text2 in enumerate(extracted_texts):
            if i != j:
                combined_text = ''.join(sorted([text1, text2]))
                unique_combinations.add(combined_text)

    result_string = ''.join(unique_combinations)

    if result_string:
        return result_string
    else:
        print(f"Failed to perform OCR on image {file_path}")
        return None
