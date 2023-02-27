import logging
import os
import time
from datetime import datetime
import importlib

# Check if obs-websocket-py is installed, if not install it
try:
    importlib.import_module('obs-websocket-py')
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", 'obs-websocket-py==0.5.3'])

# Define log levels
log_levels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET
}

# Define function for setting up logging
def setup_logging(config):
    # Set up logging
    os.makedirs(config["logging"]["log_folder"], exist_ok=True)
    log_folder = config["logging"]["log_folder"]
    log_level = config["logging"]["file_level"].upper()
    if log_level not in log_levels:
        raise ValueError(f'Invalid log level: {log_level}')
    logging.getLogger().setLevel(log_levels[log_level])

    # Add handler for writing logs to file
    log_file_path = os.path.join(config["logging"]["log_folder"], time.strftime("%Y%m%d-%H%M%S") + '.log')
    file_handler = logging.FileHandler(log_file_path)
    file_level = config["logging"]["file_level"].upper()
    if file_level not in log_levels:
        raise ValueError(f'Invalid log level: {file_level}')
    file_handler.setLevel(log_levels[file_level])

    # Create custom formatter for log messages
    log_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(log_formatter)

    logging.getLogger().addHandler(file_handler)

    # Add handler for writing logs to console
    console_handler = logging.StreamHandler()
    terminal_level = config["logging"]["terminal_level"].upper()
    console_handler.setLevel(log_levels[terminal_level])

    # Create custom formatter for log messages
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)

    logging.getLogger().addHandler(console_handler)
