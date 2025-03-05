import os
import shutil
import re

source_folder = "/Users/anastasialelekova/Downloads/archive"

destination_folder = "/Users/anastasialelekova/Desktop/data/clean"

os.makedirs(destination_folder, exist_ok=True)

pattern = r"a\d+\.jpg$"

for filename in os.listdir(source_folder):
    print(f"Checking file: {filename}")
    if re.search(pattern, filename):
        source_file = os.path.join(source_folder, filename)

        destination_file = os.path.join(destination_folder, filename)
        shutil.move(source_file, destination_file)
        print(f"Файл {filename} перемещен в {destination_folder}")
