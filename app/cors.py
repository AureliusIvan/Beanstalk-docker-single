import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def configure_cors(app):
    # Determine the environment
    env = os.getenv("ENVIRONMENT", "dev")

    # Set allowed origins based on the environment
    if env == "dev":
        origins = [
            os.getenv("DEV_ORIGIN", "http://localhost:3000")  # Default to localhost if not set
        ]
    else:
        origins = [
            os.getenv("PROD_ORIGIN", "https://www.ipsolutions4u.com")  # Replace with actual domain
        ]

    # Add CORS middleware to the FastAPI app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
