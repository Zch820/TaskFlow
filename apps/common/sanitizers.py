import bleach


def sanitize_plain_text(plain_text):
    return bleach.clean(plain_text, tags=[], attributes=[], strip_comments=True).strip()
