from queue import Queue
import subprocess
import flet as ft
import threading
import pickle
import time
import os


class Session(ft.UserControl):
    def __init__(self, task_delete, data):
        super().__init__()
        self.task_delete = task_delete
        self.data = data

    def build(self):
        self.display_task = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ALBUM, size=60),
                            title=ft.Text(
                                self.data[0], 
                                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                weight=ft.FontWeight.W_400,
                            ),
                            subtitle=ft.Text(
                                f"user : {self.data[1]} \nDate : {self.data[2]}",
                                style=ft.TextThemeStyle.BODY_SMALL,
                            ),
                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Access", 
                                    on_click=self.access_clicked,
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.MaterialState.HOVERED: ft.colors.GREEN,
                                        },
                                    ),
                                ), 
                                ft.TextButton(
                                    "Delete", 
                                    on_click=self.delete_clicked,
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.MaterialState.HOVERED: ft.colors.RED,
                                        },
                                    ),
                                ), 
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                expand=True,
                padding=10,
            )
        )

        return ft.Column(controls=[self.display_task])

    def delete_clicked(self, e):
        self.del_data = ["",""]
        
        session_title = self.display_task.content.content.controls[0].title.value
        session_subtitle = self.display_task.content.content.controls[0].subtitle.value
        print(session_title)
        print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()

        self.del_data[0], self.del_data[1]  = username, date

        self.delete_file(self.del_data)

        #in app del
        self.task_delete(self)

    def access_clicked(self, e):
        session_title = self.display_task.content.content.controls[0].title.value
        session_subtitle = self.display_task.content.content.controls[0].subtitle.value
        print(session_title)
        print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()
        self.update()

    def delete_file(self, data):
        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter files that end with ".shb"
        shb_files = [file for file in files if file.endswith(".shb")]



        # Process each .shb file
        found = [0,0]
        for shb_file in shb_files:
            found [0], found [1] = 0, 0
            file_path = os.path.join(folder_path, shb_file)
            file_name = f"Spotify Data ({data[1]}).shb"
            to_del_file_path = os.path.join(folder_path, file_name)
            if (to_del_file_path == file_path):
                found[0] = 1
            with open(file_path, "rb") as file:
                content = pickle.load(file)
                if content[0]['user_name'] == data[0]:
                    found[1] = 1
            
            print(found)
            if (found == [1,1]):
                try:
                    os.remove(file_path)
                    print(f"File '{file_path}' has been deleted.")
                except OSError as e:
                    print(f"Error deleting the file '{file_path}': {e}")
            
        #print(content)

class MyApp(ft.UserControl):

    def build(self):

        self.tasks = ft.Column([])  # Initialize tasks as a Column control
        self.reload_btn = ft.FloatingActionButton(
            icon=ft.icons.REPLAY, on_click=self.reload,
        )
        self.add_btn = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.start_web_app,
        )
        

        # application's root control (i.e. "view") containing all other controls
        return ft.Container(content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Spotipy",
                            style=ft.TextThemeStyle.DISPLAY_LARGE,
                        ),
                    ],
                    alignment="CENTER",
                ),
                ft.Row(controls=[
                    self.reload_btn,
                    self.add_btn,],
                    alignment="END",
                    ),
                self.tasks,
            ],
        ),
        padding=50
        )

    def add_clicked(self, data, e):
        self.task = Session(self.task_delete, data)
        self.tasks.controls.append(self.task)  # Append task to the tasks Column
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def Load_data(self, instance):
        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter files that end with ".shb"
        shb_files = [file for file in files if file.endswith(".shb")]
        print(shb_files)

        data = ['','','']



        # Process each .shb file
        for shb_file in shb_files:
            file_path = os.path.join(folder_path, shb_file)
            with open(file_path, "rb") as file:
                content = pickle.load(file)
                # Process deserialized content or perform any necessary actions
                if len(content) > 1:
                    data[0] = "All Playlists"
                    data[1] = content[0]['user_name']
                    data[2] = content[0]['date']
                    print("---------all--------")
                elif len(content) == 1:
                    data[0] = content[0]['playlist_name']
                    data[1] = content[0]['user_name']
                    data[2] = content[0]['date']
                    print("---------one--------")
                    
                print(data)
                self.add_clicked(data, None)
                

                #print(len(content))
                #print(f"Content of {shb_file}:\n{content}")
                # Your code here
                #print("Function executed on app start")

    def start_web_app(self, instance):

        # Start a thread to read script2.py output in real-time
        script2_process = subprocess.Popen(['python', 'web_app2.py'])

    def reload(self, instance):
        self.page.clean()
        self.page.add(self)
        self.Load_data(None)
        self.page.update()

