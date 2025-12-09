from rich import print
import numpy as np
import os
import pandas as pd

def check_if_loaded(tracker, file):
    for i in tracker:
        if file in i and i[file]:
            return 1, i[file]
    return 0, None

def process_tracker_directory(tracker_directory):
    df = pd.read_excel(tracker_directory)

    df['Field Mapping Complete'] = np.where(df['Field Mapping Complete'] == 1, "True", "False")

    result = (
        df.groupby("Folder", group_keys=False)
        .apply(
            lambda g: [{row["Raw Data File Name"]: row["Field Mapping Complete"]} for _, row in g.iterrows()],
            include_groups=False
        )
        .to_dict()
    )

    return result

def run(directory, tracker_directory) -> None:
    tracker_list = process_tracker_directory(tracker_directory = tracker_directory)
    complete_field_mapping = []
    not_complete_field_mapping = []
    folder_not_yet_added = []
    file_not_yet_added = []

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                print(f"Skipping '{entry.name}' this is not a folder")

            elif entry.is_dir():
                if entry.name in tracker_list:
                    for i in os.scandir(os.path.join(directory, entry.name)):
                        value = check_if_loaded(tracker=tracker_list[entry.name], file=i.name)
                        if value[0] == 1:
                            if value[1] == 'True':
                                complete_field_mapping.append(i.name)
                            else:
                                not_complete_field_mapping.append(i.name)
                        else:
                            print(f"[bold]{entry.name}[/bold]: '{i.name}' - [red]not yet added to the tracker[/red]")
                            file_not_yet_added.append(i.name)
                else:
                    print(f"[bold]{entry.name}[/bold] [red]add to the tracker[/red]")
                    folder_not_yet_added.append(entry.name)

    print("Finish the field mapping for these: ")
    for i in not_complete_field_mapping:
        print(i)

    lists = [
        complete_field_mapping,
        not_complete_field_mapping,
        folder_not_yet_added,
        file_not_yet_added
    ]

    max_len = max(len(lst) for lst in lists)

    padded_lists = [lst + [None]*(max_len - len(lst)) for lst in lists]

    new_df = pd.DataFrame({
        "Completed Field Mapping": padded_lists[0],
        "Not yet finished Field Mapping": padded_lists[1],
        "Folder not yet added to the tracker": padded_lists[2],
        "File not yet added to the tracker": padded_lists[3]
    })

    new_df.to_csv("Tracker output.csv", index = False)