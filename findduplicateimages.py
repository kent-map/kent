from tkinter.filedialog import askdirectory
from tkinter import Tk
import os
import hashlib
import csv
from pathlib import Path


def find_duplicates(start_path):
    file_list = os.walk(start_path)

    unique = dict()
    duplicateimages = dict()

    for root, folders, files in file_list:
        for file in files:
            path = Path(os.path.join(root, file))
            fileHash = hashlib.md5(open(path, 'rb').read()).hexdigest()

            if fileHash not in unique:
                unique[fileHash] = [(path, os.path.getctime(path))]
            else:
                original_path, original_time = unique[fileHash][0]
                duplicate_time = os.path.getctime(path)

                unique[fileHash].append((path, duplicate_time))

                if duplicate_time < original_time:
                    duplicateimages.setdefault(fileHash, []).append((path, original_path))
                else:
                    duplicateimages.setdefault(fileHash, []).append((original_path, path))

    return duplicateimages


def main():
    Tk().withdraw()
    path = askdirectory(title="Select a folder")

    duplicate_images = find_duplicates(path)

    if duplicate_images:
        with open("DuplicateImages.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Original", "Duplicate"])
            #print("Duplicate Images:")
            for hash_value, paths_list in duplicate_images.items():
                for original_path, duplicate_path in paths_list:
                    #print(f"Original: {original_path}\nDuplicate: {duplicate_path}\n")
                    writer.writerow([f"{original_path}", f"{duplicate_path}"])
    else:
        print("No duplicate images found.")


if __name__ == "__main__":
    main()
