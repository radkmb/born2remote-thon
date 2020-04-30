from dotenv import load_dotenv
import os
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


DATABASE_USER=os.getenv('DATABASE_USER')
DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')
DATABASE_HOST=os.getenv('DATABASE_HOST')
DATABASE_PORT=os.getenv('DATABASE_PORT')
DATABASE_NAME=os.getenv('DATABASE_NAME')
FT_CLIENT_UID=os.getenv("FT_CLIENT_UID")
FT_CLIENT_SECRET=os.getenv("FT_CLIENT_SECRET")
DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")