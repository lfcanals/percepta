import os
import sys

def main():
    # Get the parent folder from the command line
    if len(sys.argv) < 2:
        print("Tool to choose the Eye Fish calibration of database to be used in realtime")
        print("")
        print("Usage: python select-eye-fish-calibration.py <folder>")
        sys.exit(1)

    parent_folder = sys.argv[1]

    if not os.path.isdir(parent_folder):
        print(f"Error: '{parent_folder}' is not a folder.")
        sys.exit(1)

    # Get subfolders only
    folders = [
        name for name in os.listdir(parent_folder)
        if os.path.isdir(os.path.join(parent_folder, name))
    ]

    folders.sort()

    if not folders:
        print("No subfolders found.")
        sys.exit(0)

    # Display the folders
    print(f"\nFolders in: {parent_folder}\n")

    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")

    # Ask for selection
    while True:
        try:
            choice = int(input("\nSelect a folder by number: "))

            if 1 <= choice <= len(folders):
                selected_folder = folders[choice - 1]
                break

            print(f"Please enter a number between 1 and {len(folders)}.")

        except ValueError:
            print("Please enter a valid number.")

    # Write active.txt
    active_file = os.path.join(parent_folder, "active.txt")

    with open(active_file, "w", encoding="utf-8") as f:
        f.write(selected_folder)

    print(f"\nSelected: {selected_folder}")
    print(f"Written to: {active_file}")


if __name__ == "__main__":
    main()
