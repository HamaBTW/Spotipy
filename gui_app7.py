from PyTubSearch import YtbSearch
from PyTubMp3 import YtbToMp3
import subprocess
import flet as ft
import threading
import pickle
import os


class Session(ft.UserControl):
    def __init__(self, task_delete, data, page):
        super().__init__()
        self.task_delete = task_delete
        self.data = data
        self.app = MyApp
        self.page = page

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
        #print(session_title)
        #print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()

        self.del_data[0], self.del_data[1]  = username, date

        self.delete_file(self.del_data)

        #in app del
        self.task_delete(self)

    def access_clicked(self, e):
        self.access_data = ["",""]


        session_title = self.display_task.content.content.controls[0].title.value
        session_subtitle = self.display_task.content.content.controls[0].subtitle.value
        #print(session_title)
        #print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()

        self.access_data[0], self.access_data[1]  = username, date

        self.access_file(self.access_data)

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
            
            #print(found)
            if (found == [1,1]):
                try:
                    os.remove(file_path)
                    #print(f"File '{file_path}' has been deleted.")
                except OSError as e:
                    #print(f"Error deleting the file '{file_path}': {e}")
                    pass
            


        # Filter files that end with ".shb"
        shbd_files = [file for file in files if file.endswith(".shbd")]



        # Process each .shb file
        found = [0,0]
        for shb_file in shbd_files:
            found [0], found [1] = 0, 0
            file_path = os.path.join(folder_path, shb_file)
            file_name = f"Spotify Data ({data[1]}).shbd"
            to_del_file_path = os.path.join(folder_path, file_name)
            if (to_del_file_path == file_path):
                found[0] = 1
            with open(file_path, "rb") as file:
                content = pickle.load(file)
                if content['playlist_user_name'] == data[0]:
                    found[1] = 1
            
            #print(found)
            if (found == [1,1]):
                try:
                    os.remove(file_path)
                    #print(f"File '{file_path}' has been deleted.")
                except OSError as e:
                    #print(f"Error deleting the file '{file_path}': {e}")
                    pass
            
        #print(content)

    def access_file(self, data):
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
            
            #print(found)
            if (found == [1,1]):
                with open(file_path, "rb") as file:
                    content = pickle.load(file)
                
                if len(content) == 1:
                    #print(content)
                    self.GoToSongs(content[0])
            
        #print(content)

    def GoToSongs(self, data):
        self.page.clean()
        self.page.add(SongsList(data, self.page))
        #self.app.Load_data(self.app(), None)
        self.page.update()

class MyApp(ft.UserControl):

    def __init__(self, page):
        super().__init__()
        self.tasks = ft.Column([])  # Initialize tasks as a Column control
        self.title = ft.Text()
        self.page = page

    def build(self):

        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter files that end with ".shb"
        shb_files = [file for file in files if file.endswith(".shb")]

        self.tasks = ft.Column([])  # Initialize tasks as a Column control
        self.title = ft.Text(
                            f"Files : {len(shb_files)}", 
                            style=ft.TextThemeStyle.TITLE_LARGE,
                        )
        
        self.reload_btn = ft.FloatingActionButton(
            icon=ft.icons.REPLAY, on_click=self.reload,
        )
        self.add_btn = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.start_web_app,
        )

        self.load_btn = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_UP, on_click=self.load,
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
                ft.Row(
                    controls=[
                        self.reload_btn,
                        self.add_btn,
                    ],
                    alignment="END",
                ),
                ft.Row(
                    controls=[
                        self.title,
                        self.load_btn,
                    ]
                ),
                self.tasks,
            ],
        ),
        padding=50
        )

    def add_clicked(self, data, e):
        self.task = Session(self.task_delete, data, self.page)
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
        #print(shb_files)

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
                    #print("---------all--------")
                elif len(content) == 1:
                    data[0] = content[0]['playlist_name']
                    data[1] = content[0]['user_name']
                    data[2] = content[0]['date']
                    #print("---------one--------")
                    
                #print(data)
                self.add_clicked(data, None)
                

                #print(len(content))
                #print(f"Content of {shb_file}:\n{content}")
                # Your code here
                #print("Function executed on app start")

    def start_web_app(self, instance):

        # Start a thread to read script2.py output in real-time
        script2_process = subprocess.Popen(['python', 'web_app3.py'])

    def reload(self, instance):
        self.page.clean()
        self.page.add(self)
        self.Load_data(None)
        self.page.update()

    def load(self, instance):
        if self.load_btn.icon == ft.icons.KEYBOARD_ARROW_UP:
            self.page.clean()
            self.page.add(self)
            #self.Load_data(None)
            self.page.update()
            self.load_btn.icon = ft.icons.KEYBOARD_ARROW_DOWN
            self.update()
        else:
            self.page.clean()
            self.page.add(self)
            self.Load_data(None)
            self.page.update()
            self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
            self.update()


