import os

# Folder containing the files
FILE_PATH = "Demo_Fonts"

# Prefix to remove
prefix = "Fontspring-DEMO-"

# Loop through all files in the folder
for filename in os.listdir(FILE_PATH):
    if filename.startswith(prefix):
        # Get the full path of the file
        file_path = os.path.join(FILE_PATH, filename)
        # Rename the file
        new_filename = filename[len(prefix) :]
        new_file_path = os.path.join(FILE_PATH, new_filename)

        # Rename the file
        os.rename(file_path, new_file_path)
        print(f"Renamed {filename} to {new_filename}")
