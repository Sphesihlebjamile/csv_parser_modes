from modes.defaultmode import DefaultMode
from dotenv import load_dotenv

# load the .env file
load_dotenv()

def main():
    default_mode = DefaultMode()
    default_mode.run() # run the application

if __name__ == "__main__":
    main()