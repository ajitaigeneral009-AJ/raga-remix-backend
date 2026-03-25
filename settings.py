import os

# API Settings
API_VERSION = "5.0.0"
API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG = True

# Audio Settings
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNELS = 2
MAX_AUDIO_DURATION = 600  # 10 minutes

# Processing Settings
MAX_WORKERS = 4
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour

# File Paths
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)