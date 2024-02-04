import base64
import os
import re
import uuid
import flet as ft

from models.regulator_device_model import RegulatorDeviceModel

class RegulatorDeviceEditDialog(ft.AlertDialog):

    def __init__(self, page: ft.Page, device: RegulatorDeviceModel):
        self.page = page
        super().__init__()
        self.id_text_field_ref = ft.Ref[ft.TextField]()
        self.name_text_field_ref = ft.Ref[ft.TextField]()
        self.mac_address_text_field_ref = ft.Ref[ft.TextField]()
        self.master_key_text_field_ref = ft.Ref[ft.TextField]()

        self.device = device
        self.shape = ft.RoundedRectangleBorder(radius=5)
        self.title = ft.Text(f'Regulator device')
        self.modal = True
        self.expand = False
        self.content = ft.Column(controls=[
            ft.Row(
                controls=[
                    ft.TextField(
                        ref=self.id_text_field_ref,
                        read_only=True,
                        suffix=ft.IconButton(ft.icons.REFRESH, on_click=lambda _: self.__refresh_uuid()),
                        label=f'ID',
                        expand=True,
                        value=self.device.id,
                    ),
                ],
                width=640,
                expand=True
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        ref=self.name_text_field_ref,
                        label=f'Name',
                        expand=True,
                        value=self.device.name,
                    ),
                ],
                expand=True
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        ref=self.mac_address_text_field_ref,
                        label=f'MAC address',
                        expand=True,
                        on_change=lambda e: self.__on_mac_address_text_field_change(e),
                        value=self.device.mac_address,
                    ),
                ],
                expand=True
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        ref=self.master_key_text_field_ref,
                        label=f'Master Key',
                        expand=True,
                        suffix=ft.IconButton(ft.icons.REFRESH, on_click=lambda _: self.__refresh_master_key()),
                        value=self.device.master_key,
                    ),
                ],
                expand=True
            ),
        ], tight=True, height=320)

        self.actions=[
            ft.ElevatedButton('ADD', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=lambda _: self.__add_device(), width=100, height=35),
            ft.ElevatedButton('CLOSE', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=lambda _: self.__close_dlg(), width=100, height=35),
        ]

        self.actions_alignment=ft.MainAxisAlignment.END
        self.open = True

    def __refresh_uuid(self):
        self.id_text_field_ref.current.value = uuid.uuid4().__str__( )
        self.id_text_field_ref.current.update()


    def __close_dlg(self):
        self.open = False
        self.page.update()


    def __refresh_master_key(self):
        self.master_key_text_field_ref.current.value = base64.b64encode(os.urandom(32)).decode('utf-8')
        self.master_key_text_field_ref.current.update()


    def __on_mac_address_text_field_change(self, e):
        cleaned_value = re.sub(r'[^a-fA-F0-9]', '', e.control.value)
        formatted_value = ':'.join( re.findall(r'.{1,2}', cleaned_value)[0:6])

        e.control.value = formatted_value;
        e.control.update()


    def __add_device(self):
        devices = self.page.client_storage.get('devices')
        devices = [RegulatorDeviceModel(**i) for i in devices] if devices is not None else []

        self.device.id = self.id_text_field_ref.current.value
        self.device.name = self.name_text_field_ref.current.value
        self.device.mac_address = self.mac_address_text_field_ref.current.value

        devices.append(self.device)
        self.page.client_storage.set('devices', devices)

        self.open = False
        self.page.update()