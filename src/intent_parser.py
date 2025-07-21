import re
from datetime import datetime

MONTH_MAP = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12"
}

def extract_community_areas(user_input):
    """
    Extract community areas as list of integers.
    """
    matches = re.findall(r"(?:community area\s+)?\b([0-9]{1,2})\b", user_input)
    return list(set(int(m) for m in matches))

def extract_crime_types(user_input, known_types):
    """
    Return list of crime types matched in user input.
    """
    return [crime for crime in known_types if crime.lower() in user_input.lower()]

def extract_dates(user_input):
    """
    Extract date strings in 'YYYY-MM' or 'YYYY' format from input.
    """
    patterns = [
        r"\b(" + "|".join(MONTH_MAP.keys()) + r")\s+(\d{4})\b",  # e.g., July 2021
        r"\b(" + "|".join(MONTH_MAP.keys()) + r")\b",            # e.g., March
        r"\b(\d{4})\b"                                           # e.g., 2021
    ]
    
    found = []
    for pattern in patterns:
        matches = re.findall(pattern, user_input, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                month, year = match
                date_str = f"{year}-{MONTH_MAP[month.lower()]}"
                found.append(date_str)
            elif match.lower() in MONTH_MAP:
                found.append(f"2020-{MONTH_MAP[match.lower()]}")
            elif match.isdigit() and len(match) == 4:
                found.append(f"{match}-01")
    
    return sorted(set(found))

def parse_user_input(user_input, known_crime_types):
    """
    Parse user input into structured dictionary.
    Ensure keys exist even if empty.
    """
    crime_types = extract_crime_types(user_input, known_crime_types)
    community_areas = extract_community_areas(user_input)
    dates = extract_dates(user_input)

    # Also extract years from dates (YYYY part only)
    years = []
    for d in dates:
        try:
            years.append(int(d.split("-")[0]))
        except Exception:
            pass
    years = list(set(years))

    return {
        "intent": "",  # You may want to set this properly later
        "crime_types": crime_types,
        "community_areas": community_areas,
        "dates": dates,
        "years": years
    }
