from typing import List
import flet as ft
from controls.generated_access_token_dialog import GeneratedAccessTokenDialog

from models.regulator_device_model import RegulatorDeviceModel

class RegulatorDeviceListView(ft.ListView):

    def __init__(self, page: ft.Page, devices: List[RegulatorDeviceModel] = []):
        self.page = page
        super().__init__(
            expand=True,
            spacing=10,
            padding=10,
            controls=self.__get_items()
        )


    def __show_dialog(self, device: RegulatorDeviceModel):
        self.page.dialog = GeneratedAccessTokenDialog(self.page, device)
        self.page.dialog.open = True
        self.page.update()


    def __get_items(self):
        devices = self.page.client_storage.get('devices')
        devices = [RegulatorDeviceModel(**i) for i in devices] if devices is not None else []

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
                            on_click=lambda e: self.__show_dialog(e.control.data),
                            data=device
                        ),
                    ],
                ),
                on_click=lambda e: print(e.control.data),
                data=device
            )
            for index, device in enumerate(devices)
        ]

        return list_items
