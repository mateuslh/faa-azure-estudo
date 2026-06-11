#!/usr/bin/env python3
"""Roda todos os arquivos .sql em migrations/ em ordem."""
import os
import sys
from pathlib import Path

import psycopg2

conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    port=os.environ.get("DB_PORT", "5432"),
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    sslmode="require",
)

migrations_dir = Path(__file__).parent / "migrations"
files = sorted(migrations_dir.glob("*.sql"))

if not files:
    print("Nenhuma migration encontrada.")
    sys.exit(0)

with conn:
    with conn.cursor() as cur:
        for f in files:
            print(f"Rodando {f.name}...")
            cur.execute(f.read_text())

conn.close()
print("Migrations concluídas.")
