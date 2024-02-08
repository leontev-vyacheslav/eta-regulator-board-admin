import flet as ft
from flet_core.margin import Margin
from flet_core.alignment import Alignment

from utils.debugging import is_debug


class DrawerHeader(ft.Container):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.margin = Margin(right=10, top=10, left=0, bottom=0)

        self.content=ft.Row(
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            height=60,
                            alignment=Alignment(-1, 0),
                            content=ft.Row(controls=[
                                ft.Image(src='src/assets/icon.ico' if is_debug() else  'assets/icon.ico'),
                                ft.Divider(thickness=5, visible=True),
                                ft.Text(
                                    'ETA24™',
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color='#ff5722',
                                    no_wrap=True
                                )
                            ], expand=True),
                            padding=0,
                            margin=Margin(20, 0, 0, 0)
                        ),
                    ]
                ),
                ft.Column(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CLOSE_SHARP,
                            width=40,
                            height=40,
                            on_click=lambda _: self.__close_drawer()
                        ),
                    ]
                ),
            ]
        )


    def __close_drawer(self):
        self.page.drawer.open = False
        self.page.drawer.update()
