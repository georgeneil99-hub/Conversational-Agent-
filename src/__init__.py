import logging
import os
from dotenv import load_dotenv

def setup_logging():
    """Configures basic logging for the agent's internal processes."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("AstroAgent")

def validate_config():
    """Ensures all required environment variables are set before startup."""
    load_dotenv()
    required_keys = ["OPENAI_API_KEY"]
    for key in required_keys:
        if not os.getenv(key):
            raise EnvironmentError(f"Missing required environment variable: {key}")

# Execute validation and setup on package import
validate_config()
logger = setup_logging()
__version__ = "1.0.0"