class SongListItem(ft.UserControl):
    def __init__(self, task_delete, data, page, check_box_clicked_fun):
        super().__init__()
        self.task_delete = task_delete
        self.data = data
        self.page = page
        self.check_box_clicked_fun = check_box_clicked_fun

    def build(self):
        self.display_task = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                            ft.Checkbox(label=f"{self.data}", value=True, on_change=self.check_box_clicked),

                            ],
                            alignment=ft.MainAxisAlignment.NONE,
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
        #print(session_title)
        #print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()

        self.del_data[0], self.del_data[1]  = username, date

        self.delete_file(self.del_data)

        #in app del
        self.task_delete(self)

    def access_clicked(self, e):
        self.access_data = ["",""]


        session_title = self.display_task.content.content.controls[0].title.value
        session_subtitle = self.display_task.content.content.controls[0].subtitle.value
        #print(session_title)
        #print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()

        self.access_data[0], self.access_data[1]  = username, date

        self.access_file(self.access_data)

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
            
            #print(found)
            if (found == [1,1]):
                try:
                    #print(file_path)
                    pass
                except OSError as e:
                    #print(f"Error deleting the file '{file_path}': {e}")
                    pass
            
        #print(content)

    def access_file(self, data):
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
            
            #print(found)
            if (found == [1,1]):
                try:
                    #print(file_path, "wwwwwwwwww")
                    pass
                except OSError as e:
                    #print(f"Error deleting the file '{file_path}': {e}")
                    pass
            
        #print(content)

    def check_box_clicked(self, e):
        self.check_box_clicked_fun(self)

