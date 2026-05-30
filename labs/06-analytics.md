# Lab 06 — Analytics: DuckDB como Athena local

**Clase:** 16 · **Tiempo estimado:** 25-35 min

Objetivo: consultar archivos locales con DuckDB usando el mismo SQL que usarías en Athena, entender el patrón serverless analytics.

## Prerrequisitos

- Lab 02 completado (`data/processed/sales_by_country.csv` existe)
- `pip install -r requirements.txt` (incluye `duckdb`)

## Paso 1 — Generar el CSV si no existe

Si no hiciste el Lab 02:

```bash
docker compose up -d postgres
python scripts/load_postgres.py

docker exec -i cloud-foundations-postgres psql -U postgres -d course \
  < sql/003_export_sales_by_country.sql

docker cp cloud-foundations-postgres:/tmp/sales_by_country.csv \
  data/processed/sales_by_country.csv
```

## Paso 2 — Consultar con DuckDB

```bash
python scripts/query_analytics.py
```

Salida esperada:

```
== Ventas por pais ==
  country  total_amount
0      AR        1200.0
1      UY         850.0

Archivo consultado: data/processed/sales_by_country.csv

Equivalente en AWS:
  SELECT country, total_amount
  FROM glue_catalog.processed.sales_by_country
  ORDER BY total_amount DESC
  -- Athena cobra por datos escaneados, no por tiempo de ejecucion
```

## Paso 3 — Explorar DuckDB interactivo

DuckDB tiene una CLI propia (si está instalada):

```bash
duckdb
```

O desde Python interactivo:

```python
import duckdb

conn = duckdb.connect()

# Leer CSV directo
conn.execute("SELECT * FROM read_csv('data/processed/sales_by_country.csv', AUTO_DETECT=TRUE)").df()

# Leer JSONL
conn.execute("SELECT event, count(*) AS n FROM read_json('data/raw/events.jsonl') GROUP BY 1").df()
```

## Paso 4 — Consulta sobre events.jsonl

```python
import duckdb

conn = duckdb.connect()
result = conn.execute("""
    SELECT
        event,
        count(*)           AS total,
        count(DISTINCT user_id) AS usuarios_unicos
    FROM read_json('data/raw/events.jsonl')
    GROUP BY event
    ORDER BY total DESC
""").df()
print(result)
```

Salida esperada:

```
     event  total  usuarios_unicos
0   signup      3                3
1    login      2                2
2 purchase      2                2
3   logout      1                1
```

## Paso 5 — Join entre CSV y JSONL

```python
result = conn.execute("""
    SELECT
        s.country,
        count(e.user_id) AS eventos
    FROM read_csv('data/processed/sales_by_country.csv', AUTO_DETECT=TRUE) s
    JOIN read_json('data/raw/events.jsonl') e
      ON s.country = e.country
    GROUP BY s.country
    ORDER BY eventos DESC
""").df()
print(result)
```

Este patrón (join sobre archivos sin cargarlos a una base) es exactamente lo que hace Athena en AWS.

---

## Entregable de clase

Al finalizar deberías poder mostrar:

- Salida de `query_analytics.py` con ventas por país
- Consulta sobre `events.jsonl` con conteo por tipo de evento
- Explicación de por qué DuckDB ≈ Athena en modelo de costo

---

## Conexión conceptual (AWS)

| Local (DuckDB)                           | AWS equivalente                    |
|------------------------------------------|------------------------------------|
| `duckdb.connect()`                       | Cliente Athena / API StartQueryExecution |
| `read_csv('data/processed/sales.csv')`   | Tabla Glue sobre `s3://bucket/processed/` |
| `read_json('data/raw/events.jsonl')`     | Tabla Glue sobre `s3://bucket/raw/` |
| Sin servidor que levantar                | Athena serverless                  |
| Costo: 0 (local)                         | Athena: $5 por TB escaneado        |
| DuckDB columnar en memoria               | Athena usa Presto/Trino sobre S3   |
