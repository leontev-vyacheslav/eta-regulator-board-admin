import flet as ft
from flet import TextField
from flet_core.control_event import ControlEvent

from controls.drawer import Drawer
from controls.page_title import PageTitle


def main(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.theme_mode = ft.ThemeMode.DARK
    page.drawer = Drawer(page)

    page.add(
        ft.Row(
            controls=[
                PageTitle(page=page, title='ETA RegulatorBoard Admin')
            ],
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )

    page.theme_mode = ft.ThemeMode.DARK


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets', view=ft.AppView.FLET_APP )
