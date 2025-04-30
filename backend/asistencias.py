import json
from datetime import datetime
import pandas as pd
import os
import shutil
from pathlib import Path


def leer_datos_json(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcular_tardanza(hora_real, hora_referencia):
    if hora_real:
        entrada = datetime.strptime(hora_real, "%H:%M")
        referencia = datetime.strptime(hora_referencia, "%H:%M")
        return max(0, int((entrada - referencia).total_seconds() / 60))
    return 0

def procesar_asistencias(data, fecha_inicio, fecha_fin):
    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    tardanzas = {}

    for registro in data:
        fecha_registro = datetime.strptime(registro["fecha"], "%Y-%m-%d")
        if fecha_inicio <= fecha_registro <= fecha_fin:
            nombre = registro["nombre"]
            dia_semana = fecha_registro.weekday()  # 0 = lunes, ..., 5 = sábado

            # Hora de ingreso de referencia
            hora_ref_mañana = "09:00" if dia_semana == 5 else "08:00"
            hora_ref_tarde = "15:00"

            # Calcular tardanzas
            tardanza_mañana = calcular_tardanza(registro["hora_ingreso_1"], hora_ref_mañana)
            tardanza_tarde = 0
            if dia_semana < 5:
                tardanza_tarde = calcular_tardanza(registro["hora_ingreso_2"], hora_ref_tarde)

            total = tardanza_mañana + tardanza_tarde

            if nombre not in tardanzas:
                tardanzas[nombre] = 0
            tardanzas[nombre] += total

    # Convertir a DataFrame
    df = pd.DataFrame(list(tardanzas.items()), columns=["Empleado", "Minutos de Tardanza"])
    df.to_excel("reporte_tardanza.xlsx", index=False)
    return df

def descarga():
    # Ruta de la carpeta Descargas del usuario actual en Windows
    carpeta_descargas = Path(os.path.expanduser("~")) / "Downloads"
    archivo_origen = Path("reporte_tardanza.xlsx")
    destino = carpeta_descargas / archivo_origen.name

    try:
        shutil.copy(archivo_origen, destino)
        print(f"✅ El archivo se ha guardado correctamente en: {destino}")
    except Exception as e:
        print(f"❌ Error al guardar el archivo en Descargas: {e}")
     