import flet as ft

from controls.drawer import Drawer
from controls.page_title import PageTitle
from controls.regulator_device_list_view import RegulatorDeviceListView

from models.regulator_device_model import RegulatorDeviceModel


def main(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.update()
    
    page.theme = ft.Theme(color_scheme_seed=ft.colors.INDIGO)
    page.app_list_view = ft.Ref[ft.ListView]()
    page.app_md_view_ref = ft.Ref[ft.Markdown]()

    page.window_width = 1024
    page.window_min_width = 640
    page.window_max_width = 1024


    if page.client_storage.get('theme_mode'):
        page.theme_mode = ft.ThemeMode(page.client_storage.get('theme_mode'))
    else:
        page.client_storage.set('theme_mode', page.theme_mode.value)

    page.drawer = Drawer(page)


    page.add(
        ft.Row(
            controls=[
                PageTitle(page=page, title='ETA Regulator Board Admin')
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
        ),
        ft.Divider(thickness=2),
        ft.Row(
            controls=[
                ft.Column(
                    [ft.Markdown(
                        ref=page.app_md_view_ref,
                        value='',
                        selectable=True,
                        extension_set="gitHubWeb",
                        code_theme="atom-one-light",
                        code_style=ft.TextStyle(font_family="Roboto Mono"),
                        expand=False,
                    )],
                    expand=True,
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.END,
            expand=False,
            height=150
        )
    )



if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets', view=ft.AppView.FLET_APP )
