from datetime import datetime, timedelta
import flet as ft

from models.regulator_device_model import RegulatorDeviceModel
from utils.encoding import create_access_token


class AccessTokenDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, device: RegulatorDeviceModel):

        self.page = page
        super().__init__()
        self.accessTokenTextFieldRef = ft.Ref[ft.TextField]()
        self.expirationTimeTextFieldRef = ft.Ref[ft.TextField]()
        self.device = device
        self.shape = ft.RoundedRectangleBorder(radius=5)
        self.title = ft.Text(f'Generate access token')
        self.modal = True
        self.expand = False
        self.content = ft.Column(controls=[
            ft.Row(
                controls=[
                    ft.TextField(
                        ref=self.expirationTimeTextFieldRef,
                        label=f'Expiration time',
                        read_only=True,
                        expand=True,
                        value=f'{(datetime.now() + timedelta(hours=8)):%d.%m.%Y %H:%M}',
                    ),
                ],
                expand=True
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        ref=self.accessTokenTextFieldRef,
                        label=f'Access Token',
                        expand=True,
                        value=self.__generate_access_token(),
                        read_only=True,

                        suffix=ft.Row(controls=[
                            ft.IconButton(ft.icons.REFRESH_OUTLINED,  on_click=lambda _: self.__refresh_access_token(), scale=0.9),
                            ft.IconButton(ft.icons.COPY, on_click=lambda _: self.__copy_to_clipboard(), scale=0.9),
                        ], alignment=ft.MainAxisAlignment.END, tight=True)
                    ),
                ],
                width=640,
                expand=True
            ),
        ], height=220)

        self.actions=[
            ft.ElevatedButton('CLOSE', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=lambda _: self.__close_dlg(), width=100, height=35),
        ]

        self.actions_alignment=ft.MainAxisAlignment.END

    def __generate_access_token(self):
        return create_access_token(self.device.mac_address, 8, self.device.master_key)


    def __close_dlg(self):
        self.open = False
        self.page.update()

    def __copy_to_clipboard(self):
        self.page.set_clipboard(self.accessTokenTextFieldRef.current.value)

    def __refresh_access_token(self):
        self.accessTokenTextFieldRef.current.value = self.__generate_access_token()
        self.page.update()