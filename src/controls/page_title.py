import flet as ft


class PageTitle(ft.Container):
    def __init__(self, page: ft.Page, title: str):
        super().__init__()

        self.page = page

        self.title = title
        self.content = ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.MENU,
                        on_click=self.__show_drawer
                    ),
                    ft.WindowDragArea(ft.Container(
                            ft.Text(self.title, color='#ff5722', weight=ft.FontWeight.BOLD, size=18, no_wrap=True),
                            padding=10
                        ),
                        expand=True
                    ),
                    ft.IconButton(
                        ft.icons.CLOSE,
                        on_click=lambda _: self.__close_window()
                    )
                ]
            )
        self.expand = True

    def __close_window(self):
        def __close_alert_dialog():
            self.page.dialog.open = False
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            open=True,
            modal=True,
            title=ft.Text('Confirm'),
            content=ft.Row(
                controls=[
                    ft.Text('Do you really want to close the application?' ),
                ], width=450
            ),
            actions=[
                ft.ElevatedButton('OK', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), bgcolor='#ff5722', color='white'), on_click=lambda _: self.page.window_close(), width=100, height=35),
                ft.ElevatedButton('CANCEL', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=lambda _: __close_alert_dialog(), width=120, height=35),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.update()


    def __show_drawer(self, e):
        self.page.drawer.open = True
        self.page.drawer.update()

