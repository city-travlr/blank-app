from transformers import pipeline

# Load Hugging Face models
def load_huggingface_models():
    """Load Hugging Face pipelines for summarization and entity extraction."""
    print("Loading Hugging Face models...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    entity_recognizer = pipeline("ner", grouped_entities=True)
    print("Hugging Face models loaded successfully.")
    return summarizer, entity_recognizer

# Initialize Hugging Face pipelines
summarizer, entity_recognizer = load_huggingface_models()

def extract_key_details_hf(text):
    """Extract goals, deliverables, timeline, and evaluation criteria using Hugging Face."""
    print("Extracting key details...")
    ner_results = entity_recognizer(text)
    goals, deliverables, timeline, criteria = [], [], [], []

    for entity in ner_results:
        entity_text = entity['word']
        entity_label = entity['entity_group']
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

def summarize_text(text, max_length=130, min_length=30):
    """Summarize long text using a Hugging Face model."""
    print("Summarizing text...")
    if len(text.split()) < 50:
        return text  # Skip summarization for very short text
    summary = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False,
    )
    return summary[0]["summary_text"]
