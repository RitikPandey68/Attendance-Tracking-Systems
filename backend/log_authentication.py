import logging
from fastapi import FastAPI, HTTPException
from routers.auth import router as auth_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/log_authentication/")
async def log_authentication(email: str, password: str):
    logger.info(f"Attempting to log in user: {email}")
    # Here you would typically call your authentication logic
    # For now, just log the attempt
    logger.info("Login attempt logged.")
    return {"message": "Login attempt logged."}

app.include_router(auth_router)
