import os
import zipfile
import tempfile
from fastapi import FastAPI
from azure.storage.blob import BlobServiceClient
import tensorflow as tf
from transformers import AutoTokenizer

app = FastAPI()
# On récupère les variables d'environnement pour le stockage azure
account_name = os.environ.get("AZURE_ACCOUNT_NAME")
account_key = os.environ.get("AZURE_ACCOUNT_KEY")
container_name = os.environ.get("AZURE_CONTAINER_NAME", "models")

blob_service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)

# ---------------------------
# Fonctions utilitaires pour télécharger et dézipper les fichiers depuis Azure
# ---------------------------
def download_and_extract_zip(blob_name, extract_to):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Télécharger le blob dans un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(blob_client.download_blob().readall())
        tmp_file_path = tmp_file.name

    # Extraire le zip
    with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    return extract_to


tmp_model_dir = tempfile.mkdtemp()
tmp_tokenizer_dir = tempfile.mkdtemp()

download_and_extract_zip("Best_BERT_model.zip", tmp_model_dir)
download_and_extract_zip("Best_BERT_tokenizer.zip", tmp_tokenizer_dir)

@app.get("/")
def read_root():
    return {"Hello": "World"}

