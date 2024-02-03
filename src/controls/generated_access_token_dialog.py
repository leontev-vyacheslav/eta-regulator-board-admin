import flet as ft

from models.regulator_device_model import RegulatorDeviceModel
from utils.encoding import create_access_token


class GeneratedAccessTokenDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, device: RegulatorDeviceModel):

        super().__init__()
        self.page = page
        self.device = device
        self.shape = ft.RoundedRectangleBorder(radius=5)
        self.title = ft.Text(f'Generate access token')
        self.modal = True
        self.expand = False
        self.content = ft.Row(
            controls=[
                ft.TextField(
                    label=f'Access Token',
                    expand=True,
                    value=self.__generate_access_token(),
                ),
            ],
            width=450,
            expand=True
        )
        self.actions=[
            ft.ElevatedButton('CLOSE', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=lambda _: self.__close_dlg(), width=100, height=35),
        ]

        self.actions_alignment=ft.MainAxisAlignment.END

    def __generate_access_token(self):
        return create_access_token(self.device.mac, 8, self.device.master_key)


    def __close_dlg(self):
        self.open = False
        self.page.update()