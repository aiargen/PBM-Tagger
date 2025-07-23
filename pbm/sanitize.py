import re

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+|teams\.microsoft\.com\S*', re.IGNORECASE)
HYPHEN_BAR_PATTERN = re.compile(r'-{2,}')
CUST_ENV_PATTERN = re.compile(
    r'\b[a-zA-Z0-9]+-(qa|dev|prod|sand)\b',
    re.IGNORECASE
)

def sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    out = URL_PATTERN.sub('', text)
    out = CUST_ENV_PATTERN.sub('<customer-env>', out)
    out = HYPHEN_BAR_PATTERN.sub('', out)
    # collapse extra whitespace
    out = re.sub(r'\s+', ' ', out).strip()
    return out