class SongListItem(ft.UserControl):
    def __init__(self, task_delete, data):
        super().__init__()
        self.task_delete = task_delete
        self.data = data

    def build(self):
        self.display_task = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ALBUM, size=60),
                            title=ft.Text(
                                self.data[0], 
                                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                weight=ft.FontWeight.W_400,
                            ),
                            subtitle=ft.Text(
                                f"user : {self.data[1]} \nDate : {self.data[2]}",
                                style=ft.TextThemeStyle.BODY_SMALL,
                            ),
                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Access", 
                                    on_click=self.access_clicked,
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.MaterialState.HOVERED: ft.colors.GREEN,
                                        },
                                    ),
                                ), 
                                ft.TextButton(
                                    "Delete", 
                                    on_click=self.delete_clicked,
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.MaterialState.HOVERED: ft.colors.RED,
                                        },
                                    ),
                                ), 
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                expand=True,
                padding=10,
            )
        )

        return ft.Column(controls=[self.display_task])

    def delete_clicked(self, e):
        self.del_data = ["",""]
        
        session_title = self.display_task.content.content.controls[0].title.value
        session_subtitle = self.display_task.content.content.controls[0].subtitle.value
        print(session_title)
        print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()

        self.del_data[0], self.del_data[1]  = username, date

        self.delete_file(self.del_data)

        #in app del
        self.task_delete(self)

    def access_clicked(self, e):
        session_title = self.display_task.content.content.controls[0].title.value
        session_subtitle = self.display_task.content.content.controls[0].subtitle.value
        print(session_title)
        print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()
        self.update()

    def delete_file(self, data):
        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter files that end with ".shb"
        shb_files = [file for file in files if file.endswith(".shb")]



        # Process each .shb file
        found = [0,0]
        for shb_file in shb_files:
            found [0], found [1] = 0, 0
            file_path = os.path.join(folder_path, shb_file)
            file_name = f"Spotify Data ({data[1]}).shb"
            to_del_file_path = os.path.join(folder_path, file_name)
            if (to_del_file_path == file_path):
                found[0] = 1
            with open(file_path, "rb") as file:
                content = pickle.load(file)
                if content[0]['user_name'] == data[0]:
                    found[1] = 1
            
            print(found)
            if (found == [1,1]):
                try:
                    os.remove(file_path)
                    print(f"File '{file_path}' has been deleted.")
                except OSError as e:
                    print(f"Error deleting the file '{file_path}': {e}")
            
        #print(content)

class SongsList(ft.UserControl):

    def build(self):

        self.tasks = ft.Column([])  # Initialize tasks as a Column control
        self.reload_btn = ft.FloatingActionButton(
            icon=ft.icons.REPLAY, on_click=self.reload,
        )
        self.add_btn = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.start_web_app,
        )
        

        # application's root control (i.e. "view") containing all other controls
        return ft.Container(content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Spotipy2",
                            style=ft.TextThemeStyle.DISPLAY_LARGE,
                        ),
                    ],
                    alignment="CENTER",
                ),
                ft.Row(controls=[
                    self.reload_btn,
                    self.add_btn,],
                    alignment="END",
                    ),
                self.tasks,
            ],
        ),
        padding=50
        )

    def add_clicked(self, data, e):
        self.task = SongListItem(self.task_delete, data)
        self.tasks.controls.append(self.task)  # Append task to the tasks Column
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def Load_data(self, instance):
        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter files that end with ".shb"
        shb_files = [file for file in files if file.endswith(".shb")]
        print(shb_files)

        data = ['','','']



        # Process each .shb file
        for shb_file in shb_files:
            file_path = os.path.join(folder_path, shb_file)
            with open(file_path, "rb") as file:
                content = pickle.load(file)
                # Process deserialized content or perform any necessary actions
                if len(content) > 1:
                    data[0] = "All Playlists"
                    data[1] = content[0]['user_name']
                    data[2] = content[0]['date']
                    print("---------all--------")
                elif len(content) == 1:
                    data[0] = content[0]['playlist_name']
                    data[1] = content[0]['user_name']
                    data[2] = content[0]['date']
                    print("---------one--------")
                    
                print(data)
                self.add_clicked(data, None)
                

                #print(len(content))
                #print(f"Content of {shb_file}:\n{content}")
                # Your code here
                #print("Function executed on app start")

    def start_web_app(self, instance):

        # Start a thread to read script2.py output in real-time
        script2_process = subprocess.Popen(['python', 'web_app2.py'])

    def reload(self, instance):
        self.page.clean()
        self.page.add(self)
        self.Load_data(None)
        self.page.update()


def main(page: ft.Page):
    
    page.title = "ToDo App"
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"
    page.update()

    #app = MyApp()
    app = SongsList()

    # add application's root control to the page
    page.add(app)
    
    page.update()
    
    app.Load_data(None)
    

ft.app(target=main)


