import warnings
from transformers import AutoTokenizer

# Suppress specific warning
warnings.filterwarnings("ignore", message=r".*clean_up_tokenization_spaces.*", category=FutureWarning)

def custom_tokenize(text, model_name='sentence-transformers/all-mpnet-base-v2'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Manually clean up tokenization spaces
    cleaned_text = text.replace("  ", " ").strip()

    return tokenizer(
        cleaned_text,
        padding=True,
        truncation=True,
        return_tensors='pt',
        clean_up_tokenization_spaces=False  # Explicitly set to avoid warning
    )
