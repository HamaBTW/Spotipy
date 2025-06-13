import flet as ft
import pickle
import os


def main(page: ft.Page):

    def your_function():
        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter files that end with ".shb"
        shb_files = [file for file in files if file.endswith(".shb")]
        print(shb_files)

        # Process each .shb file
        for shb_file in shb_files:
            file_path = os.path.join(folder_path, shb_file)
            with open(file_path, "rb") as file:
                content = pickle.load(file)
                # Process deserialized content or perform any necessary actions
                if len(content) > 1:
                    print("---------all--------")
                elif len(content) == 1:
                    print("---------one--------")
                print(len(content))
                print(f"Content of {shb_file}:\n{content}")
                # Your code here
                print("Function executed on app start")
    
    your_function()

    t = ft.Text(value="Hello, world!", color="green")
    page.controls.append(t)
    page.update()

ft.app(target=main)