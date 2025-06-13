import pickle as pk
import flet as ft
import subprocess
import webbrowser
import os
 
 
def main(page : ft.Page):

	def load_web_app_data(f_name):
		#print(f_name)
		with open(f_name, "rb") as f:
			data = pk.load(f)
			return data

	def export_web_app_data(f_name):
		c_id = user_id.value
		c_sc = user_secret.value
		with open(f_name, "wb") as f:
			pk.dump({"client_id":str(c_id), "client_secret":str(c_sc)}, f)
		
		script2_process = subprocess.Popen(['Spotipy Web Connector.exe'])
		hidedialog(None)
        
	def showdialog(e):

		file_path = "./data"
		if not os.path.exists(file_path):
			os.makedirs(file_path)
		
		file_path = "./data/web app data.wbspy"
		
		if not os.path.exists(file_path):
			f = open(file_path, "wb")
			pk.dump({"client_id":"", "client_secret":""}, f)
			f.close()

		web_data = load_web_app_data(file_path)

		user_id.value = web_data['client_id']
		user_id.update()
		user_secret.value = web_data['client_secret']
		user_secret.update()
 
		page.update()

	def hidedialog(e):
		page.window_close()
		
		page.update()
		page.window_close()

	def show_hide_id(e):
		user_id.password = not user_id.password
		user_id_btn.icon_color=ft.colors.WHITE if user_id_btn.icon_color==ft.colors.GREEN else ft.colors.GREEN
		user_id_btn.update()
		user_id.update()
	
	def show_hide_secret(e):
		user_secret.password = not user_secret.password
		user_secret_btn.icon_color=ft.colors.WHITE if user_secret_btn.icon_color==ft.colors.GREEN else ft.colors.GREEN
		user_secret_btn.update()
		user_secret.update()

	def submit(e):
		ok = True
		if len(user_secret.value) != 32 or len(user_id.value) != 32:
			ok = False
		
		if len(user_id.value) != 32:
			user_id.error_text = "invalid format"
		else:
			user_id.error_text = ""
		user_id.update()

		if len(user_secret.value) != 32:
			user_secret.error_text = "invalid format"
		else:
			user_secret.error_text = ""
		user_secret.update()
		
		if ok:
			file_path = "./data/web app data.wbspy"
			export_web_app_data(file_path)

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

	def open_how_to(e):
		url = "https://spotipy-app.netlify.app/client-id-&-secret"
		webbrowser.open(url)

	page.window_left = 400
	page.window_top = 300
	page.window_width = 1000
	page.window_height = 180
	page.window_frameless = True
	page.window_title_bar_hidden = True
	page.title = "Spotipy"
	page.window_maximizable = False
	page.theme_mode = (ft.ThemeMode.DARK)
	page.window_always_on_top = True
	page.update()

	hide_win_btn = ft.IconButton(ft.icons.HORIZONTAL_RULE, icon_size=15, icon_color="white", on_click=hide_win)
	min_max_win_btn = ft.IconButton(ft.icons.CROP_SQUARE, icon_color="grey", icon_size=15, on_click=maximize_win, disabled=True)
	close_win_btn = ft.IconButton(ft.icons.CLOSE, icon_color="white", icon_size=15, on_click=lambda e: page.window_close(), style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED_ACCENT_200,},))

	img = ft.Image(src=f"./assets/favicon1.png", fit=ft.ImageFit.COVER, repeat=ft.ImageRepeat.NO_REPEAT,)

	app_br = ft.AppBar(
        leading=ft.WindowDragArea(content=ft.Container(content=img, margin=10), maximizable=False),
        title=ft.WindowDragArea(content=ft.Text("Spotipy", size=30), maximizable=False),
        center_title=True,
        bgcolor=ft.colors.GREY_900,
        actions=[ft.WindowDragArea(content=ft.Row([hide_win_btn, min_max_win_btn, close_win_btn,]), maximizable=False)]
    )    

	page.appbar = app_br

	page.update()

	user_id = ft.TextField(label="user id", expand=True, password=True, error_text="")
	user_id_btn = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, on_click=show_hide_id, icon_color=ft.colors.WHITE)
	user_secret = ft.TextField(label="user secret", expand=True, password=True, error_text="")
	user_secret_btn = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, on_click=show_hide_secret, icon_color=ft.colors.WHITE)
	go_btn = ft.FloatingActionButton(icon=ft.icons.ARROW_FORWARD, on_click=submit)
	how_to_btn = ft.FloatingActionButton(icon=ft.icons.QUESTION_MARK_OUTLINED, on_click=open_how_to)
	form = ft.Row(controls=[user_id, user_id_btn, user_secret, user_secret_btn, go_btn, how_to_btn])

	bgDialog = ft.ResponsiveRow([
		ft.Container(
		width=page.window_width,
		height=page.window_height,
		bgcolor="#000000",
		ink=False,
		# SET TRANSPARENT YOU BG DIALOG
		opacity=0.6,
		# THIS IS IF BG DIALOG IS CLICK
		# THEN CLOSE YOU DIALOG
		disabled=True,
 
			)
 
		])

	dialog = ft.Container(
		border_radius=30,
		margin=ft.margin.only(left=30,right=30),
		height=200,
		alignment=ft.alignment.center,
		content=form,
		# SET EFFECT SLIDE UP FOR YOU DIALOG
		offset=ft.transform.Offset(0,2),
		animate_offset=ft.animation.Animation(duration=300,curve="easeIn"),
		padding=ft.padding.only(left=50,right=50),
 
		)
 
	modal = ft.Container(content=ft.Stack([bgDialog,dialog]), opacity=0, animate_opacity=300)

	



 

	page.add(form)
	showdialog(None)
 
 
 

ft.app(target=main)
#flet pack "Spotipy Web Security.py" --name "Spotipy Web Security" --icon img2.png