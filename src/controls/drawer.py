import os
import signal
import flet as ft
import json
import pathlib
import subprocess

from controls.drawer_header import DrawerHeader
from controls.regulator_device_edit_dialog import RegulatorDeviceEditDialog
from utils.debugging import is_debug


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
                        leading=ft.Icon(ft.icons.TERMINAL),
                        title=ft.Text('Test shell'),
                        on_click=lambda _: self._test_shell(),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.DEVICES),
                        title=ft.Text('Add device'),
                        on_click=lambda _: self._add_regulator_device(),
                    ),
                    ft.Divider(height=10),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.DOWNLOAD),
                        title=ft.Text('Download devices'),
                        on_click=lambda _: self._download_devices(),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.UPLOAD),
                        title=ft.Text('Upload devices'),
                        on_click=lambda _: self._upload_devices(),
                    ),
                    ft.Divider(height=10),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.APP_REGISTRATION),
                        title=ft.Text('About'),
                        on_click=lambda _: self._show_about_dialog(),
                    ),
                     ft.ListTile(
                        leading=ft.Icon(ref=self.themeIconRef, name=ft.icons.LIGHT_MODE_OUTLINED),
                        title=ft.Text(ref=self.themeItemRef, value='Light Theme'),
                        on_click=lambda _: self._toggle_theme(),
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

    def _test_shell(self):

        try:
            shell_process = subprocess.Popen(
                ['pwsh', '-File', 'src/assets/test.ps1' if is_debug() else  'assets/test.ps1'],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                shell=True
            )

            while True:
                output = shell_process.stdout.readline()
                if not output:
                    break
                print(output.strip())
                self.page.app_md_view_ref.current.value += output.strip() + '\n\n'
                self.page.app_md_view_ref.current.update()
        finally:
            shell_process.kill()


    def _upload_devices(self):
        def _open_devices_callback(e: ft.FilePickerResultEvent):
            if e.files and len(e.files):
                with open(e.files[0].path, 'r') as f:
                    devices = json.loads(f.read())

                self.page.client_storage.set('devices', devices)
                self.page.update()

        file_piker = ft.FilePicker(on_result=lambda e: _open_devices_callback(e))
        self.page.add(file_piker)
        file_piker.pick_files()
        self.page.update()

    def _download_devices(self):
        def _save_devices_callback(e: ft.FilePickerResultEvent):
            if e.path:
                devices = self.page.client_storage.get('devices')
                if devices is None:
                    devices = []

                json_text = json.dumps(devices)
                path = pathlib.Path(e.path)
                if path.suffix != '.json':
                    e.path = f'{e.path}.json'

                with open(e.path, 'w') as f:
                    f.write(json_text)

        file_piker = ft.FilePicker(on_result=lambda e: _save_devices_callback(e))
        self.page.add(file_piker)
        file_piker.save_file(file_type='json', allowed_extensions=['*.json'])

    def _add_regulator_device(self):

        self.page.dialog = RegulatorDeviceEditDialog(page=self.page, device=None)
        self.page.dialog.open = True
        self.page.update()

    def _toggle_theme(self):
        current_theme = ft.ThemeMode(self.page.client_storage.get('theme_mode'))

        current_theme = ft.ThemeMode.LIGHT if current_theme == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.themeItemRef.current.value = 'Light Theme' if current_theme == ft.ThemeMode.DARK else 'Dark Theme'
        self.themeIconRef.current.name = ft.icons.LIGHT_MODE_OUTLINED if current_theme == ft.ThemeMode.DARK else ft.icons.DARK_MODE_OUTLINED

        self.page.client_storage.set('theme_mode', current_theme.value)
        self.page.theme_mode = current_theme

        self.page.update()


    def _show_about_dialog(self):

        self.about_dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            modal=True,
            title = ft.Row(controls=[
                ft.Text('About', size=24, expand=True, color='#ff5722'),
                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: self._close_about_dlg())
            ]),
            title_padding = 18,
            content=ft.Row(
                controls=[
                    ft.Image('src/assets/icon.ico' if is_debug() else 'assets/icon.ico'),
                    ft.Text('ETA Regulator Board Admin v. 0.1' ),
                ], width=450
            ),
            actions=[
                ft.ElevatedButton('OK', style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=lambda _: self._close_about_dlg(), width=100, height=35),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = self.about_dialog

        self.about_dialog.open = True
        self.page.update()
        pass

    def _close_about_dlg(self):

        self.about_dialog.open = False
        self.page.update()