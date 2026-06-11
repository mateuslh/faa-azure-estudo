# faa-azure-estudo — API de Pessoas

API REST em **FastAPI** rodando como **Azure Container App**, com endpoints para cadastrar e listar pessoas. Conecta ao PostgreSQL provisionado pelo [adp-azure-estudo](https://github.com/mateuslh/adp-azure-estudo).

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/pessoas` | Lista todas as pessoas |
| `POST` | `/pessoas` | Cadastra uma pessoa |

**Payload do POST:**
```json
{
  "nome": "Gledson",
  "idade": 30,
  "tecnologia_que_o_gledson_ama": "Azure"
}
```

## Stack

- **Runtime:** Python 3.11 + FastAPI + uvicorn
- **Banco:** PostgreSQL 16 via psycopg2
- **Infra:** Azure Container App (Consumption, escala a zero)
- **Registry:** Azure Container Registry (Basic)
- **IaC:** Terraform

## Recursos criados pelo Terraform

| Recurso | Detalhes |
|---|---|
| Azure Container Registry | SKU Basic, admin enabled |
| Container App Environment | Log Analytics integrado |
| Container App | 0.25 vCPU / 0.5 GB RAM, min 0 réplicas |

## Pipeline

```
push main  →  terraform apply  →  migration  →  docker build + push  →  containerapp update
manual     →  escolhe: apply | destroy
```

## Migrations

Ficam em `migrations/`. São rodadas pelo `migrate.py` a cada deploy, antes do código subir.

Para adicionar uma migration:
```sh
# crie o arquivo seguindo a convenção de nome
migrations/V2__descricao_da_mudanca.sql
```

## Rodando localmente

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=adp_test
export DB_USER=pgadmin
export DB_PASSWORD=senha

uvicorn main:app --reload
```

## Secrets necessários no GitHub

| Secret | Descrição |
|---|---|
| `AZURE_CLIENT_ID` | Service principal client ID |
| `AZURE_CLIENT_SECRET` | Service principal secret |
| `AZURE_SUBSCRIPTION_ID` | ID da subscription |
| `AZURE_TENANT_ID` | ID do tenant |
| `DB_HOST` | FQDN do PostgreSQL (output do adp-azure-estudo) |
| `DB_PASSWORD` | Senha do admin do PostgreSQL |

## Projetos relacionados

- [adp-azure-estudo](https://github.com/mateuslh/adp-azure-estudo) — Provisiona o banco PostgreSQL
- [swa-azure-estudo](https://github.com/mateuslh/swa-azure-estudo) — Frontend estático
