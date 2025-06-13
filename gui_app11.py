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

            # Replace invalid characters
            to_del_file_path = to_del_file_path.replace("<", "").replace(">", "")
            # Replace spaces and other invalid characters
            to_del_file_path = to_del_file_path.replace(" ", "_").replace(":", "-")

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
            # Replace invalid characters
            to_del_file_path = to_del_file_path.replace("<", "").replace(">", "")
            # Replace spaces and other invalid characters
            to_del_file_path = to_del_file_path.replace(" ", "_").replace(":", "-")

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

            # Replace invalid characters
            to_del_file_path = to_del_file_path.replace("<", "").replace(">", "")
            # Replace spaces and other invalid characters
            to_del_file_path = to_del_file_path.replace(" ", "_").replace(":", "-")

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
                
                # if len(content) > 1:
                #     for line in content:
                #         print(line)
                #     #print(content)
                #     #self.GoToSongs(content[0])
            
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
            icon=ft.icons.ADD, on_click=self.showdialog,
        )

        self.load_btn = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_UP, on_click=self.load,
        )

        #search zone
        self.search_field_text = ft.TextField(label="Search", on_focus=self.search_f, on_blur=self.search_b, on_change=self.search_c, expand=True, animate_scale=20)
        self.search_field_date = ""
        ft.TextField(label="Search", on_focus=self.search_f, on_blur=self.search_b, on_change=self.search_c, expand=True,)
        self.search_field = self.search_field_text
        self.search_icon = ft.Icon(ft.icons.SEARCH, opacity=0.5, expand=True,)
        self.search_drop_down = ft.Dropdown(
            value="Playlist Name",
            options=[
                    ft.dropdown.Option("Playlist Name"),
                    ft.dropdown.Option("User Name"),
            ],
            width=135,
            expand=False,
            on_change=self.dropdown_change,
        )
        
        self.search_bar = ft.Stack(
            [
                ft.Container(
                    content=self.search_icon,
                    alignment=ft.alignment.center_right,
                    padding=16,
                    expand=True,
                ),
                self.search_field,
                
            ],
            width=300,
            
        )

        #web thing
        self.user_id = ft.TextField(label="user id", expand=True, password=True, error_text="")
        self.user_id_btn = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, on_click=self.show_hide_id, icon_color=ft.colors.WHITE)
        self.user_secret = ft.TextField(label="user secret", expand=True, password=True, error_text="")
        self.user_secret_btn = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, on_click=self.show_hide_secret, icon_color=ft.colors.WHITE)
        self.go_btn = ft.FloatingActionButton(icon=ft.icons.ARROW_FORWARD, on_click=self.submit)
        self.how_to_btn = ft.FloatingActionButton(icon=ft.icons.QUESTION_MARK_OUTLINED)
        self.form = ft.Row(controls=[self.user_id, self.user_id_btn, self.user_secret, self.user_secret_btn, self.go_btn, self.how_to_btn])

        self.bgDialog = ft.ResponsiveRow([
            ft.Container(
            width=self.page.window_width,
            height=self.page.window_height,
            bgcolor="#000000",
            ink=False,
            # SET TRANSPARENT YOU BG DIALOG
            opacity=0.6,
            # THIS IS IF BG DIALOG IS CLICK
            # THEN CLOSE YOU DIALOG
            on_click=self.hidedialog,
            disabled=True,
    
                )
    
            ])

        self.dialog = ft.Container(
            border_radius=30,
            margin=ft.margin.only(top=80,left=30,right=30),
            height=200,
            alignment=ft.alignment.center,
            content=self.form,
            # SET EFFECT SLIDE UP FOR YOU DIALOG
            offset=ft.transform.Offset(0,2),
            animate_offset=ft.animation.Animation(duration=300,curve="easeIn"),
            padding=ft.padding.only(top=20,left=50,right=50),
    
            )
    
        self.modal = ft.Container(content=ft.Stack([self.bgDialog,self.dialog]), opacity=0, animate_opacity=300)
        

        # application's root control (i.e. "view") containing all other controls
        return ft.Container(
            content=ft.Column(
            controls=[
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
                        self.search_bar,
                        self.search_drop_down,
                    ]
                ),
                self.tasks,
                self.modal,
            ],
        ),
        padding=50
        )

    def load_web_app_data(sef, f_name):
        with open(f_name, "rb") as f:
            data = pickle.load(f)
        return data

    def export_web_app_data(self, f_name):
        c_id = self.user_id.value
        c_sc = self.user_secret.value
        with open(f_name, "wb") as f:
            pickle.dump({"client_id":str(c_id), "client_secret":str(c_sc)}, f)
        self.hidedialog(None)
        
    def showdialog(self, e):
        if self.modal.opacity == 0:
            self.modal.opacity = 1 
 
        if self.modal.opacity == 1:
            self.dialog.offset = ft.transform.Offset(0,0) 
		
        self.bgDialog.controls[0].disabled = False
        self.bgDialog.update()

        file_path = "./data"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
		
        file_path = "./data/web app data.wbspy"
		
        if not os.path.exists(file_path):
            f = open(file_path, "wb")
            pickle.dump({"client_id":"", "client_secret":""}, f)
            f.close()

        web_data = self.load_web_app_data(file_path)

        self.user_id.value = web_data['client_id']
        self.user_id.update()
        self.user_secret.value = web_data['client_secret']
        self.user_secret.update()
 
        self.page.update()

    def hidedialog(self, e):
        if self.modal.opacity != 0:
            self.modal.opacity = 0

        if self.modal.opacity != 1:
            ft.transform.Offset(0,2)

        self.bgDialog.controls[0].disabled = True
        self.bgDialog.update()
 
        self.page.update()

    def show_hide_id(self, e):
        self.user_id.password = not self.user_id.password
        self.user_id_btn.icon_color=ft.colors.WHITE if self.user_id_btn.icon_color==ft.colors.GREEN else ft.colors.GREEN
        self.user_id_btn.update()
        self.user_id.update()
	
    def show_hide_secret(self, e):
        self.user_secret.password = not self.user_secret.password
        self.user_secret_btn.icon_color=ft.colors.WHITE if self.user_secret_btn.icon_color==ft.colors.GREEN else ft.colors.GREEN
        self.user_secret_btn.update()
        self.user_secret.update()

    def submit(self, e):
        ok = True
        if len(self.user_secret.value) != 32 or len(self.user_id.value) != 32:
            ok = False
		
        if len(self.user_id.value) != 32:
            self.user_id.error_text = "invalid format"
        else:
            self.user_id.error_text = ""
        self.user_id.update()

        if len(self.user_secret.value) != 32:
            self.user_secret.error_text = "invalid format"
        else:
            self.user_secret.error_text = ""
        self.user_secret.update()
		
        if ok:
            file_path = "./data/web app data.wbspy"
            self.export_web_app_data(file_path)
            self.start_web_app(e)

    def dropdown_change(self, e):
            to_search = self.search_field.value.replace('  ', '')
            to_search_type = self.search_drop_down.value
            
            if to_search_type != "Date":
                self.reload(e)

            #self.search_field.value = to_search
            self.search_field.update()
            self.search_drop_down.value = to_search_type
            self.search_drop_down.update()

    def search_f(self, e):
        self.search_bar.width=None
        self.search_icon.opacity=1
        self.search_bar.expand = True
        self.search_field.update()
        self.search_bar.update()
        self.search_icon.update()
       
    def search_b(self, e):
        self.search_bar.width=300
        self.search_icon.opacity=0.5
        self.search_bar.expand = False
        self.search_field.update()
        self.search_bar.update()
        self.search_icon.update()
    
    def search_c(self, e):
        value = self.search_field.value
        value = value.replace(' ','')
        to_search = self.search_field.value.replace('  ', '')
        to_search_type = self.search_drop_down.value
        if self.search_drop_down.value == "Playlist Name":
            self.search_c_fun(e, value, "Playlist Name")
            self.search_field.value = to_search
            self.search_field.update()
            self.search_field.focus()
            self.search_drop_down.value = to_search_type
            self.search_drop_down.update()
        elif self.search_drop_down.value == "User Name":
            self.search_c_fun(e , value, "User Name")
            self.search_field.value = to_search
            self.search_field.update()
            self.search_field.focus()
            self.search_drop_down.value = to_search_type
            self.search_drop_down.update()
        
    def search_c_fun(self, e, to_search, search_type):
        self.page.clean()
        self.page.add(self)
        self.Load_data_search_pl_n(None, to_search, search_type)
        self.page.update()
        self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
        self.update()
    
    def Load_data_search_pl_n(self, instance, to_search, search_type):
        folder_path = "./data"  # Replace with the actual path to your folder

        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter files that end with ".shb"
        shb_files = [file for file in files if file.endswith(".shb")]
        #print(shb_files)

        data = ['','','','']



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
                    data[3] = content[0]['error_tracks']
                    #print("---------all--------")
                elif len(content) == 1:
                    data[0] = content[0]['playlist_name']
                    data[1] = content[0]['user_name']
                    data[2] = content[0]['date']
                    data[3] = content[0]['error_tracks']
                    #print("---------one--------")
                    
                #print(data)
                if search_type == "Playlist Name":
                    if to_search.lower() in data[0].lower():
                        self.add_clicked(data, None)
                elif search_type == "User Name":
                    if to_search.lower() in data[1].lower():
                        self.add_clicked(data, None)
                elif search_type == "Date":
                    if to_search.lower() in data[2].lower():
                        self.add_clicked(data, None)

                #print(len(content))
                #print(f"Content of {shb_file}:\n{content}")
                # Your code here
                #print("Function executed on app start")
    
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

        data = ['','','','']



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
                    data[3] = content[0]['error_tracks']
                    #print("---------all--------")
                elif len(content) == 1:
                    data[0] = content[0]['playlist_name']
                    data[1] = content[0]['user_name']
                    data[2] = content[0]['date']
                    data[3] = content[0]['error_tracks']
                    #print("---------one--------")
                    
                #print(data)
                self.add_clicked(data, None)
                

                #print(len(content))
                #print(f"Content of {shb_file}:\n{content}")
                # Your code here
                #print("Function executed on app start")

    def start_web_app(self, instance):

        # Start a thread to read script2.py output in real-time
        script2_process = subprocess.Popen(['Spotipy web connector.exe'])

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

            # Replace invalid characters
            to_del_file_path = to_del_file_path.replace("<", "").replace(">", "")
            # Replace spaces and other invalid characters
            to_del_file_path = to_del_file_path.replace(" ", "_").replace(":", "-")

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

            # Replace invalid characters
            to_del_file_path = to_del_file_path.replace("<", "").replace(">", "")
            # Replace spaces and other invalid characters
            to_del_file_path = to_del_file_path.replace(" ", "_").replace(":", "-")

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
        self.data_type = "normal"

    def build(self):

        self.tasks = ft.Column([])  # Initialize tasks as a Column control
        self.back_btn = ft.FloatingActionButton(
            icon=ft.icons.KEYBOARD_BACKSPACE_ROUNDED, on_click=self.GoToHome,
        )
        self.load_btn = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_DOWN, on_click=self.reload,
        )
        self.download_btn = ft.FloatingActionButton(
            icon=ft.icons.FILE_DOWNLOAD, on_click=self.download_clicked, bgcolor=ft.colors.GREEN_700,
        )

        self.downloaded_songs_btn = ft.FloatingActionButton(
            icon=ft.icons.AUDIO_FILE, on_click=self.open_songs_folder, bgcolor=ft.colors.YELLOW_900,
        )

        self.errors_btn = ft.FloatingActionButton(
            icon=ft.icons.ERROR_OUTLINE_OUTLINED, on_click=self.error_clicked, bgcolor=ft.colors.RED_900,
        )

        self.progress_bar = ft.Column([ ft.Text("Status : Unstarted"), ft.ProgressBar(value=0, bar_height=5, color=ft.colors.GREEN_600)])

        self.check_box = ft.Checkbox(label="Select all songs", on_change=self.checkbox_changed, value=True)

        self.clear_btn = ft.TextButton(
            "Clear",
            icon="DELETE_FOREVER_ROUNDED",
            icon_color="pink600", 
            visible=False, 
            on_click=self.clear_error_songs,
            style=ft.ButtonStyle(color={ft.MaterialState.DEFAULT: ft.colors.WHITE,}),
        )

        #search zone
        self.search_field = ft.TextField(label="Search", on_focus=self.search_f, on_blur=self.search_b, on_change=self.search_c, expand=True,)
        self.search_icon = ft.Icon(ft.icons.SEARCH, opacity=0.5, expand=True,)
        self.search_drop_down = ft.Dropdown(
            value="Song - Artist",
            options=[
                    ft.dropdown.Option("Song - Artist"),
            ],
            width=135,
            expand=False,
            on_change=self.dropdown_change,
        )
        
        self.search_bar = ft.Stack(
            [
                ft.Container(
                    content=self.search_icon,
                    alignment=ft.alignment.center_right,
                    padding=16,
                    expand=True,
                ),
                self.search_field,
                
            ],
            width=300,
            
        )
        

        #print("data :", self.data)

        # application's root control (i.e. "view") containing all other controls
        return ft.Container(content=ft.Column(
            controls=[
                ft.Row(),
                ft.Row(
                    controls=[
                        self.back_btn,
                        self.download_btn,
                        self.downloaded_songs_btn,
                        self.errors_btn,
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
                        self.clear_btn,
                        self.search_bar, 
                        self.search_drop_down,
                    ],
                ),
                self.progress_bar,
                self.tasks,
            ],
        ),
        padding=50
        )

    def dropdown_change(self, e):
            to_search = self.search_field.value.replace('  ', '')
            to_search_type = self.search_drop_down.value
            if self.data_type == "normal":
                self.page.clean()
                self.page.add(self)
                self.Load_data(None)
                self.page.update()
                self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
                self.update()
                
                song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(e))
                song_download_thread.daemon = True
                song_download_thread.start()
            else:
                self.page.clean()
                self.page.add(self)
                self.Load_data(None)
                self.page.update()
                self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
                self.update()

                title_text = self.controls[0].content.controls[2].controls[0]
                title_text.value = f"{self.data['playlist_name']} [error] ({len(self.data['error_tracks'])} song)"
                title_text.update()

                self.errors_btn.icon = ft.icons.MUSIC_NOTE
                self.errors_btn.bgcolor = ft.colors.TEAL
                self.errors_btn.update()

                self.clear_btn.visible = True
                self.clear_btn.update()
                
                song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(e))
                song_download_thread.daemon = True
                song_download_thread.start() 

            #self.search_field.value = to_search
            self.search_field.update()
            self.search_drop_down.value = to_search_type
            self.search_drop_down.update()

    def search_f(self, e):
        self.search_bar.width=None
        self.search_icon.opacity=1
        self.search_bar.expand = True
        self.search_field.update()
        self.search_bar.update()
        self.search_icon.update()
       
    def search_b(self, e):
        self.search_bar.width=300
        self.search_icon.opacity=0.5
        self.search_bar.expand = False
        self.search_field.update()
        self.search_bar.update()
        self.search_icon.update()
    
    def search_c(self, e):
        value = self.search_field.value
        value = value.replace(' ','')
        if self.search_drop_down.value == "Song - Artist":
            self.search_c_song_artist(e, value)
        elif self.search_drop_down.value == "User Name":
            self.search_c_user_name(e , value)
        
    def search_c_song_artist(self, e, value):
        if value != '':
            if self.data_type == "normal":
                to_search = self.search_field.value.replace('  ', '')
                to_search_type = self.search_drop_down.value
                self.load_search(e, to_search)
                self.search_field.value = to_search
                self.search_field.update()
                self.search_field.focus()
                self.search_drop_down.value = to_search_type
                self.search_drop_down.update()
            else:
                to_search = self.search_field.value.replace('  ', '')
                to_search_type = self.search_drop_down.value
                self.load_search(e, to_search)
                self.search_field.value = to_search
                self.search_field.update()
                self.search_field.focus()
                self.search_drop_down.value = to_search_type
                self.search_drop_down.update()

                title_text = self.controls[0].content.controls[2].controls[0]
                title_text.value = f"{self.data['playlist_name']} [error] ({len(self.data['error_tracks'])} song)"
                title_text.update()

                self.errors_btn.icon = ft.icons.MUSIC_NOTE
                self.errors_btn.bgcolor = ft.colors.TEAL
                self.errors_btn.update()

                self.clear_btn.visible = True
                self.clear_btn.update()


        else:
            to_search = self.search_field.value.replace('  ', '')
            to_search_type = self.search_drop_down.value
            if self.data_type == "normal":
                self.page.clean()
                self.page.add(self)
                self.Load_data(None)
                self.page.update()
                self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
                self.update()
                
                song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(e))
                song_download_thread.daemon = True
                song_download_thread.start()
            else:
                self.page.clean()
                self.page.add(self)
                self.Load_data(None)
                self.page.update()
                self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
                self.update()

                title_text = self.controls[0].content.controls[2].controls[0]
                title_text.value = f"{self.data['playlist_name']} [error] ({len(self.data['error_tracks'])} song)"
                title_text.update()

                self.errors_btn.icon = ft.icons.MUSIC_NOTE
                self.errors_btn.bgcolor = ft.colors.TEAL
                self.errors_btn.update()

                self.clear_btn.visible = True
                self.clear_btn.update()
                
                song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(e))
                song_download_thread.daemon = True
                song_download_thread.start() 

            self.search_field.value = to_search
            self.search_field.update()
            self.search_drop_down.value = to_search_type
            self.search_drop_down.update()       

    def search_c_user_name(self, e, value):
        print("heehy\nhh")
        pass

    def load_search(self, e, to_search):
        if self.data_type == "normal":
            self.load_search_fun(e, to_search)
        else:
            self.load_search_fun(e, to_search)
        
    def load_search_fun(self, e, to_search):
        self.page.clean()
        self.page.add(self)
        self.load_search_data(None, to_search)
        self.page.update()
        self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
        self.update()
            
        song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(e))
        song_download_thread.daemon = True
        song_download_thread.start()

    def load_search_data(self, e, to_search):
        song_download_thread = threading.Thread(target=lambda : self.Load_search_data_fun(e, to_search))
        song_download_thread.daemon = True
        song_download_thread.start()

    def Load_search_data_fun(self, instance, to_search):
        #print(self.data)
        if self.data_type == 'normal':
            for _ in self.data["playlist_tracks"]:
                if to_search.lower() in _.lower():
                    self.add_clicked(_, None)
        
        if self.data_type == 'error':
            for _ in self.data["error_tracks"]:
                if to_search.lower() in _.lower():
                    self.add_clicked(_, None)
                

                #print(len(content))
                #print(f"Content of {shb_file}:\n{content}")
                # Your code here
                #print("Function executed on app start")

    def add_clicked(self, data, e):
        self.task = SongListItem(self.task_delete, data, self.page, self.change_check_box_state)
        self.tasks.controls.append(self.task)  # Append task to the tasks Column
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def Load_data_fun(self, instance):
        #print(self.data)
        if self.data_type == 'normal':
            for _ in self.data["playlist_tracks"]:
                self.add_clicked(_, None)
        
        if self.data_type == 'error':
            for _ in self.data["error_tracks"]:
                self.add_clicked(_, None)
                

                #print(len(content))
                #print(f"Content of {shb_file}:\n{content}")
                # Your code here
                #print("Function executed on app start")

    def Load_data(self, instance):
        song_download_thread = threading.Thread(target=lambda : self.Load_data_fun(instance))
        song_download_thread.daemon = True
        song_download_thread.start()

    def reload(self, instance):
        if self.data_type == "normal":
            self.reload_fun(instance)
        else:
            self.reload_error_fun(instance)

    def reload_fun(self, instance):
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

    def reload_error_fun(self, instance):
        if self.load_btn.icon != ft.icons.KEYBOARD_ARROW_UP:
            self.page.clean()
            self.page.add(self)
            self.Load_data(None)
            self.page.update()
            self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
            self.update()

            title_text = self.controls[0].content.controls[2].controls[0]
            title_text.value = f"{self.data['playlist_name']} [error] ({len(self.data['error_tracks'])} song)"
            title_text.update()

            self.errors_btn.icon = ft.icons.MUSIC_NOTE
            self.errors_btn.bgcolor = ft.colors.TEAL
            self.errors_btn.update()

            self.clear_btn.visible = True
            self.clear_btn.update()
            
            song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(instance))
            song_download_thread.daemon = True
            song_download_thread.start()
        else:
            self.page.clean()
            self.page.add(self)
            self.page.update()
            self.load_btn.icon = ft.icons.KEYBOARD_ARROW_DOWN
            self.update()

            title_text = self.controls[0].content.controls[2].controls[0]
            title_text.value = f"{self.data['playlist_name']} [error] ({len(self.data['error_tracks'])} song)"
            title_text.update()

            self.errors_btn.icon = ft.icons.MUSIC_NOTE
            self.errors_btn.bgcolor = ft.colors.TEAL
            self.errors_btn.update()

            self.clear_btn.visible = True
            self.clear_btn.update()
            
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

        # Replace invalid characters
        new_file_path = new_file_path.replace("<", "").replace(">", "")
        # Replace spaces and other invalid characters
        new_file_path = new_file_path.replace(" ", "_").replace(":", "-")

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

            # Replace invalid characters
            to_del_file_path = to_del_file_path.replace("<", "").replace(">", "")
            # Replace spaces and other invalid characters
            to_del_file_path = to_del_file_path.replace(" ", "_").replace(":", "-")

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
       
        # Replace invalid characters
        folder_path = folder_path.replace("<", "").replace(">", "")
        # Replace spaces and other invalid characters
        folder_path = folder_path.replace(" ", "_").replace(":", "-")
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


        total_songs = len(songs)
        downloaded_songs = 0
        self.progress_bar.controls[0].value = "Status : Started"
        self.progress_bar.controls[1].value = 0
        self.progress_bar.controls[1].color = ft.colors.GREEN_700
        self.progress_bar.update()


        response = ""
        for song in songs:
            try:
                progress = (downloaded_songs / total_songs)
            except:
                progress = 0
            
            try_var = True
            try:
                self.progress_bar.controls[0].value = f"Status : Downloading : {int(progress*100)}% ( {downloaded_songs}/{total_songs} ) : {song}"
                self.progress_bar.update()

                data = YtbSearch.Search2(song)
                #print(data)

                video_id = data["video_id"]

                # List all files in the folder
                files = os.listdir(folder_path)
                #print("files :", files)
                #print("hhhhhhh")

                # Filter files that end with ".shb"
                titles = [file for file in files if file.endswith(".mp3")]
                        
                ytb_to_mp3 = YtbToMp3(video_id, titles, folder_path)
                #print("hhhhhhh")
                response = ytb_to_mp3.Download()
                #print("res :", response)
                        
                downloaded_songs += 1
                progress = (downloaded_songs / total_songs)
                self.progress_bar.controls[1].value = progress
                self.progress_bar.update()
                try_var = False

                if response == "free plan":
                    break

            except Exception as e:
                print(e)
                pass
                break

        #print("res :", response)

        if response == "free plan":
            self.progress_bar.controls[0].value = f"Status : Error (max songs reached for today) : {int(progress*100)}% ( {downloaded_songs}/{total_songs} ) : {song}"
            self.progress_bar.controls[1].color = ft.colors.RED
            self.progress_bar.update()
        elif response == "error":
            self.progress_bar.controls[0].value = f"Status : Error (Unknown) : {int(progress*100)}% ( {downloaded_songs}/{total_songs} ) : {song}"
            if downloaded_songs > 0:
                self.progress_bar.controls[1].color = ft.colors.RED
            else:
                self.progress_bar.controls[1].bgcolor = ft.colors.RED
            self.progress_bar.update()
            self.error_songs_fill(songs, downloaded_songs, total_songs)
        elif response == "done":
            self.progress_bar.controls[1].color = ft.colors.GREEN_600
            self.progress_bar.update()
        else:
            self.progress_bar.controls[0].value = f"Status : Error (Unknown) : {int(progress*100)}% ( {downloaded_songs}/{total_songs} ) : {song}"
            if downloaded_songs > 0:
                self.progress_bar.controls[1].color = ft.colors.RED
            else:
                self.progress_bar.controls[1].bgcolor = ft.colors.RED
            self.progress_bar.update()
            self.error_songs_fill(songs, downloaded_songs, total_songs)




                
        
        if downloaded_songs == total_songs:
            self.progress_bar.controls[0].value = f"Status : Completed ( {downloaded_songs}/{total_songs} songs downloaded )"
            self.progress_bar.controls[1].value = 1
            self.progress_bar.update()
            if downloaded_songs > 0:
                self.open_songs_folder(e)

    def error_songs_fill(self, songs, downloaded_songs, total_songs):
        exp = False
        for i in range(downloaded_songs, total_songs):
            song = songs[i]
            if song not in self.data['error_tracks']:
                exp = True
                self.data['error_tracks'].append(song)

        if exp:
            folder_path = "./data"  # Replace with the actual path to your folder


            file_name = f"Spotify Data ({self.data['date']}).shb"
            new_file_path = os.path.join(folder_path, file_name)

            # Replace invalid characters
            new_file_path = new_file_path.replace("<", "").replace(">", "")
            # Replace spaces and other invalid characters
            new_file_path = new_file_path.replace(" ", "_").replace(":", "-")

            data_t = []
            data_t.append(self.data)

            with open(new_file_path, "wb") as file:
                pickle.dump(data_t, file)

    def open_songs_folder(self, e):
        folder_name = f"Spotify songs - {self.data['playlist_name']} - ({self.data['date']})"

        current_dir = os.getcwd()

        # Replace invalid characters
        folder_name = folder_name.replace("<", "").replace(">", "")
        # Replace spaces and other invalid characters
        folder_name = folder_name.replace(" ", "_").replace(":", "-")

        folder_path = os.path.join(current_dir, "output", folder_name)
        
        #print(folder_name)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            if os.name == 'nt':
                subprocess.Popen(['explorer', folder_path])
        else:
            #print(f"Folder not found: {folder_path}")
            pass
        
        #folder_path = f"./output/Spotify songs - {self.data['playlist_name']} - ({self.data['date']})"

    def error_load(self, e):
        self.page.clean()
        self.page.add(self)
        self.Load_data(None)
        self.page.update()
        self.load_btn.icon = ft.icons.KEYBOARD_ARROW_UP
        self.update()
                
        song_download_thread = threading.Thread(target=lambda : self.load_check_box_data(e))
        song_download_thread.daemon = True
        song_download_thread.start()

    def error_clicked(self, e):
        if self.data_type == "normal":
            self.data_type = "error"
            self.error_load(e)
            title_text = self.controls[0].content.controls[2].controls[0]
            title_text.value = f"{self.data['playlist_name']} [error] ({len(self.data['error_tracks'])} song)"
            title_text.update()

            self.errors_btn.icon = ft.icons.MUSIC_NOTE
            self.errors_btn.bgcolor = ft.colors.TEAL
            self.errors_btn.update()

            self.clear_btn.visible = True
            self.clear_btn.update()
        else:
            self.data_type = "normal"
            self.error_load(e)
            title_text = self.controls[0].content.controls[2].controls[0]
            title_text.value = f"{self.data['playlist_name']} ({len(self.data['playlist_tracks'])} song)"
            title_text.update()

            self.errors_btn.icon = ft.icons.ERROR_OUTLINE_OUTLINED
            self.errors_btn.bgcolor = ft.colors.RED_900
            self.errors_btn.update()

            self.clear_btn.visible = False
            self.clear_btn.update()

    def clear_error_songs(self, e):
        
        self.data['error_tracks'].clear()

        folder_path = "./data"  # Replace with the actual path to your folder


        file_name = f"Spotify Data ({self.data['date']}).shb"
        new_file_path = os.path.join(folder_path, file_name)

        # Replace invalid characters
        new_file_path = new_file_path.replace("<", "").replace(">", "")
        # Replace spaces and other invalid characters
        new_file_path = new_file_path.replace(" ", "_").replace(":", "-")

        data_t = []
        data_t.append(self.data)

        with open(new_file_path, "wb") as file:
            pickle.dump(data_t, file)
            
        self.reload(e)

