"""
Consulta analitica local con DuckDB.
Equivalente local de Athena sobre S3.

Athena real:
  - datos en s3://bucket/processed/
  - tabla definida en Glue Data Catalog
  - motor serverless, costo por datos escaneados

Aqui:
  - datos en data/processed/
  - DuckDB lee directamente el archivo
  - mismo SQL, sin infraestructura adicional
"""

import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
csv_file = ROOT / "data" / "processed" / "sales_by_country.csv"

if not csv_file.exists():
    print(f"Archivo no encontrado: {csv_file}")
    print()
    print("Generarlo con:")
    print("  docker exec -i cloud-foundations-postgres psql -U postgres -d course < sql/003_export_sales_by_country.sql")
    print("  docker cp cloud-foundations-postgres:/tmp/sales_by_country.csv data/processed/sales_by_country.csv")
    sys.exit(1)

conn = duckdb.connect()

print("== Ventas por pais ==")
result = conn.execute(f"""
    SELECT country, total_amount
    FROM read_csv('{csv_file}', AUTO_DETECT=TRUE)
    ORDER BY total_amount DESC
""").fetchdf()
print(result)

print()
print(f"Archivo consultado: {csv_file}")
print()
print("Equivalente en AWS:")
print("  SELECT country, total_amount")
print("  FROM glue_catalog.processed.sales_by_country")
print("  ORDER BY total_amount DESC")
print("  -- Athena cobra por datos escaneados, no por tiempo de ejecucion")
