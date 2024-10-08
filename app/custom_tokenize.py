# app/custom_tokenize.py

import warnings
from sentence_transformers import SentenceTransformer

# Suppress specific warning
warnings.filterwarnings("ignore", message=r".*clean_up_tokenization_spaces.*", category=FutureWarning)

def custom_tokenize(text, model_name='sentence-transformers/all-mpnet-base-v2'):
    model = SentenceTransformer(model_name)
    tokenizer = model.tokenizer
    
    # Manually clean up tokenization spaces
    cleaned_text = text.replace("  ", " ").strip()

    return tokenizer(
        cleaned_text,
        padding=True,
        truncation=True,
        return_tensors='pt',
        clean_up_tokenization_spaces=False  # Explicitly set to avoid warning
    )
