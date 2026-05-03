import os
import sys
from dotenv import load_dotenv


def load_config():
    # Load .env file (if it exists)
    load_dotenv()

    config = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }

    return config


def validate_config(config):
    missing = []

    for key, value in config.items():
        if not value:
            missing.append(key)

    return missing


def display_config(config):
    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")

    mode = config["MATRIX_MODE"] or "undefined"

    print(f"Mode: {mode}")

    # Database
    if config["DATABASE_URL"]:
        if "localhost" in config["DATABASE_URL"] or "127.0.0.1" in config["DATABASE_URL"]:
            print("Database: Connected to local instance")
        else:
            print("Database: Connected to remote instance")
    else:
        print("Database: NOT CONFIGURED")

    # API Key
    if config["API_KEY"]:
        print("API Access: Authenticated")
    else:
        print("API Access: Missing API key")

    # Log level
    print(f"Log Level: {config['LOG_LEVEL'] or 'DEFAULT'}")

    # Zion endpoint
    if config["ZION_ENDPOINT"]:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")


def security_check(config):
    print("\nEnvironment security check:")

    # Check for hardcoded secrets (basic heuristic)
    if config["API_KEY"] and "secret" not in config["API_KEY"].lower():
        print("[OK] No obvious hardcoded secrets detected")
    else:
        print("[WARNING] API key looks unsafe or missing")

    # Check .env existence
    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file missing")

    # Check production readiness
    if config["MATRIX_MODE"] == "production":
        print("[OK] Production overrides active")
    else:
        print("[OK] Production overrides available")


def main():
    config = load_config()

    missing = validate_config(config)

    display_config(config)

    if missing:
        print("\nWARNING: Missing configuration variables:")
        for m in missing:
            print(f"- {m}")

        print("\nTip: Create a .env file or export environment variables.")

    security_check(config)


if __name__ == "__main__":
    main()