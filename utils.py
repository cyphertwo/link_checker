from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# Nettoyer le texte pour recherche pseudo
def clean_text(text):
    return " ".join(text.lower().split())

# Normalisation avancée des URLs
def normalize_url(url, ignore_query=True):
    parsed = urlparse(url)
    netloc = parsed.netloc.split(":")[0]  # enlever port
    path = parsed.path.rstrip("/")        # supprimer slash final
    query = ""
    if not ignore_query:
        query = urlencode(sorted(parse_qsl(parsed.query)))
    normalized = urlunparse(("", "", netloc + path, "", query, ""))  # fragment vide
    return normalized.lower()
