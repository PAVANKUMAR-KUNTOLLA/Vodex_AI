from fastapi import FastAPI
import os
from typing import Type

from app.clients.sustainable_ai.config import SustainableBotConfig
from app.clients.wealth_bot.config import WealthBotConfig
from app.clients.rfp.config import RFPBotConfig
from app.clients.etl.config import ETLBotConfig

class AppTasks:
    def __init__(self, app: FastAPI):
        self.app = app 
        self._register_events()

    async def initialize_database(self, bot_config_class, env_var: str):
        print("Initializing database...")

        # Get the environment variable value
        env_value = os.environ.get(env_var, "None")
        
        # Check if the environment variable is "None" or empty
        if env_value == "None" or not env_value.strip():
            print(f"Environment variable '{env_var}' is not set or is invalid.")
            return


        # Strip any extra characters from the URL
        endpoints = [endpoint.strip('[]') for endpoint in env_value.split(',')]

        # Iterate through the URLs and initialize each bot configuration
        for endpoint in endpoints:
            print("urls:",endpoint)
            # Create an instance of the bot configuration class with the endpoint
            bot_config_instance = bot_config_class(endpoint)
            print(f"{bot_config_class.__name__} instance: {bot_config_instance}")

            # Check if the method exists in the instance
            if not hasattr(bot_config_instance, 'initialize_bot_configuration'):
                print("Method initialize_bot_configuration does not exist")
            else:
                # Call the initialize_bot_configuration method for each endpoint
                print(f"Calling initialize_bot_configuration with endpoint: {endpoint}")
                await bot_config_instance.initialize_bot_configuration()


    async def startup(self):
        await self.initialize_database(SustainableBotConfig, "SUSTAINABLE_BOT_BOTSETTINGS_ENDPOINT")
        await self.initialize_database(WealthBotConfig, "WEALTH_BOT_BOTSETTINGS_ENDPOINT")
        await self.initialize_database(RFPBotConfig, "RFP_BOT_BOTSETTINGS_ENDPOINT")
        await self.initialize_database(ETLBotConfig,"ETL_BOT_BOTSETTINGS_ENDPOINT")

    def _register_events(self):
        @self.app.on_event("startup")
        async def on_startup():
            await self.startup()
