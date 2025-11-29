import os
from pathlib import Path
from dotenv import load_dotenv


# ============================= Path to .env =============================
env_file = Path(__file__).parent.parent / "config" / "env" / "dev.env"
load_dotenv(dotenv_path=env_file)

# ================= Warn if the env file does not exist ==================
if not Path(env_file).exists():
    print(f"\n[WARNING]: ENV_FILE not found: {env_file}\n")

# ========================================================================
#                            ENVs properties
# ========================================================================
class BaseSettings:
    """Base configuration shared across all environments"""
    # ----- Environment:
    CURRENT_ENV: str = os.getenv("APP_ENV", "dev")  # Based on env_file

class DevSettings(BaseSettings):
    """Dev configuration"""

    DSN: str = os.getenv("DSN", "dbname=mydb user=admin password=admin host=localhost port=5432")

class UatSettings(BaseSettings):
    """UAT configuration"""
    pass

class ProdSettings(BaseSettings):
    """Prod configuration"""
    pass

# --- Instantiate the correct settings based on ENV_FILE ---
if "prod.env" in str(env_file).lower():
    settings = ProdSettings()

if "uat.env" in str(env_file).lower():
    settings = UatSettings()

if "dev.env" in str(env_file).lower():
    settings = DevSettings()



# == Test in this file:
if __name__ == "__main__":
    print('\n==> in settings.py')
    print(CURRENT_ENV)
    print(DSN)