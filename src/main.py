from datetime import datetime, timedelta
import flet as ft

from controls.drawer import Drawer
from controls.page_title import PageTitle
from controls.regulator_device_list_view import RegulatorDeviceListView

from models.regulator_device_model import RegulatorDeviceModel


def main(page: ft.Page):

    page.theme = ft.Theme(color_scheme_seed=ft.colors.INDIGO)
    page.app_list_view = ft.Ref[ft.ListView]()

    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.window_width = 1024
    page.window_min_width = 640
    page.window_max_width = 1024

    # devices = page.client_storage.get('devices')
    # if devices is not None:

    #   devices = [RegulatorDeviceModel(
    #       id=d['id'],
    #       name=d['name'],
    #       mac_address=d['mac_address'],
    #       master_key=d['master_key'],
    #       creation_date=datetime.now()
    #     ) for d in devices]

    #   for i, d in enumerate(devices):
    #       d.creation_date = datetime.now() + timedelta(days=i)

    # page.client_storage.set('devices',
    #     [{
    #         'id': d.id,
    #         'name': d.name,
    #         'mac_address': d.mac_address,
    #         'master_key': d.master_key,
    #         'creation_date': d.creation_date.isoformat()
    #     }
    #     for d in devices])


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
                RegulatorDeviceListView(
                    ref=page.app_list_view,
                    page=page
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets', view=ft.AppView.FLET_APP )
