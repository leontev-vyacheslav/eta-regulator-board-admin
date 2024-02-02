import random
from uuid import uuid4 as uuid
import flet as ft

from controls.drawer import Drawer
from controls.page_title import PageTitle
from models.regulator_device_model import RegulatorDeviceModel


def main(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    if page.client_storage.get('theme_mode'):
        page.theme_mode = ft.ThemeMode(page.client_storage.get('theme_mode'))

    # page.theme_mode = ft.ThemeMode.LIGHT

    page.drawer = Drawer(page)
    page.window_width = 1024
    page.window_min_width = 640
    page.window_max_width = 1024

    list_items = [
        ft.ListTile(
            leading=ft.Icon(ft.icons.DEVICES),
            title=ft.Text(f'{index + 1}. {device.name}',  no_wrap=True),
            trailing=ft.PopupMenuButton(
                icon=ft.icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(
                        icon=ft.icons.KEY_OUTLINED,
                        text='Generate operation key',
                        on_click=lambda e: print(f'{e.control.data}'),
                        data=device
                    ),
                ],
            ),
            on_click=lambda e: print(e.control.data),
            data=device
        )
        for index, device in enumerate([RegulatorDeviceModel(id=uuid().__str__(), name=f'Omega-{random.randint(1000, 9999)}', mac='') for _ in range(50)])
    ]

    page.add(
        ft.Row(
            controls=[
                PageTitle(page=page, title='ETA RegulatorBoard Admin')
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        ft.Row(
            controls=[
                ft.ListView(controls=list_items, height=500, expand=True, spacing=10, padding=10)
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )

    page.theme_mode = ft.ThemeMode.DARK


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets', view=ft.AppView.FLET_APP )
