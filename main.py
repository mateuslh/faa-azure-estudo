import logging
import os
from datetime import datetime

import psycopg2
import psycopg2.extras
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode="require",
    )


def serialize(row: dict) -> dict:
    return {k: v.isoformat() if isinstance(v, datetime) else v for k, v in row.items()}


class Pessoa(BaseModel):
    nome: str
    idade: int
    tecnologia_que_o_gledson_ama: str


@app.get("/pessoas")
def listar_pessoas():
    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM pessoas ORDER BY id")
                rows = [serialize(dict(r)) for r in cur.fetchall()]
        return JSONResponse(rows)
    except Exception as e:
        logging.exception("Erro ao listar pessoas")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pessoas", status_code=201)
def criar_pessoa(pessoa: Pessoa):
    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO pessoas (nome, idade, tecnologia_que_o_gledson_ama)
                    VALUES (%s, %s, %s)
                    RETURNING *
                    """,
                    (pessoa.nome, pessoa.idade, pessoa.tecnologia_que_o_gledson_ama),
                )
                row = serialize(dict(cur.fetchone()))
            conn.commit()
        return JSONResponse(row, status_code=201)
    except Exception as e:
        logging.exception("Erro ao criar pessoa")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/pessoas/{pessoa_id}")
def atualizar_pessoa(pessoa_id: int, pessoa: Pessoa):
    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """
                    UPDATE pessoas
                    SET nome = %s, idade = %s, tecnologia_que_o_gledson_ama = %s
                    WHERE id = %s
                    RETURNING *
                    """,
                    (pessoa.nome, pessoa.idade, pessoa.tecnologia_que_o_gledson_ama, pessoa_id),
                )
                row = cur.fetchone()
            conn.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada")
        return JSONResponse(serialize(dict(row)))
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Erro ao atualizar pessoa")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/pessoas/{pessoa_id}", status_code=204)
def deletar_pessoa(pessoa_id: int):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM pessoas WHERE id = %s RETURNING id", (pessoa_id,))
                deleted = cur.fetchone()
            conn.commit()
        if not deleted:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Erro ao deletar pessoa")
        raise HTTPException(status_code=500, detail=str(e))
