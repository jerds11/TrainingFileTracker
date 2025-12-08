import os
import app
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    print(datetime.now().strftime("%B %d, %Y %I:%M %p"))

    app.run(
        directory = os.getenv("MAIN_DIRECTORY"),
        tracker_directory = os.getenv("TRACKER_FILE_DIRECTORY")
    )
    