class SongsList(ft.UserControl):
    def __init__(self, data, page):
        super().__init__()
        self.data = data
        self.tasks = ft.Column([])
        self.page = page

    def build(self):

        self.tasks = ft.Column([])  # Initialize tasks as a Column control
        self.back_btn = ft.FloatingActionButton(
            icon=ft.icons.KEYBOARD_BACKSPACE_ROUNDED, on_click=self.GoToHome
        )
        self.load_btn = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_DOWN, on_click=self.reload,
        )
        self.download_btn = ft.FloatingActionButton(
            icon=ft.icons.FILE_DOWNLOAD, on_click=self.download_clicked, bgcolor=ft.colors.GREEN_700,
        )
        self.progress_bar = ft.Column([ ft.Text("Status : Unstarted"), ft.ProgressBar(value=0, bar_height=5, color=ft.colors.GREEN_600)])

        self.check_box = ft.Checkbox(label="Select all songs", on_change=self.checkbox_changed, value=False)
        
        #print("data :", self.data)

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
                ft.Row(
                    controls=[
                        self.back_btn,
                        self.download_btn,
                    ],
                    alignment="END",
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            f"{self.data['playlist_name']} ({len(self.data['playlist_tracks'])} song)", 
                            style=ft.TextThemeStyle.TITLE_LARGE,
                        ),
                        self.load_btn,
                        self.check_box,
                    ]
                ),
                self.progress_bar,
                self.tasks,
            ],
        ),
        padding=50
        )

    def add_clicked(self, data, e):
        self.task = SongListItem(self.task_delete, data, self.page, self.change_check_box_state)
        self.tasks.controls.append(self.task)  # Append task to the tasks Column
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def Load_data_fun(self, instance):
        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)
        #print(self.data)
        for _ in self.data["playlist_tracks"]:
            self.add_clicked(_, None)
                

                #print(len(content))
                #print(f"Content of {shb_file}:\n{content}")
                # Your code here
                #print("Function executed on app start")

    def Load_data(self, instance):
        song_download_thread = threading.Thread(target=lambda : self.Load_data_fun(instance))
        song_download_thread.daemon = True
        song_download_thread.start()

    def start_web_app(self, instance):

        # Start a thread to read script2.py output in real-time
        script2_process = subprocess.Popen(['python', 'web_app3.py'])

    def reload(self, instance):
        if self.load_btn.icon != ft.icons.KEYBOARD_ARROW_UP:
            self.page.clean()
            self.page.add(self)
            self.Load_data(None)
            self.page.update()
            self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
            self.update()
            
            song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(instance))
            song_download_thread.daemon = True
            song_download_thread.start()
        else:
            self.page.clean()
            self.page.add(self)
            self.page.update()
            self.load_btn.icon = ft.icons.KEYBOARD_ARROW_DOWN
            self.update()
            
            song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(instance))
            song_download_thread.daemon = True
            song_download_thread.start()

    def GoToHome(self, data):
        self.page.clean()
        self.page.add(MyApp(self.page))
        #self.app.Load_data(self.app(), None)
        self.page.update()

    def checkbox_changed(self, e):
        if self.check_box.value == True:
            self.check_box.label = "Deselect all songs"
        elif self.check_box.value == False:
            self.check_box.label = "Select all songs"
        self.check_box.update()

        #play list change
        if self.check_box.value == True:
            for _ in (self.tasks.controls):
                check_box = (_.controls[0].controls[0].content.content.controls[0].controls[0])
                check_box.value = True
                #print(check_box.value, check_box.label)
                check_box.update()
        
        if self.check_box.value == False:
            for _ in (self.tasks.controls):
                check_box = (_.controls[0].controls[0].content.content.controls[0].controls[0])
                check_box.value = False
                #print(check_box.value, check_box.label)
                check_box.update()
        
        song_download_thread = threading.Thread(target=lambda : self.export_check_box_data(e))
        song_download_thread.daemon = True
        song_download_thread.start()
        
    def change_check_box_state_fun(self, e):
        
        all_checked =True
        
        for _ in (self.tasks.controls):
            check_box = (_.controls[0].controls[0].content.content.controls[0].controls[0])
            if check_box.value == False:
                all_checked = False
        
        if not all_checked:
            self.check_box.label = "Select all songs"
            self.check_box.value = False
        else:
            self.check_box.label = "Deselect all songs"
            self.check_box.value = True
        
        song_download_thread = threading.Thread(target=lambda : self.export_check_box_data(e))
        song_download_thread.daemon = True
        song_download_thread.start()

        self.check_box.update()

    def change_check_box_state(self, e):
        
        song_download_thread = threading.Thread(target=lambda : self.change_check_box_state_fun(e))
        song_download_thread.daemon = True
        song_download_thread.start()

    def export_check_box_data(self, e):
        chk_bx_data = {"playlist_name":"", "playlist_date":"", "playlist_user_name":"", "select_all_chkbox":"", "data":[]}
        for _ in (self.tasks.controls):
            data_row = {"song":"", "value":""}
            check_box = (_.controls[0].controls[0].content.content.controls[0].controls[0])
            data_row['song'] = check_box.label
            data_row['value'] = check_box.value
            chk_bx_data['data'].append(data_row) 
            chk_bx_data['select_all_chkbox'] = self.check_box.value
            



        #print(self.data)
        chk_bx_data['playlist_user_name'] = self.data['user_name']
        chk_bx_data['playlist_date'] = self.data['date']
        chk_bx_data['playlist_name'] = self.data['playlist_name']
        #print(chk_bx_data)

        folder_path = "./data"  # Replace with the actual path to your folder


        file_name = f"Spotify Data ({self.data['date']}).shbd"
        new_file_path = os.path.join(folder_path, file_name)
        with open(new_file_path, "wb") as file:
            pickle.dump(chk_bx_data, file)

    def load_check_box_data(self, e):
        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter files that end with ".shb"
        shb_files = [file for file in files if file.endswith(".shbd")]



        # Process each .shb file
        found = [0,0]
        file_exist = False
        for shb_file in shb_files:
            found [0], found [1] = 0, 0
            file_path = os.path.join(folder_path, shb_file)
            file_name = f"Spotify Data ({self.data['date']}).shbd"
            to_del_file_path = os.path.join(folder_path, file_name)
            if (to_del_file_path == file_path):
                found[0] = 1
            with open(file_path, "rb") as file:
                content = pickle.load(file)
                #print(content)
                if content['playlist_user_name'] == self.data['user_name']:
                    found[1] = 1
            
            #print(found)
            #print(found)
            if (found == [1,1]):
                file_exist = True
                with open(file_path, "rb") as file:
                    content = pickle.load(file)
                    #print(content)
                    for _ in (self.tasks.controls):
                        check_box = (_.controls[0].controls[0].content.content.controls[0].controls[0])
                        for __ in content['data']:
                            if __['song'] == check_box.label:
                                check_box.value = __['value']
                                check_box.update()
                    self.check_box.value = content['select_all_chkbox'] 
                    self.check_box.update()

    def download_clicked(self, e):
        to_download = []
        for _ in (self.tasks.controls):
            check_box = (_.controls[0].controls[0].content.content.controls[0].controls[0])
            if check_box.value:
                to_download.append(check_box.label)
            
        song_download_thread = threading.Thread(target=lambda : self.download(e, to_download))
        song_download_thread.daemon = True
        song_download_thread.start()
        #print(to_download)

    def download(self, e, songs):
        folder_path = "./output"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        folder_path = f"./output/Spotify songs - {self.data['playlist_name']} - ({self.data['date']})"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


        total_songs = len(songs)
        downloaded_songs = 0
        self.progress_bar.controls[0].value = "Status : Started"
        self.progress_bar.controls[1].value = 0
        self.progress_bar.controls[1].color = ft.colors.GREEN_700
        self.progress_bar.update()


        for song in songs:
            try:
                progress = (downloaded_songs / total_songs)
            except:
                progress = 0
            
            try_var = True
            while try_var:
                try:

                    self.progress_bar.controls[0].value = f"Status : Downloading : {int(progress*100)}% ( {downloaded_songs}/{total_songs} ) : {song}"
                    self.progress_bar.update()

                    data = YtbSearch.Search(song)
                    print(data)

                    video_id = data["video_id"]

                    # List all files in the folder
                    files = os.listdir(folder_path)
                    #print("files :", files)

                    # Filter files that end with ".shb"
                    titles = [file for file in files if file.endswith(".mp3")]
                    
                    ytb_to_mp3 = YtbToMp3(video_id, titles, folder_path)
                    ytb_to_mp3.Download()
                    
                    downloaded_songs += 1
                    progress = (downloaded_songs / total_songs)
                    self.progress_bar.controls[1].value = progress
                    self.progress_bar.update()
                    try_var = False
                except Exception as e:
                    print(e)
                    self.progress_bar.controls[0].value = f"Status : Error : {int(progress*100)}% ( {downloaded_songs}/{total_songs} ) : {song}"
                    self.progress_bar.controls[1].color=ft.colors.RED
                    self.progress_bar.update()
                    try_var = True#must be True
                    #break
        
        if downloaded_songs == total_songs:
            self.progress_bar.controls[0].value = f"Status : Completed ( {downloaded_songs}/{total_songs} songs downloaded )"
            self.progress_bar.controls[1].value = 1
            self.progress_bar.update()
            



def main(page: ft.Page):
    page.title = "ToDo App"
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"
    page.theme_mode = (ft.ThemeMode.DARK)

    page.update()

    #app = MyApp()
    data = ['Plug in Baby - Muse', 'Supermassive Black Hole - Muse', 'Psycho - Muse']
    app = MyApp(page)

    # add application's root control to the page
    
    page.add(app)
    
    page.update()
    
    app.Load_data(None)
    

ft.app(target=main)


