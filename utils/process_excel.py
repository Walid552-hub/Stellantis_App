import pandas as pd

def extract_vin_tasks(excel_path):
    df = pd.read_excel(excel_path)
    if 'VIN' not in df.columns or 'Tâche' not in df.columns:
        raise ValueError("Le fichier doit contenir les colonnes 'VIN' et 'Tâche'.")
    vin_groups = df.groupby('VIN')['Tâche'].apply(list).to_dict()
    return vin_groups
