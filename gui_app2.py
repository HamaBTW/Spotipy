import flet as ft


class Session(ft.UserControl):
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Container(
            content=ft.Row(
                expand=True,
                controls=[
                    ft.FilledButton(
                        text=self.task_name,
                        disabled=True,
                        style=ft.ButtonStyle(
                            color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                            bgcolor={"": ft.colors.YELLOW}
                        ),
                        expand=True,
                    ),
                    ft.FilledButton(
                        text=self.task_name,
                        disabled=True,
                        style=ft.ButtonStyle(
                            color={ft.MaterialState.DEFAULT: ft.colors.BLACK},
                            bgcolor={"": ft.colors.YELLOW}
                        ),
                        expand=True,
                    ),
                ],
            ),
            expand=True
        )
        
        self.display_view = ft.Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            ft.icons.ARROW_CIRCLE_RIGHT_OUTLINED,
                            tooltip="Access",
                            on_click=self.access_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        return ft.Column(controls=[self.display_view])

    def delete_clicked(self, e):
        self.task_delete(self)

    def access_clicked(self, e):
        self.display_task.text = "fgh"
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


