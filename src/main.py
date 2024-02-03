import flet as ft

from controls.drawer import Drawer
from controls.page_title import PageTitle
from controls.regulator_device_list_view import RegulatorDeviceListView
import random
import uuid

from models.regulator_device_model import RegulatorDeviceModel


def main(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.window_width = 1024
    page.window_min_width = 640
    page.window_max_width = 1024

    page.client_storage.remove('devices')
    if page.client_storage.get('devices') is None:
      page.client_storage.set('devices', [
          RegulatorDeviceModel(
              id=uuid.uuid4().__str__(),
              name='omega-8f79',
              mac='40:a3:6b:c9:8f:7b',
              master_key='XAMhI3XWj+PaXP5nRQ+nNpEn9DKyHPTVa95i89UZL6o='
            )
      ])


    if page.client_storage.get('theme_mode'):
        page.theme_mode = ft.ThemeMode(page.client_storage.get('theme_mode'))
    else:
        page.client_storage.set('theme_mode', page.theme_mode.value)

    page.drawer = Drawer(page)

    page.add(
        ft.Row(
            controls=[
                PageTitle(page=page, title='ETA RegulatorBoard Admin')
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        ft.Row(
            controls=[
                RegulatorDeviceListView(page=page)
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets', view=ft.AppView.FLET_APP )
