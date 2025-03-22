# import re
# from transformers import pipeline
# from difflib import SequenceMatcher
# from collections import Counter

# # Initialize the AI model
# qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

# def is_similar(sent1, sent2, threshold=0.75):
#     """Checks if two sentences are similar using fuzzy matching."""
#     return SequenceMatcher(None, sent1, sent2).ratio() > threshold

# def remove_repetitive_sentences(text):
#     """
#     Removes both exact and near-duplicate sentences from chatbot responses.
#     Uses fuzzy matching to detect reworded duplicates.
#     """
#     sentences = re.split(r'(?<=[.!?])\s+', text)  # Split into sentences
#     cleaned_sentences = []
    
#     for sentence in sentences:
#         trimmed_sentence = sentence.strip()
#         if trimmed_sentence and not any(is_similar(trimmed_sentence, s) for s in cleaned_sentences):
#             cleaned_sentences.append(trimmed_sentence)

#     return " ".join(cleaned_sentences)

# def remove_repeated_words(text):
#     """
#     Removes excessive word repetition while preserving meaningful content.
#     Ensures words are not duplicated more than a reasonable amount.
#     """
#     words = text.split()
#     word_count = Counter(words)
    
#     # Limit each word to appear a maximum of 3 times
#     max_repeats = 1
#     filtered_words = []
    
#     for word in words:
#         if word_count[word] > max_repeats:
#             if filtered_words.count(word) < max_repeats:
#                 filtered_words.append(word)
#         else:
#             filtered_words.append(word)
    
#     return " ".join(filtered_words)

# def get_gardening_advice(question):
#     """
#     Generates gardening-related advice using FLAN-T5 and removes redundancy.
#     """
#     prompt = f"Provide detailed gardening advice with steps, tips, and potential challenges: {question}"
    
#     try:
#         response = qa_pipeline(prompt, max_length=500, min_length=100, do_sample=False)
#         cleaned_response = remove_repetitive_sentences(response[0]['generated_text'])
#         final_response = remove_repeated_words(cleaned_response)
#         return final_response
#     except Exception as e:
#         return f"An error occurred: {str(e)}"


import re
from transformers import pipeline
from difflib import SequenceMatcher
from collections import Counter

# Initialize the AI model
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

def is_similar(sent1, sent2, threshold=0.75):
    """Checks if two sentences are similar using fuzzy matching."""
    return SequenceMatcher(None, sent1, sent2).ratio() > threshold

def remove_repetitive_sentences(text):
    """Removes both exact and near-duplicate sentences from chatbot responses."""
    sentences = re.split(r'(?<=[.!?])\s+', text)  
    cleaned_sentences = []
    
    for sentence in sentences:
        trimmed_sentence = sentence.strip()
        if trimmed_sentence and not any(is_similar(trimmed_sentence, s) for s in cleaned_sentences):
            cleaned_sentences.append(trimmed_sentence)

    return " ".join(cleaned_sentences)

def remove_repeated_words(text):
    """Removes excessive word repetition while preserving meaningful content."""
    words = text.split()
    word_count = Counter(words)
    
    max_repeats = 1  # Set limit on repeated words
    filtered_words = []
    
    for word in words:
        if word_count[word] > max_repeats:
            if filtered_words.count(word) < max_repeats:
                filtered_words.append(word)
        else:
            filtered_words.append(word)
    
    return " ".join(filtered_words)

def format_response(text):
    """Formats the response into structured output with headings and bullet points."""
    formatted_text = text.replace("Step 1:", "\n**Step 1:**").replace("Step 2:", "\n**Step 2:**")  
    formatted_text = formatted_text.replace("Tips:", "\n**Tips:**").replace("Challenges:", "\n**Challenges:**")  
    return formatted_text

def get_gardening_advice(question):
    """
    Generates detailed gardening-related advice using FLAN-T5 and removes redundancy.
    """
    prompt = (
        f"You are an expert gardener providing professional advice. "
        f"Give a detailed response with **step-by-step guidance**, **best practices**, and **potential challenges**. "
        f"Use structured formatting for clarity: {question}"
    )
    
    try:
        response = qa_pipeline(prompt, max_length=700, min_length=200, do_sample=True, temperature=0.9)
        cleaned_response = remove_repetitive_sentences(response[0]['generated_text'])
        final_response = remove_repeated_words(cleaned_response)
        formatted_response = format_response(final_response)
        return formatted_response
    except Exception as e:
        return f"Sorry, I couldn't process your request right now. Error: {str(e)}"