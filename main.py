import logging
from fastapi import FastAPI
from elasticsearch import Elasticsearch
from datetime import datetime

app = FastAPI()

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200", verify_certs=False)

# Ensure index exists
if not es.indices.exists(index="fastapi-logs"):
    es.indices.create(index="fastapi-logs")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/log")
async def log_message():
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": "This is a test log from FastAPI"
    }
    es.index(index="fastapi-logs", document=log_entry)  # Fixed method
    logger.info("Logged a message to Elasticsearch")
    return {"message": "Check your logs for the logged message!"}
