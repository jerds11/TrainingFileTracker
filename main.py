import app
from pathlib import Path
from datetime import datetime

if __name__ == '__main__':
    print(datetime.now().strftime("%B %d, %Y %I:%M %p"))

    directory = Path(r"C:\Users\erl.jocson\Downloads")
    tracker_directory = Path(r"R:\BE and Transformation Services\Analytics\04 Team Folder\Jocson, Erl Jerrald\Training Dashboard Data Tracker\Data Loaded Tracker.xlsx")

    app.run(
        directory = directory,
        tracker_directory = tracker_directory
    )
    