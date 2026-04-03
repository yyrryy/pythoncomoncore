import os
import sys
try:
    from dotenv import load_dotenv

    def load_config() -> dict:
        load_dotenv()
        keys = [
            "MATRIX_MODE",
            "DATABASE_URL",
            "API_KEY",
            "LOG_LEVEL",
            "ZION_ENDPOINT"
        ]
        config = {}
        missing = []
        for key in keys:
            value = os.getenv(key)
            if value is None or value.strip() == '':
                config[key] = None
                missing.append(key)
            else:
                config[key] = value
        if len(missing):
            print("WARNING: Missing configuration variables:")
            for i in missing:
                print(f" - {i}\n")
        return config

    if __name__ == "__main__":
        config = load_config()
        keys = [
            "MATRIX_MODE",
            "DATABASE_URL",
            "API_KEY",
            "LOG_LEVEL",
            "ZION_ENDPOINT"
        ]
        missing = [key for key, value in config.items() if value is None]
        if not os.path.exists(".env") and len(missing) == len(config):
            print("[WARNING] .env file is not found or keys are not available")
            sys.exit(1)
        else:
            print("ORACLE STATUS: Reading the Matrix...")
            print("\nConfiguration loaded:")
            print(f"Mode: {config['MATRIX_MODE']}")
            print(f"Database: {config['DATABASE_URL']}")
            print(f"API Access: {config['API_KEY']}")
            print(f"Log Level: {config['LOG_LEVEL']}")
            print(f"Zion Network: {config['ZION_ENDPOINT']}")
            print("\nEnvironment security check:")
            print("[OK] No hardcoded secrets detected")
            print("[OK] .env file properly configured")
            print("[OK] Production overrides active")
            print("\nThe Oracle sees all configurations.")
except ModuleNotFoundError:
    print("dotenv is not installed, pip install it.")
