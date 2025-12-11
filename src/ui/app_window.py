import flet as ft
import getpass
import time
import os
import subprocess
from .. import renamePictures
from .. import extractZip
from .. import validationXmlPdf
from .. import renamePdfUuid
from .. import processFiles
from .. import moveFilesRenamed

usuario = getpass.getuser()

def main_window(page: ft.Page):
    page.title = "Herramienta para renombrar facturas e Imagenes"
    page.window.resizable = False
    page.window.width = 800
    page.window.height = 600
    progress_bar = ft.ProgressBar(width=600, height=15, value=0, visible=False)
    lbl_progreso = ft.Text(value="", text_align=ft.TextAlign.CENTER, visible=False)
    col_progreso = ft.Column(controls=[progress_bar, lbl_progreso], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    lbl_bienvenida = ft.Text(
        value=f"\nHola {usuario} \n\nEsta herramienta ayuda a renombrar facturas de forma rápida.\n\nSelecciona una opción.",
        text_align=ft.TextAlign.CENTER,
        size=20,
    )

    selectedSucursal = ft.Ref[ft.Dropdown]()
    dropdown_sucursales = ft.Dropdown(
        ref=selectedSucursal,
        label="Sucursal",
        options=[
            ft.dropdown.Option("QUERETARO"),
            ft.dropdown.Option("CORDOBA"),
            ft.dropdown.Option("MERIDA"),
        ],
        width=200,
    )

    def mostrar_alerta(mensaje, titulo="Atención"):
        dlg = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(dlg, "open", False), page.update()))]
        )
        page.open(dlg)
        page.update()

    def update_progress(value):
        progress_bar.value = value
        page.update()

    def result_handler(func, *args):
        try:
            return func(*args)
        except Exception as e:
            mostrar_alerta(str(e), "Error")
            return None

    def process_files(carpeta):
        if carpeta is None:
            return # Se canceló el picker

        try:
            progress_bar.visible = True
            progress_bar.value = 0
            lbl_progreso.value = "Procesando..."
            lbl_progreso.visible = True
            page.update()

            # Lógica de negocio
            result_handler(extractZip.process_zip_files, carpeta)
            validationXmlPdf.moveFilesErrors(carpeta)
            renamePdfUuid.processPdfs(carpeta)
            
            # processFiles ahora retorna la ruta del excel si todo sale bien
            excel_path = result_handler(
                processFiles.process_files_logic, 
                carpeta, 
                selectedSucursal.current.value, 
                update_progress
            )

            lbl_progreso.value = "Terminado"
            page.update()
            time.sleep(1)
            
            if excel_path:
                mostrar_alerta("Renombrado de facturas completado. \n\nReporte en Excel generado.", "Éxito")
                try:
                    subprocess.Popen([excel_path], shell=True)
                except Exception as ex:
                    mostrar_alerta(f"No se pudo abrir el archivo Excel: {str(ex)}", "Error")

        except Exception as e:
             mostrar_alerta(f"Error general: {str(e)}", "Error")
        finally:
            progress_bar.visible = False
            lbl_progreso.visible = False
            page.update()

    def organize_facturas(ruta_origen):
        if ruta_origen is None:
             return 

        try:
            progress_bar.visible = True
            progress_bar.value = 0
            lbl_progreso.value = "Organizando..."
            lbl_progreso.visible = True
            page.update()

            result_handler(moveFilesRenamed.move_files_renamed, ruta_origen, update_progress)

            lbl_progreso.value = "Terminado"
            page.update()
            time.sleep(1)
            mostrar_alerta(f"Archivos organizados exitosamente en: {ruta_origen}", "Éxito")

        except Exception as e:
             mostrar_alerta(str(e), "Error")
        finally:
            progress_bar.visible = False
            lbl_progreso.visible = False
            page.update()

    def runRenamePicture(carpeta):
         if carpeta is None:
            return
         
         try:
            renamed = result_handler(renamePictures.rename_pictures_in_dir, carpeta)
            if renamed is not None:
                 mostrar_alerta("Renombrado de imágenes completado.", "Éxito")
         except Exception as e:
             mostrar_alerta(str(e), "Error")

    selectPathImg = ft.FilePicker(on_result=lambda e: runRenamePicture(e.path))
    page.overlay.append(selectPathImg)

    selectPathFacturas = ft.FilePicker(on_result=lambda e: process_files(e.path))
    page.overlay.append(selectPathFacturas)

    selectPathReorder = ft.FilePicker(on_result=lambda e: organize_facturas(e.path))
    page.overlay.append(selectPathReorder)

    def rename_facturas_click(e):
        if selectedSucursal.current.value is None:
            mostrar_alerta("Selecciona una sucursal antes de continuar.")
            return
        selectPathFacturas.get_directory_path()

    btn_img = ft.ElevatedButton(
        text="Renombrar Imágenes",
        on_click=lambda _: selectPathImg.get_directory_path(),
        width=200,
        height=50,
        style=ft.ButtonStyle(
        color=ft.Colors.TEAL_400,
        text_style=ft.TextStyle(size=17, font_family="Roboto", weight=ft.FontWeight.BOLD),
        ),
    )
    
    btn_facturas = ft.ElevatedButton(
        text="Renombrar Facturas",
        on_click=rename_facturas_click,
        width=200,
        height=50,
        style=ft.ButtonStyle(
        color=ft.Colors.TEAL_400,
        text_style=ft.TextStyle(size=17, font_family="Roboto", weight=ft.FontWeight.BOLD),
        ),
    )
    
    btn_organizar = ft.ElevatedButton(
        text="Organizar Facturas",
        on_click=lambda _: selectPathReorder.get_directory_path(),
        width=200,
        height=50,
        style=ft.ButtonStyle(
        color=ft.Colors.TEAL_400,
        text_style=ft.TextStyle(size=17, font_family="Roboto", weight=ft.FontWeight.BOLD),
        ),
    )


    page.add(
        ft.Column(
            controls=[
                lbl_bienvenida,
                dropdown_sucursales,
                ft.Row(controls=[btn_img], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[btn_facturas, btn_organizar], alignment=ft.MainAxisAlignment.CENTER),
                col_progreso
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()
