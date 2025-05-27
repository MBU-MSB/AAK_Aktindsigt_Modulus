import os


def make_folderpath(serial: str, cpr: str) -> str:
    # Define the base path and create the folder structure
    base_path = r"\\srvsql46\INDBAKKE\AAK_Aktindsigt"
    folder_name = f"{serial}_{cpr}"
    full_path = os.path.join(base_path, folder_name, "Modulus")

    try:
        # Create the folder
        os.makedirs(full_path, exist_ok=True)
        print(f"Folder '{full_path}' created successfully.")
        return full_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
