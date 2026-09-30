import pandas as pd
import unicodedata as uni

def normalizar_nome(coluna:str) -> str:
    """'Agente / Matricula' -> 'Agente_Matricula'"""
    texto = uni.normalize('NFKD', str(coluna))
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.strip().lower()
    for caractere in "-/().$ ":
        texto = texto.replace(caractere, "_")
    while "__" in texto:
        texto = texto.replace("__","_")
    return texto.strip("_")

#Transformar o arquivo em data frame
def transformar (df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    
    df.columns = [normalizar_nome(c) for c in df.columns]
    
    df = df.rename(columns=lambda c: "obs" if c.startswith("obs") else c)
    
    for coluna in df.select_dtypes(include=["object", "str"]).columns:
        df[coluna] = df[coluna].str.strip()
        
    agen_matri = df["agente_matricula"].str.split("/", n=1, expand=True)
    df = df.drop(columns=["agente_matricula"])
    
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["ciclos"] = pd.to_numeric(df["ciclos"], errors="coerce")
    ...
    df["agente"] = agen_matri[0].str.strip()
    df["matricula"] = agen_matri[1].str.strip()
    df["qt"] = pd.to_numeric(df["qt"], errors="coerce")
    ...
    df["dt_coleta"] = pd.to_datetime(df["dt_coleta"], errors="coerce", format="ISO8601").dt.strftime("%Y-%m-%d")
    ...
    df["n_ovos"] = pd.to_numeric(df["n_ovos"], errors="coerce")
    df["obs"] = df["obs"].str.strip()
    
    df = df.dropna(how='all')
    df = df.drop_duplicates()

    return df