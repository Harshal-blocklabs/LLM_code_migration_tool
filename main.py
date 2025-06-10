# # main.py
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import logging
# import os
# import requests
# from dotenv import load_dotenv

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# load_dotenv()

# app = FastAPI()

# # Logging
# logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
# logger = logging.getLogger("llm-code-migrator")

# # Define input model
# class MigrationRequest(BaseModel):
#     source_code: str
#     source_language: str
#     target_language: str

# @app.get("/")
# def health_check():
#     return {"status": "ok"}

# @app.post("/migrate")
# def migrate_code(request: MigrationRequest):
#     """
#     Accepts source code and desired target language,
#     calls Ollama LLM endpoint to translate code.
#     """
#     logger.info(f"Received migration request: {request.source_language} -> {request.target_language}")

#     # Ollama endpoint
#     llm_endpoint = os.getenv("LLM_ENDPOINT", "http://localhost:11434/api/generate")
#     model = os.getenv("LLM_MODEL", "codellama")  # You can use mistral, llama3, etc.
#     prompt = f"Convert the following code from {request.source_language} to {request.target_language}:\n\n{request.source_code}"

#     try:
#         response = requests.post(
#             llm_endpoint,
#             json={
#                 "model": model,
#                 "prompt": prompt,
#                 "stream": False
#             },
#             headers={"Content-Type": "application/json"}
#         )
#         response.raise_for_status()
#         data = response.json()

#         return {
#             "migrated_code": data.get("response", "No result"),
#             "model_used": model
#         }

#     except Exception as e:
#         logger.error(f"Error contacting LLM service: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to process LLM request")

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
import os
import requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware  # <- Added this line

load_dotenv()

app = FastAPI()  # <- app must be defined before using it

# CORS middleware (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can set specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("llm-code-migrator")

# Input model
class MigrationRequest(BaseModel):
    source_code: str
    source_language: str
    target_language: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/migrate")
def migrate_code(request: MigrationRequest):
    logger.info(f"Received migration request: {request.source_language} -> {request.target_language}")

    llm_endpoint = os.getenv("LLM_ENDPOINT", "http://localhost:11434/api/generate")
    model = os.getenv("LLM_MODEL", "codellama")
    prompt = f"Convert the following code from {request.source_language} to {request.target_language}:\n\n{request.source_code}"

    try:
        response = requests.post(llm_endpoint, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()

        return {
            "migrated_code": data.get("response", "No result"),
            "model_used": model
        }
    except Exception as e:
        logger.error(f"Error contacting LLM service: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process LLM request")
# 