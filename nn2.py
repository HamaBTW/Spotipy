
import flet as ft
 
 
def main(page:ft.Page):
	# REMOVE SPACING AND PADDING PAGE
	page.spacing = 0
	page.padding = 0
 
	# SET ANIMATION WHEN OPEN AND CLOSE
 
	def showdialog(e):
		modal.opacity = 1 if modal.opacity == 0 else 0
 
		dialog.offset = ft.transform.Offset(0,0) if modal.opacity == 1 else ft.transform.Offset(0,2)
 
		page.update()
 
 
 
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
		on_click=showdialog
 
			)
 
		])
 
	# CREATE YOU DIALOG
	dialog = ft.Container(
		bgcolor="white",
		border_radius=30,
		margin=ft.margin.only(top=80,left=30,right=30),
		height=200,
		alignment=ft.alignment.center,
		content=ft.Text("i am is dialog you",
			size=20,
			color="black"
			),
		# SET EFFECT SLIDE UP FOR YOU DIALOG
		offset=ft.transform.Offset(0,2),
		animate_offset=ft.animation.Animation(duration=300,curve="easeIn")
 
		)
 
	modal = ft.Container(content=ft.Stack([bgDialog,dialog]), opacity=0, animate_opacity=300)
 
    
    page.add(
		ft
		#modal,
	  )
 
 
 
ft.app(target=main)