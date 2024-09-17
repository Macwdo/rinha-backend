DROP TABLE IF EXISTS "pessoas";

CREATE TABLE "pessoas" (
  "id" UUID PRIMARY KEY,
  "apelido" VARCHAR(32) UNIQUE,
  "nome" VARCHAR(100),
  "data_nascimento" DATE,
  "stack" TEXT
);

CREATE INDEX "pessoas_apelido" ON "pessoas" ("apelido");
CREATE INDEX "pessoas_nome" ON "pessoas" ("nome");
CREATE INDEX "pessoas_stack" ON "pessoas" ("stack");
