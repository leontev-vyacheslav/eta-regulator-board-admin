import flet as ft


class PageTitle(ft.Container):
    def __init__(self, page: ft.Page, title: str):
        super().__init__()
        self.title = title
        self.page = page
        self.content = ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.MENU,
                        on_click=self.__show_drawer
                    ),
                    ft.WindowDragArea(ft.Container(
                            ft.Text(self.title, color='#ff5722', weight=ft.FontWeight.BOLD, size=18),
                            padding=10
                        ),
                        expand=True
                    ),
                    ft.IconButton(
                        ft.icons.CLOSE,
                        on_click=lambda _: self.page.window_close()
                    )
                ]
            )
        self.expand = True

    def __show_drawer(self, e):
        self.page.drawer.open = True
        self.page.drawer.update()

