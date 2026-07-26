import os
from dotenv import load_dotenv

load_dotenv()

PROMETHEUS_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://192.168.1.254:9090"
)
