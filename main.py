import os
import app
from datetime import datetime
from dotenv import load_dotenv
from time import time
from rich import print

load_dotenv()

if __name__ == '__main__':
    print(datetime.now().strftime("%B %d, %Y %I:%M %p"))

    start_time = time()
    app.run(
        directory = os.getenv("MAIN_DIRECTORY"),
        tracker_directory = os.getenv("TRACKER_FILE_DIRECTORY")
    )

    end_time = time()

    print(f"{round(end_time - start_time, 0)} seconds")