"""Language detection and message catalog (English/Spanish)."""
import re

_ES = {"el", "la", "los", "las", "de", "del", "que", "para", "con", "una", "un",
       "necesito", "quiero", "hola", "gracias", "por", "favor", "cuánto", "cuanto",
       "pies", "patio", "jardín", "jardin", "césped", "cesped", "árbol", "arbol",
       "árboles", "arboles", "mi", "tengo", "está", "esta", "y", "es", "cuesta",
       "precio", "cotización", "cotizacion", "aprobar", "aprueba"}
_EN = {"the", "and", "for", "with", "need", "want", "hello", "thanks", "please",
       "how", "much", "my", "have", "is", "a", "to", "of", "yard", "lawn", "tree",
       "trees", "price", "quote", "approve"}


def detect_language(text: str) -> str:
    words = re.findall(r"[a-záéíóúñü]+", text.lower())
    es = sum(w in _ES for w in words) + 2 * len(re.findall(r"[áéíóúñ¿¡]", text.lower()))
    en = sum(w in _EN for w in words)
    return "es" if es > en else "en"


STRINGS = {
    "en": {
        "greeting": "Hi! Thanks for contacting us.",
        "ack": "We received your request. The owner will review your quote and send it shortly.",
        "no_items": "I couldn't tell which work you need. Could you describe the job (for example: 'sod for 1200 sq ft')?",
        "bad_photo": "That photo could not be read. Please send a JPEG or PNG image.",
        "optout": "You're unsubscribed. We won't message you again.",
        "approved": "Good news! Your quote has been approved.",
    },
    "es": {
        "greeting": "¡Hola! Gracias por contactarnos.",
        "ack": "Recibimos su solicitud. El dueño revisará su cotización y se la enviará pronto.",
        "no_items": "No pude entender qué trabajo necesita. ¿Puede describirlo (por ejemplo: 'césped para 1200 pies cuadrados')?",
        "bad_photo": "No se pudo leer esa foto. Por favor envíe una imagen JPEG o PNG.",
        "optout": "Ya no recibirá más mensajes de nosotros.",
        "approved": "¡Buenas noticias! Su cotización fue aprobada.",
    },
}


def t(key: str, lang: str, **kw) -> str:
    lang = lang if lang in STRINGS else "en"
    return STRINGS[lang][key].format(**kw)
