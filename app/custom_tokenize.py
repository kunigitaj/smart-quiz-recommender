# app/custom_tokenize.py

from transformers import AutoTokenizer

def custom_tokenize(text, model_name='sentence-transformers/all-mpnet-base-v2'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Manually clean up tokenization spaces
    cleaned_text = text.replace(" ", "").strip()

    return tokenizer(
        cleaned_text,
        padding=True,
        truncation=True,
        return_tensors='pt'
    )
