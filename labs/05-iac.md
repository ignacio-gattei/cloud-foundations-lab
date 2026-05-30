# Lab 05 — IaC: Terraform con LocalStack

**Clase:** 17 · **Tiempo estimado:** 40-50 min

Objetivo: usar Terraform/OpenTofu para crear y gestionar infraestructura local contra LocalStack, entendiendo el flujo plan → apply → state.

## Prerrequisitos

- `docker compose up -d localstack`
- Terraform ≥ 1.5 o OpenTofu ≥ 1.6 instalado
- `awslocal` instalado: `pip install awscli-local`

Verificar:

```bash
terraform version   # o: tofu version
docker compose ps localstack
```

## Paso 1 — Leer el código antes de aplicar

```bash
cat infra/terraform/main.tf
cat infra/terraform/variables.tf
cat infra/terraform/outputs.tf
```

Identificar:
- ¿Qué recursos se van a crear? (3 buckets S3 + 1 cola SQS + 1 DLQ)
- ¿Cuál es el endpoint que apunta a LocalStack?
- ¿Qué significa `skip_credentials_validation = true`?

## Paso 2 — Inicializar

```bash
cd infra/terraform
terraform init
```

Descarga el provider AWS (~10 MB). Salida esperada: `Terraform has been successfully initialized!`

## Paso 3 — Plan (sin tocar nada)

```bash
terraform plan
```

Leer la salida. Cada `+` es un recurso que se va a crear. Verificar que el plan muestra los 5 recursos esperados.

## Paso 4 — Apply

```bash
terraform apply -auto-approve
```

Salida esperada: `Apply complete! Resources: 5 added, 0 changed, 0 destroyed.`

## Paso 5 — Verificar contra LocalStack

```bash
# Buckets creados
awslocal s3 ls

# Cola de eventos
awslocal sqs list-queues

# Outputs de Terraform
terraform output
```

Salida de `terraform output`:

```
bucket_curated  = "cloud-foundations-lab-curated"
bucket_processed = "cloud-foundations-lab-processed"
bucket_raw      = "cloud-foundations-lab-raw"
queue_events_dlq_url = "http://localhost:4566/000000000000/cloud-foundations-lab-events-dlq"
queue_events_url     = "http://localhost:4566/000000000000/cloud-foundations-lab-events"
```

## Paso 6 — Inspeccionar el state

```bash
# Listar recursos en el state
terraform state list

# Detalle de un recurso específico
terraform state show aws_sqs_queue.events
```

El state es el registro de lo que Terraform sabe que existe. Si se borra, Terraform pierde el tracking.

## Paso 7 — Destruir y recrear

```bash
terraform destroy -auto-approve
awslocal s3 ls   # debe estar vacío

terraform apply -auto-approve
awslocal s3 ls   # vuelve a aparecer
```

## Paso 8 — Agregar un recurso nuevo (ejercicio)

Abrir `infra/terraform/main.tf` y agregar un nuevo bucket:

```hcl
resource "aws_s3_bucket" "archive" {
  bucket = "${local.project_name}-archive"
}
```

Luego:

```bash
terraform plan    # debe mostrar 1 recurso para agregar
terraform apply -auto-approve
awslocal s3 ls
```

---

## Entregable de clase

Al finalizar deberías poder mostrar:

- `terraform state list` con 5+ recursos
- `awslocal s3 ls` con los 3 buckets
- `awslocal sqs list-queues` con cola + DLQ
- Nuevo recurso agregado y aplicado

---

## Conexión conceptual (AWS)

| Local (LocalStack)                  | AWS real                           |
|-------------------------------------|------------------------------------|
| `provider "aws" { endpoints {...} }` | Provider sin override de endpoints |
| `terraform apply` → LocalStack      | `terraform apply` → cuenta AWS     |
| `awslocal s3 ls`                    | `aws s3 ls`                        |
| `terraform.tfstate` local           | Remote state en S3 + DynamoDB lock |
| `skip_credentials_validation = true`| Credenciales reales en AWS         |
