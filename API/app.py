import os
import zipfile
from azure.storage.blob import BlobServiceClient
import tensorflow as tf
from transformers import AutoTokenizer

app = FastAPI()




@app.get("/")
def read_root():
    return {"Hello": "World"}

