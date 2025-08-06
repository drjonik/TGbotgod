from dateutil import parser
import re

def parse_natural(text: str, lang: str) -> dict:
    # Crude example: extract datetime and text
    dt = parser.parse(text, dayfirst=True)
    cleaned = re.sub(r"(Напомни|Remind|завтра|в|\d{1,2}[\.:]\d{2})", "", text).strip()
    return {'text': cleaned, 'date_time': dt}
