import flet as ft

from controls.drawer_header import DrawerHeader
from controls.regulator_device_edit_dialog import RegulatorDeviceEditDialog
from models.regulator_device_model import RegulatorDeviceModel


class Drawer(ft.NavigationDrawer):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.themeItemRef = ft.Ref()
        self.themeIconRef = ft.Ref()
        self.listRef = ft.Ref()

        self.controls = [
            DrawerHeader(self.page),

            ft.ListView(
                ref=self.listRef,
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.DEVICES),
                        title=ft.Text('Add device'),
                        on_click=lambda _: self.__show_regulator_device_edit_dialog(RegulatorDeviceModel(id='', mac_address='', master_key='', name='Omega-xxx')),
                    ),
                    ft.Divider(height=10),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.APP_REGISTRATION),
                        title=ft.Text('About'),
                        on_click=lambda _: self.__show_about_dialog(),
                    ),
                     ft.ListTile(
                        leading=ft.Icon(ref=self.themeIconRef, name=ft.icons.LIGHT_MODE_OUTLINED),
                        title=ft.Text(ref=self.themeItemRef, value='Light Theme'),
                        on_click=lambda _: self.__toggle_theme(),
                    ),
                    ft.Divider(height=10),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.EXIT_TO_APP),
                        title=ft.Text('Exit'),
                        on_click=lambda _: self.page.window_close()
                    )
                ]
            )
        ]
        current_theme = ft.ThemeMode(self.page.client_storage.get('theme_mode'))
        self.themeItemRef.current.value = 'Light Theme' if current_theme == ft.ThemeMode.DARK else 'Dark Theme'
        self.themeIconRef.current.name = ft.icons.LIGHT_MODE_OUTLINED if current_theme == ft.ThemeMode.DARK else ft.icons.DARK_MODE_OUTLINED


    def __show_regulator_device_edit_dialog(self, device: RegulatorDeviceModel):
        self.open = False

        self.page.dialog = RegulatorDeviceEditDialog(self.page, device)
        self.page.dialog.open = True
        self.page.update()

    def __toggle_theme(self):
        current_theme = ft.ThemeMode(self.page.client_storage.get('theme_mode'))

        current_theme = ft.ThemeMode.LIGHT if current_theme == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.themeItemRef.current.value = 'Light Theme' if current_theme == ft.ThemeMode.DARK else 'Dark Theme'
        self.themeIconRef.current.name = ft.icons.LIGHT_MODE_OUTLINED if current_theme == ft.ThemeMode.DARK else ft.icons.DARK_MODE_OUTLINED

        self.page.client_storage.set('theme_mode', current_theme.value)
        self.page.theme_mode = current_theme

        self.page.update()


    def __show_about_dialog(self):
        self.open = False

        self.page.dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            modal=True,
            title=ft.Text('About'),
            content=ft.Row(
                controls=[
                    ft.Image('src/assets/icon.ico'),
                    ft.Text('ETA RegulatorBoard Admin v. 0.1' ),
                ], width=450
            ),
            actions=[
                ft.ElevatedButton('OK', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=lambda _: self.__close_about_dlg(), width=100, height=35),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog.open = True
        self.page.update()

    def __close_about_dlg(self):
        self.page.dialog.open = False
        self.page.update()