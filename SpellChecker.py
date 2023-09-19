import csv

from spellchecker import SpellChecker


# Load word frequencies from the CSV file into a dictionary
def load_word_frequencies():
    word_freq_dict = {}
    with open('unigram_freq.csv', 'r') as wf:
        freqList = csv.DictReader(wf)
        for row in freqList:
            word_freq_dict[row["word"]] = int(row["count"])
    return word_freq_dict


word_freq_dict = load_word_frequencies()


def word_freq_test(suggestions):
    highScoringWord = None  # Initialize to None
    currentCount = 0

    for word in suggestions:
        if word in word_freq_dict:
            count = word_freq_dict[word]  # Get word count from the pre-loaded dictionary
            if count > currentCount:
                highScoringWord = word  # Update with the current word
                currentCount = count

    return highScoringWord  # Return the word with the highest frequency


def spell_check_and_correct(capture):
    spell = SpellChecker()
    words = capture.split()
    misspelled = spell.unknown(words)  # Identify misspelled words
    corrected_capture = []  # Initialize an empty list to store corrected words
    print("Words:", words)
    print("Misspelled words:", misspelled)

    for word in words:
        if word.lower() in (misspelled_word.lower() for misspelled_word in misspelled):
            # If the word is misspelled, get its suggestions
            suggestions = spell.candidates(word)
            corrected_word = word_freq_test(suggestions)
            if corrected_word:
                corrected_capture.append(corrected_word)
            else:
                # If no suggestions, keep the original word
                corrected_capture.append(word)
        else:
            # If the word is not misspelled, keep it as is
            corrected_capture.append(word)

    corrected_sentence = " ".join(corrected_capture)
    return corrected_sentence

