# Lab 03 — Queues: SQS con LocalStack

**Clase:** 12 · **Tiempo estimado:** 30-40 min

Objetivo: entender el patrón productor/consumidor con una cola SQS local vía LocalStack.

## Prerrequisitos

- `docker compose up -d localstack`
- Healthcheck de LocalStack OK (`curl http://localhost:4566/_localstack/health`)
- `pip install -r requirements.txt`

## Paso 1 — Levantar LocalStack

```bash
docker compose up -d localstack
docker compose ps localstack
```

Esperar a que el healthcheck muestre `healthy` (puede tardar 20-30 segundos).

## Paso 2 — Crear la cola (opción A: script Python)

```bash
python scripts/produce_sqs.py
```

El script crea la cola `cloud-foundations-events` en LocalStack si no existe y envía los eventos de `data/raw/events.jsonl`.

Salida esperada:

```
Cola: cloud-foundations-events (http://localhost:4566/000000000000/cloud-foundations-events)
Enviado [signup]  user_id=1 country=AR
Enviado [login]   user_id=1
Enviado [signup]  user_id=2 country=UY
...
Total enviados: 8 mensajes
```

## Paso 3 — Crear la cola (opción B: CLI awslocal)

Si tenés `awslocal` instalado (`pip install awscli-local`):

```bash
awslocal sqs create-queue --queue-name cloud-foundations-events
awslocal sqs list-queues
```

## Paso 4 — Consumir mensajes

```bash
python scripts/consume_sqs.py
```

Salida esperada:

```
Consumiendo de cloud-foundations-events...
[1/8] signup  | user_id=1, country=AR, ts=2024-01-15T10:00:00Z
[2/8] login   | user_id=1, ts=2024-01-15T10:05:00Z
...
Cola vacía, se detiene.
```

## Paso 5 — Dead Letter Queue (DLQ)

Cuando Terraform está disponible (clase 17), el repo ya define una DLQ `cloud-foundations-events-dlq` con `maxReceiveCount=3`. Para probarlo:

```bash
cd infra/terraform
terraform init
terraform apply -auto-approve
```

Ver los recursos creados:

```bash
awslocal sqs list-queues
```

---

## Patrones para el diagrama del caso integrador

Dibujá en papel o en el README de tu proyecto el flujo:

```
[Productor (app/script)]
        │
        ▼
  SQS: cloud-foundations-events
        │  (maxReceiveCount=3)
        ▼
[Consumidor (worker)]
        │ (si falla 3 veces)
        ▼
  SQS: cloud-foundations-events-dlq
```

---

## Entregable de clase

Al finalizar deberías poder mostrar:

- Salida de `produce_sqs.py` con mensajes enviados
- Salida de `consume_sqs.py` con mensajes recibidos
- Diagrama productor → cola → consumidor → DLQ

---

## Conexión conceptual (AWS)

| Local                                | AWS equivalente                  |
|--------------------------------------|----------------------------------|
| LocalStack SQS                       | Amazon SQS                       |
| `awslocal sqs create-queue`          | `aws sqs create-queue`           |
| `produce_sqs.py` (boto3 send_message)| Productor con SDK boto3/Java/... |
| `consume_sqs.py` (receive_message)   | Lambda trigger o poller          |
| DLQ con maxReceiveCount=3            | Mismo concepto en SQS real       |
