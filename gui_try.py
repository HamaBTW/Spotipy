import flet as ft

 
 
def main(page: ft.Page):
    page.window_frameless = False
    page.window_title_bar_hidden = True
    page.spacing = 0
    page.padding = 0
    # DETECT WIDTH
    widthsrc = page.window_width

    page.scroll = "adaptive"
 
    def maximize_win(e):
        # docs: https://flet.dev/docs/controls/page#window_maximized
        page.window_maximized = not page.window_maximized
        page.update()
 
    page.add(
        ft.ResponsiveRow([
            ft.WindowDragArea(
                ft.Container(
                    width=widthsrc,
                    bgcolor="blue",
                    padding=15,
                    content=ft.Row([
                        ft.Text("MyHome", size=30, color="white"),
                        ft.Container(content=ft.Row([
                            ft.IconButton(ft.icons.CHECK_BOX_OUTLINE_BLANK, icon_color="white",
                                       on_click=maximize_win),
                            ft.IconButton(ft.icons.CLOSE, icon_color="white",
                                       on_click=lambda e: page.window_close()),
                        ]))
                    ], alignment="spaceBetween")
                ),
            )
        ])
    )

    app_a = ft.Column(controls=[], scroll = "AUTO")

    for i in "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff":
        app_a.controls.append(ft.Text("fff"))
    
    page.add(app_a)
    app_a.update()

    
 
 
ft.app(target=main)