def main(page: ft.Page):

    def maximize_win(e):
        page.window_maximized = not page.window_maximized
        if page.window_maximized:
            min_max_win_btn.icon = ft.icons.CONTENT_COPY
            min_max_win_btn.update()
        else:
            min_max_win_btn.icon = ft.icons.CROP_SQUARE
            min_max_win_btn.update()
        page.update()
    
    def hide_win(e):
        page.window_minimized = not page.window_minimized
        page.update()

    page.title = "Spotipy"
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"
    page.window_left = 400
    page.window_top = 200
    page.window_frameless = False
    page.window_title_bar_hidden = True
    page.spacing = 0
    page.theme_mode = (ft.ThemeMode.DARK)

    page.update()

    if not os.path.exists("./data"):
        os.makedirs("data")

    
    hide_win_btn = ft.IconButton(ft.icons.HORIZONTAL_RULE, icon_size=15, icon_color="white", on_click=hide_win)
    min_max_win_btn = ft.IconButton(ft.icons.CROP_SQUARE, icon_color="white", icon_size=15, on_click=maximize_win)
    close_win_btn = ft.IconButton(ft.icons.CLOSE, icon_color="white", icon_size=15, on_click=lambda e: page.window_close(), style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED_ACCENT_200,},))

    img = ft.Image(src=f"./assets/favicon.png", fit=ft.ImageFit.COVER, repeat=ft.ImageRepeat.NO_REPEAT,)

    app_br = ft.AppBar(
        leading=ft.WindowDragArea(content=ft.Container(content=img, margin=10)),
        title=ft.WindowDragArea(content=ft.Text("Spotipy", size=30)),
        center_title=True,
        bgcolor=ft.colors.GREY_900,
        actions=[ft.WindowDragArea(content=ft.Row([hide_win_btn, min_max_win_btn, close_win_btn,]))]
    )    
    
    page.appbar = app_br

    page.update()

    app = MyApp(page)

    page.add(app)
    
    page.update()
    
    app.Load_data(None)
    
    #flet pack gui_app10.py --name Spotipy --icon favicon.png

ft.app(target=main, assets_dir="assets")


