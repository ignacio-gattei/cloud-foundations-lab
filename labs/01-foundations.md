# Lab 01 — Foundations: setup y pipeline básico

**Clases:** 1 y 2 · **Tiempo estimado:** 30-40 min

Objetivo: levantar el entorno local, procesar eventos y verificar que todo esté en orden antes de la clase 3.

## Prerrequisitos

- Docker Engine (Linux) o Docker Desktop (macOS/Windows + WSL2)
- Python 3.10+ con pip
- Git

## Paso 1 — Bootstrap

```bash
./scripts/bootstrap.sh
```

Qué hace:
- Verifica que Docker y Python estén disponibles
- Crea `.env` desde `.env.example` si no existe
- Crea directorios `data/raw`, `data/processed`, `docs`, `logs`
- Genera `data/raw/events.jsonl` con eventos de ejemplo
- Copia las plantillas de documentación a `docs/`

## Paso 2 — Instalar dependencias Python

```bash
pip install -r requirements.txt
```

## Paso 3 — Levantar servicios base

```bash
docker compose up -d postgres minio redis
```

Esperar a que los healthchecks pasen (≈ 10 segundos):

```bash
docker compose ps
```

Salida esperada: los tres servicios con status `healthy`.

| Servicio  | Puerto | Equivalente AWS      |
|-----------|--------|----------------------|
| postgres  | 5432   | RDS / Aurora         |
| minio     | 9000   | S3                   |
| minio UI  | 9001   | S3 Console           |
| redis     | 6379   | ElastiCache          |

## Paso 4 — Cargar la base de datos

```bash
python scripts/load_postgres.py
```

Qué hace:
- Crea el esquema `events` y la tabla `signups`
- Inserta filas de usuarios de ejemplo
- Imprime el conteo final

Verificar con psql (opcional):

```bash
docker exec -it cloud-foundations-postgres psql -U postgres -d course -c "SELECT * FROM signups;"
```

## Paso 5 — Procesar eventos

```bash
python scripts/process_events.py
```

Salida esperada:

```
Procesados 3 signups → data/processed/signups.json
```

Verificar:

```bash
cat data/processed/signups.json
```

## Paso 6 — Check general

```bash
./scripts/check.sh
```

Resultado esperado: al menos 5 OK, 0 errores críticos.

---

## Entregable de clase

Al finalizar deberías poder mostrar:

- `docker compose ps` con postgres, minio y redis en `healthy`
- `data/processed/signups.json` con al menos 3 registros
- `docs/architecture.md` y `docs/decisions.md` creados

---

## Conexión conceptual (AWS)

| Local                        | AWS equivalente        |
|------------------------------|------------------------|
| `docker compose up postgres` | RDS instance (managed) |
| `data/raw/events.jsonl`      | S3 raw prefix          |
| `scripts/process_events.py`  | Lambda / Glue job      |
| `data/processed/signups.json`| S3 processed prefix    |
