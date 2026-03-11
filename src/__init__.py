import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("AstroAgent")

# validate_config() <-- Comment this out to bypass the OPENAI_API_KEY check
logger = setup_logging()