import pytesseract
from pdf2image import convert_from_bytes
import cv2
import numpy as np
import re
from PIL import Image
from fuzzywuzzy import process, fuzz
from collections import Counter, defaultdict
import concurrent.futures
import asyncio
from app.utility_digitilization.utils.regex.utility_regex import patterns

# Custom Tesseract configuration
TESSERACT_CONFIG = r'--oem 3 --psm 6 -c preserve_interword_spaces=1 tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;()-/& '


def preprocess_image(image):
    """Preprocess the image for better OCR accuracy."""
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    return Image.fromarray(thresh)


def extract_text_from_image(image):
    """Extract text from a single image."""
    processed_image = preprocess_image(image)
    text = pytesseract.image_to_string(
        processed_image,
        config=TESSERACT_CONFIG,
        lang='eng+msa'  # English and Malay languages
    )
    return text


def extract_text_from_pdf(pdf_bytes):
    """Convert PDF pages to images and extract text using parallel processing."""
    images = convert_from_bytes(pdf_bytes, dpi=400)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        texts = list(executor.map(extract_text_from_image, images))
    return "\n".join(texts)


def calculate_accuracy(ground_truth, extracted_text):
    """Calculate the accuracy of the extracted text compared to the ground truth."""
    ground_truth_words = Counter(ground_truth.lower().split())
    extracted_text_words = Counter(extracted_text.lower().split())
    common_words = sum((ground_truth_words & extracted_text_words).values())
    total_words = sum(ground_truth_words.values())
    return (common_words / total_words) * 100 if total_words > 0 else 0


def preprocess_reference_words(reference_words):
    """Preprocess reference words for faster lookup."""
    word_dict = defaultdict(list)
    for word in reference_words:
        word_dict[word[0].lower()].append(word)
    return word_dict


def correct_with_context(text, reference_words_dict, context_size=2, threshold=85):
    """Correct OCR output using fuzzy matching with improved context awareness and performance."""
    words = text.split()
    corrected_words = []
    for i, word in enumerate(words):
        if re.search(r'\w', word):
            start = max(0, i - context_size)
            end = min(len(words), i + context_size + 1)
            context = " ".join(words[start:end])
            potential_matches = reference_words_dict.get(word[0].lower(), [])
            if potential_matches:
                # Use fuzzy matching to find the best match
                matches = process.extractBests(
                    word,
                    potential_matches,
                    scorer=fuzz.ratio,
                    score_cutoff=threshold,
                    limit=3
                )

                # Use partial ratio for better context matching
                if matches:
                    best_match = max(
                        matches,
                        key=lambda x: fuzz.partial_ratio(x[0], context)
                    )

                    # Replace the word if the score is above the threshold
                    if best_match[1] > threshold:
                        corrected_words.append(best_match[0])
                    else:
                        corrected_words.append(word)
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
    return " ".join(corrected_words)


def extract_with_reference(
        text: str,
        patterns: dict
):
    """
    Extract structured data using known patterns.
    :param text: The text to extract data from.
    :param patterns: A dictionary of keys and patterns to extract data.
    """
    return {
        key: re.search(
            pattern,
            text
        ).group(1) if re.search(pattern, text) else 'Not Found' for key, pattern in patterns.items()
    }


# Main function to process the PDF
async def process_pdf(pdf_bytes):
    """
    Process the PDF and return corrected text, extracted structured data, and accuracy.

    Args:
        pdf_bytes (bytes): The bytes of the PDF file.

    Returns:
        dict: A dictionary with corrected text, parsed data, and accuracy (if ground truth is provided).
    """
    try:
        # Use ThreadPoolExecutor to run the CPU-bound task in a separate thread
        loop = asyncio.get_running_loop()
        extracted_text = await loop.run_in_executor(None, extract_text_from_pdf, pdf_bytes)

        # Reference phrases and patterns
        reference_words = ["bil", "nasional", "bagi", "telefon", "penggunaan", "melebihi"]
        reference_words_dict = preprocess_reference_words(reference_words)

        # Correct OCR errors and extract structured data
        # return correct_with_context(extracted_text, reference_words_dict)
        corrected_text = correct_with_context(extracted_text, reference_words_dict)

        # Extract structured data using known patterns
        pattern = patterns.get("tnb")

        if not pattern:
            raise Exception("No pattern found for the utility.")

        parsed_data = extract_with_reference(corrected_text, pattern)

        return {
            "corrected_text": corrected_text,
            "parsed_data": parsed_data
        }
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")
