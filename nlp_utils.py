from transformers import pipeline
import logging

# Suppress warnings for unused weights and other deprecations
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
logging.getLogger("transformers.configuration_utils").setLevel(logging.ERROR)
logging.getLogger("transformers.file_utils").setLevel(logging.ERROR)

# Load Hugging Face models
def load_huggingface_pipelines():
    """Load pipelines for summarization and NER (Named Entity Recognition)."""
    print("Loading Hugging Face models...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    ner_pipeline = pipeline(
        "ner",
        model="dbmdz/bert-large-cased-finetuned-conll03-english",
        aggregation_strategy="simple"  # Updated to avoid deprecation
    )
    print("Hugging Face models loaded successfully.")
    return summarizer, ner_pipeline


# Initialize models
summarizer, ner_pipeline = load_huggingface_pipelines()


def summarize_text(text, max_length=130, min_length=30):
    """Summarize long text using a Hugging Face summarization model."""
    print("Summarizing text...")
    if len(text.split()) < 50:
        return text  # Skip summarization for very short text
    try:
        summary = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )
        return summary[0]["summary_text"]
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Error generating summary."


def extract_key_details(text):
    """Extract goals, deliverables, timeline, and evaluation criteria using Hugging Face NER."""
    print("Extracting key details...")
    try:
        ner_results = ner_pipeline(text)
        goals, deliverables, timeline, criteria = [], [], [], []

        for entity in ner_results:
            entity_text = entity["word"]
            entity_label = entity["entity_group"]
            if entity_label in ["ORG", "PRODUCT"]:
                goals.append(entity_text)
            elif entity_label == "DATE":
                timeline.append(entity_text)
            elif entity_label in ["MONEY", "PERCENT"]:
                deliverables.append(entity_text)
            elif "evaluation" in entity_text.lower():
                criteria.append(entity_text)

        return {
            "Goals": " | ".join(goals) if goals else "No specific goals detected.",
            "Deliverables": " | ".join(deliverables) if deliverables else "No specific deliverables detected.",
            "Timeline": " | ".join(timeline) if timeline else "No timeline detected.",
            "Evaluation Criteria": " | ".join(criteria) if criteria else "No evaluation criteria detected.",
        }
    except Exception as e:
        print(f"Error during key detail extraction: {e}")
        return {
            "Goals": "Error extracting goals.",
            "Deliverables": "Error extracting deliverables.",
            "Timeline": "Error extracting timeline.",
            "Evaluation Criteria": "Error extracting evaluation criteria.",
        }


# Example usage for debugging
if __name__ == "__main__":
    sample_text = (
        "Apple is planning to invest $10 billion in renewable energy projects by 2024."
        " The initiative aims to reduce carbon emissions by 40%. Evaluation criteria will "
        "focus on sustainability and long-term impact."
    )
    print("\n--- Summarized Text ---")
    print(summarize_text(sample_text))
    print("\n--- Extracted Key Details ---")
    print(extract_key_details(sample_text))
