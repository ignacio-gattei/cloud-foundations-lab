"""
Productor SQS: lee data/raw/events.jsonl y envía cada evento como mensaje.
Equivalente AWS: cualquier servicio que hace send_message a una cola SQS real.

AWS real:
  - endpoint_url no va (usa el endpoint de la región)
  - credenciales reales vía IAM role o env vars
  - misma API boto3

Aqui:
  - endpoint_url apunta a LocalStack en localhost:4566
  - credenciales dummy ("test"/"test")
"""

import json
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

ROOT = Path(__file__).resolve().parents[1]
EVENTS_FILE = ROOT / "data" / "raw" / "events.jsonl"

ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "cloud-foundations-events")

sqs = boto3.client(
    "sqs",
    endpoint_url=ENDPOINT,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    region_name=REGION,
)


def get_or_create_queue(name: str) -> str:
    try:
        resp = sqs.get_queue_url(QueueName=name)
        return resp["QueueUrl"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "AWS.SimpleQueueService.NonExistentQueue":
            resp = sqs.create_queue(QueueName=name)
            print(f"Cola creada: {name}")
            return resp["QueueUrl"]
        raise


def main() -> None:
    if not EVENTS_FILE.exists():
        print(f"Archivo no encontrado: {EVENTS_FILE}")
        print("Ejecutar primero: ./scripts/bootstrap.sh")
        return

    queue_url = get_or_create_queue(QUEUE_NAME)
    print(f"Cola: {QUEUE_NAME} ({queue_url})")

    sent = 0
    with EVENTS_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            event = json.loads(line)
            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(event),
                MessageAttributes={
                    "event_type": {
                        "StringValue": event.get("event", "unknown"),
                        "DataType": "String",
                    }
                },
            )
            print(f"Enviado [{event.get('event', '?'):8s}] user_id={event.get('user_id', '-')}"
                  + (f" country={event['country']}" if "country" in event else ""))
            sent += 1

    print(f"\nTotal enviados: {sent} mensajes")


if __name__ == "__main__":
    main()
