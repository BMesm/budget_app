import pandas as pd

def parse_excel_file(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    # Exemple d’adaptation : ici un format fictif de banque
    if "Montant" in df.columns and "Date opération" in df.columns:
        df = df.rename(columns={
            "Montant": "amount",
            "Date opération": "date",
            "Libellé": "description"
        })
    else:
        raise ValueError("Format non reconnu")

    df = df[["date", "description", "amount"]]
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"])
    return df
