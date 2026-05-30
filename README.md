# cloud-foundations-lab

Infraestructura local reutilizable para el modulo Foundations y Cloud Architecture.

## Objetivo

Practicar patrones cloud sin depender de una cuenta AWS:

- object storage con MinIO;
- base relacional con PostgreSQL;
- cache con Redis;
- APIs AWS-like con LocalStack;
- streaming con Redpanda;
- automatizacion con Python;
- IaC con Terraform/OpenTofu.

## Requisitos

- Docker.
- Docker Compose.
- Python 3.
- Git.
- AWS CLI opcional.
- Terraform u OpenTofu opcional.

## Inicio rapido

```bash
./scripts/bootstrap.sh
docker compose up -d
./scripts/check.sh
```

## Servicios

| Servicio | URL/Puerto | Uso |
|---|---|---|
| MinIO API | http://localhost:9000 | S3-compatible object storage |
| MinIO Console | http://localhost:9001 | UI de object storage |
| PostgreSQL | localhost:5432 | Base relacional |
| Redis | localhost:6379 | Cache |
| LocalStack | http://localhost:4566 | APIs AWS-like |
| Redpanda | localhost:9092 | Kafka-compatible streaming |

## Credenciales locales

Estas credenciales son solo para laboratorio local.

- MinIO user: `minioadmin`
- MinIO password: `minioadmin`
- PostgreSQL user: `postgres`
- PostgreSQL password: `postgres`
- PostgreSQL db: `course`

## Mapeo cloud

| Local | Cloud conceptual |
|---|---|
| MinIO | S3 |
| PostgreSQL | RDS/Aurora |
| Redis | ElastiCache |
| LocalStack SQS/SNS/Lambda/EventBridge | Servicios AWS administrados |
| Redpanda | MSK/Kinesis conceptual |
| Docker Compose | Entorno reproducible |
| Terraform/OpenTofu | Infrastructure as Code |

## Uso responsable de AI

Podes usar asistentes AI para explicar errores, revisar README o proponer mejoras, pero:

- no pegues secretos;
- no pegues claves privadas;
- no ejecutes comandos destructivos sin entenderlos;
- valida servicios, limites y seguridad con documentacion oficial.

## Criterios de avance

El repo funciona como evidencia de aprendizaje. Durante el modulo se espera que puedas mostrar:

- `scripts/bootstrap.sh` ejecutado correctamente;
- `scripts/check.sh` ejecutado correctamente;
- datos procesados en `data/processed/`;
- PostgreSQL con schema y datos;
- MinIO con bucket y objetos;
- `docs/architecture.md` actualizado;
- `docs/decisions.md` con tradeoffs;
- `infra/terraform` validado o revisado;
- README suficientemente claro para que otra persona pueda levantar el entorno.

## Defensa final

Al cierre deberias poder explicar:

- que problema resuelve esta arquitectura;
- que representa cada servicio local;
- cual seria su equivalente cloud;
- que riesgos quedan;
- como extenderias el repo para Data Engineering o ML;
- que parte esta expresada como IaC.
