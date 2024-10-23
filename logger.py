import logging
import logging.config
from pathlib import Path
from typing import Literal


# Function to set up logging
def setup_logging(
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    log_file: Path = Path("app.log"),
):
    level = getattr(
        logging, log_level, logging.INFO
    )  # Default to INFO if not recognized

    # Configure logging
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Log to a file
            logging.StreamHandler(),  # Log to terminal
        ],
    )

    # Optional: You can log the current settings
    logger = logging.getLogger(__name__)
    logger.info(f"Logging started with level {log_level} to file: {log_file}")