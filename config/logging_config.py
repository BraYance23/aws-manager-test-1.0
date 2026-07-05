import logging
from pathlib import Path

def setup_logging() -> None:

    BASE_DIR = Path(__file__).parent.parent
    PATH_LOG = BASE_DIR/"logs"/"manager_aws.log"
    PATH_LOG.parent.mkdir(parents=True,exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(
                PATH_LOG,
                encoding="utf-8"
            )
        ]
    )
