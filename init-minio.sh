#!/bin/bash

# Aguarda o MinIO estar pronto
sleep 5

# Configura o alias para o cliente mc
mc alias set local http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Cria o bucket se não existir
mc mb local/$MINIO_BUCKET --ignore-existing

# Define política de leitura pública no bucket
mc anonymous set download local/$MINIO_BUCKET

echo "MinIO configurado com sucesso!"
echo "Bucket: $MINIO_BUCKET"
echo "Política: download público habilitado"