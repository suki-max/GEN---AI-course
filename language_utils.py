from langdetect import detect

LANG_MAP = {
    'en': 'en_XX',
    'hi': 'hi_IN',
    'es': 'es_XX',
    # Add more mappings as needed
}

def detect_language(text: str):
    try:
        lang = detect(text)
        return LANG_MAP.get(lang, 'en_XX')
    except:
        return 'en_XX'
