import csv
import logging

from spellchecker import SpellChecker

# Configure logging
logging.basicConfig(filename='spell_checker.log', level=logging.DEBUG)


def load_word_frequencies(filepath='unigram_freq.csv'):
    """Load word frequencies from a CSV file into a dictionary.

    Args:
        filepath (str): The path to the CSV file containing word frequencies.

    Returns:
        dict: A dictionary with words as keys and their frequencies as values.
    """
    word_freq_dict = {}
    try:
        with open(filepath, 'r') as wf:
            freqList = csv.DictReader(wf)
            for row in freqList:
                word_freq_dict[row["word"]] = int(row["count"])
    except FileNotFoundError:
        logging.error(f"Could not find the file at {filepath}")
    except Exception as e:
        logging.error(f"An error occurred while loading word frequencies: {e}")

    return word_freq_dict


word_freq_dict = load_word_frequencies()


def word_freq_test(suggestions):
    """Find the highest frequency word from the suggestions based on a pre-loaded dictionary.

    Args:
        suggestions (list): A list of suggested words.

    Returns:
        str: The highest frequency word from the suggestions.
    """
    highScoringWord = None
    currentCount = 0

    for word in suggestions:
        if word in word_freq_dict:
            count = word_freq_dict[word]
            if count > currentCount:
                highScoringWord = word
                currentCount = count

    return highScoringWord


def spell_check_and_correct(capture):
    """Perform spell checking and correction on a given text.

    Args:
        capture (str): The text to be spell-checked and corrected.

    Returns:
        str: The corrected text.
    """
    spell = SpellChecker()
    words = capture.split()
    misspelled = spell.unknown(words)

    corrected_capture = []

    for word in words:
        if word.lower() in (misspelled_word.lower() for misspelled_word in misspelled):
            suggestions = spell.candidates(word)
            corrected_word = word_freq_test(suggestions)
            if corrected_word:
                corrected_capture.append(corrected_word)
            else:
                corrected_capture.append(word)
        else:
            corrected_capture.append(word)

    corrected_sentence = " ".join(corrected_capture)
    return corrected_sentence
