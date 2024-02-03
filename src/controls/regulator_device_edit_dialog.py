import flet as ft

from models.regulator_device_model import RegulatorDeviceModel

class RegulatorDeviceEditDialog(ft.AlertDialog):

    def __init__(self, page: ft.Page, device: RegulatorDeviceModel):
        self.page = page
        super().__init__()

        self.device = device
        self.shape = ft.RoundedRectangleBorder(radius=5)
        self.title = ft.Text(f'Regulator device')
        self.modal = True
        self.expand = False
        self.content = ft.Column(controls=[
            ft.Row(
                controls=[
                    ft.TextField(
                        label=f'Name',
                        expand=True,
                       value=self.device.name,
                    ),
                ],
                width=450,
                expand=True
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        label=f'MAC address',
                        expand=True,
                        value=self.device.mac_address,
                    ),
                ],
                width=450,
                expand=True
            ),
        ], height=220)

        self.actions=[
            ft.ElevatedButton('CLOSE', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=lambda _: self.__close_dlg(), width=100, height=35),
        ]

        self.actions_alignment=ft.MainAxisAlignment.END

    def __close_dlg(self):
        self.open = False
        self.page.update()