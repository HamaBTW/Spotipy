import flet as ft
 
 
def main(page: ft.Page):
    page.window_frameless = False
    page.window_title_bar_hidden = True
    page.spacing = 0
    page.padding = 0
    # DETECT WIDTH
    widthsrc = page.window_width
 
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

    hide_win_btn = ft.IconButton(ft.icons.HORIZONTAL_RULE, icon_size=15, icon_color="white", on_click=hide_win)
    min_max_win_btn = ft.IconButton(ft.icons.CROP_SQUARE, icon_color="white", icon_size=15, on_click=maximize_win)
    close_win_btn = ft.IconButton(ft.icons.CLOSE, icon_color="white", icon_size=15, on_click=lambda e: page.window_close(), style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED_ACCENT_200,},))

    bar1 = ft.ResponsiveRow([
            ft.WindowDragArea(
                ft.Container(
                    width=widthsrc,
                    bgcolor=ft.colors.GREY_900,
                    padding=5,
                    content=ft.Row([
                        ft.Text("MyHome", size=15, color="white"),
                        ft.Container(content=ft.Row([
                           hide_win_btn,
                           min_max_win_btn,
                           close_win_btn,
                        ]))
                    ], alignment="spaceBetween")
                ),
            )
        ])

    app_bar_items = ft.WindowDragArea(content=ft.Row(controls=[hide_win_btn, min_max_win_btn, close_win_btn,]))
    img = ft.Image(
                src=f"./img.png",
                fit=ft.ImageFit.COVER,
                repeat=ft.ImageRepeat.NO_REPEAT,
            )
    
    app_br = ft.AppBar(
        leading=ft.WindowDragArea(content=ft.Container(content=img, margin=10)),
        title=ft.WindowDragArea(content=ft.Text("AppBar Example",)),
        center_title=True,
        bgcolor=ft.colors.GREY_900,
        actions=[
            app_bar_items
        ],
    )

    page.appbar = app_br
    
    
    page.add(ft.Text("Display Large", style=ft.TextThemeStyle.DISPLAY_LARGE),)
 
 
ft.app(target=main)