import os

from infrastructure.logging.LoggerImplements import LoggerImplements

logger = LoggerImplements("ConfigLogger")


class Config:
    def __init__(self):
        """
        Config loader for environment variables.
        """
        logger.log_information("Using system environment variables", method="Config.__init__")

        # 👇 UNCOMMENT THIS SECTION FOR LOCAL DEVELOPMENT (.env support)
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env.dev")

        if os.path.exists(env_file):
            from dotenv import load_dotenv

            load_dotenv(env_file)
            logger.log_information(f".env file loaded successfully: {env_file}", method="Config.__init__")
        else:
            logger.log_error(f".env file not found: {env_file}", method="Config.__init__")

    def get(self, key: str, default=None):
        value = os.getenv(key, default)
        if value is not None:
            logger.log_information(f"Loaded env variable: {key}", method="Config.get")
        else:
            logger.log_warning(f"Env variable {key} not defined", method="Config.get")
        return value


# Singleton
CONFIG = Config()
