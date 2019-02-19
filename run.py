import os  # Import os python modules
from os.path import join, dirname
from dotenv import load_dotenv
from api import create_app  # import create_app fxn for api(local) module

# create .env file path
dotenv_path = join(dirname(__file__), '.env')

# load .env from the path
load_dotenv(dotenv_path)

# Get the app settings defined in the .env file
config_name = os.getenv('APP_SETTINGS')

# defining the configuration to be used
app = create_app(config_name)

# the interpreter inserts this at the top of the module when run as the main program.
if __name__ == "__main__":
    app.run()
