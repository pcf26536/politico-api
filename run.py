import os # Import os and sys python modules

from api import create_app # import create_app fxn for api(local) module

config_name = os.getenv("APP_SETTINGS") # Get the app settings defined in the .env file

app = create_app(config_name) # defining the configuration to be used

if __name__ == "__main__": # the interpreter inserts this at the top of the module when run as the main program.
    app.run()
    