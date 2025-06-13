import flet as ft


class Session(ft.UserControl):
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ALBUM, size=60),
                            title=ft.Text(
                                "All PlayLists", 
                                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                weight=ft.FontWeight.W_400,
                            ),
                            subtitle=ft.Text(
                                "user : Mohamed Abidi \nDate : 2023-08-16 06-50-23",
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
        self.task_delete(self)

    def access_clicked(self, e):
        self.display_task.text = "fgh"
        session_title = self.display_task.content.content.controls[0].title.value
        session_subtitle = self.display_task.content.content.controls[0].subtitle.value
        print(session_title)
        print(session_subtitle)

        username = session_subtitle.split("\n")[0].split(":")[1].strip()

        date = session_subtitle.split("\n")[1].split(":")[1].strip()
        self.update()


class MyApp(ft.UserControl):
    def build(self):
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.tasks,
            ],
        )

    def add_clicked(self, e):
        task = Session(self.new_task.value, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()


def main(page: ft.Page):
    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    page.update()

    # create application instance
    app = MyApp()

    # add application's root control to the page
    page.add(app)


ft.app(target=main)


