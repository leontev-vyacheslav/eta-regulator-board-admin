from datetime import datetime
from typing import List
import flet as ft
from controls.access_token_dialog import AccessTokenDialog
from controls.regulator_device_edit_dialog import RegulatorDeviceEditDialog

from models.regulator_device_model import RegulatorDeviceModel

class RegulatorDeviceListView(ft.ListView):

    def __init__(self, ref: ft.Ref, page: ft.Page, devices: List[RegulatorDeviceModel] = []):
        self.page = page

        self.name = 'app_list_view'
        super().__init__(
            ref=ref,
            expand=True,
            spacing=10,
            padding=10,
            controls=self._get_items()
        )

    def update(self):
        self.clean()
        self.controls = self._get_items()

        return super().update()

    def _show_access_token_dialog(self, device: RegulatorDeviceModel):
        self.page.dialog = AccessTokenDialog(self.page, device)
        self.page.dialog.open = True
        self.page.update()

    def _show_regulator_device_edit_dialog(self, device: RegulatorDeviceModel):
        self.page.dialog = RegulatorDeviceEditDialog(self.page, device)
        self.page.dialog.open = True
        self.page.update()


    def _get_items(self):
        devices = self.page.client_storage.get('devices')
        devices = [RegulatorDeviceModel(
            id=i['id'],
            name=i['name'],
            mac_address=i['mac_address'],
            master_key=i['master_key'],
            creation_date=datetime.fromisoformat(i['creation_date']),
        ) for i in devices] if devices is not None else []
        pass

        list_items = [
            ft.ListTile(
                leading=ft.Icon(ft.icons.DEVICES),
                title=ft.Text(f'{index + 1}. {device.name}',  no_wrap=True),
                trailing=ft.PopupMenuButton(
                    icon=ft.icons.MORE_VERT,
                    items=[
                        ft.PopupMenuItem(
                            icon=ft.icons.EDIT,
                            text='Edit device',
                            on_click=lambda e: self._show_regulator_device_edit_dialog(e.control.data),
                            data=device
                        ),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            icon=ft.icons.KEY_OUTLINED,
                            text='Generate access token',
                            on_click=lambda e: self._show_access_token_dialog(e.control.data),
                            data=device
                        )
                    ],
                ),
                on_click=lambda e: print(e.control.data),
                data=device
            )
            for index, device in enumerate(devices)
        ]

        return list_items
