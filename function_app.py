import json
import logging
import os

import azure.functions as func
import psycopg2
import psycopg2.extras

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode="require",
    )


@app.route(route="pessoas", methods=["GET"])
def listar_pessoas(req: func.HttpRequest) -> func.HttpResponse:
    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM pessoas ORDER BY id")
                rows = cur.fetchall()
        return func.HttpResponse(
            json.dumps(rows, default=str),
            mimetype="application/json",
            status_code=200,
        )
    except Exception as e:
        logging.exception("Erro ao listar pessoas")
        return func.HttpResponse(str(e), status_code=500)


@app.route(route="pessoas", methods=["POST"])
def criar_pessoa(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("Payload JSON inválido", status_code=400)

    nome = body.get("nome")
    idade = body.get("idade")
    tecnologia = body.get("tecnologia_que_o_gledson_ama")

    if not all([nome, idade, tecnologia]):
        return func.HttpResponse(
            "Campos obrigatórios: nome, idade, tecnologia_que_o_gledson_ama",
            status_code=422,
        )

    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO pessoas (nome, idade, tecnologia_que_o_gledson_ama)
                    VALUES (%s, %s, %s)
                    RETURNING *
                    """,
                    (nome, idade, tecnologia),
                )
                row = cur.fetchone()
            conn.commit()
        return func.HttpResponse(
            json.dumps(dict(row), default=str),
            mimetype="application/json",
            status_code=201,
        )
    except Exception as e:
        logging.exception("Erro ao criar pessoa")
        return func.HttpResponse(str(e), status_code=500)
