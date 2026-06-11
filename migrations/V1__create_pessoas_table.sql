CREATE TABLE IF NOT EXISTS pessoas (
    id                          SERIAL PRIMARY KEY,
    nome                        VARCHAR(255)  NOT NULL,
    idade                       INTEGER       NOT NULL,
    tecnologia_que_o_gledson_ama VARCHAR(255) NOT NULL,
    criado_em                   TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);
