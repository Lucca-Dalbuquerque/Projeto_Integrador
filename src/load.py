#Imports
import pandas as pd
from contextlib import closing
from pathlib import Path
import sqlite3

#Função para colocar no sqlite
def carregar(df: pd.DataFrame, caminho_db: Path, tabela: str, SCHEMA) -> int:
    caminho_db.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(caminho_db)) as conexao:
        with conexao:
            conexao.executescript(f"BEGIN; DROP TABLE IF EXISTS {tabela}; {SCHEMA}")
            df.to_sql(tabela, conexao, if_exists="append", index=False)
        return conexao.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]