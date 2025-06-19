KEYWORDS = {
    "carrefour": "Alimentation",
    "uber": "Transport",
    "sncf": "Transport",
    "netflix": "Abonnement",
    "amazon": "Shopping",
}

def categorize(description: str) -> str:
    description = description.lower()
    for keyword, category in KEYWORDS.items():
        if keyword in description:
            return category
    return "Autres"

def categorize_transactions(df):
    df["category"] = df["description"].apply(categorize)
    return df