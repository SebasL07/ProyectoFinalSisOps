import csv
from django.shortcuts import render, redirect
import subprocess
from django.conf import settings
import os
import platform

def monitor_procesos_windows(request):


    if platform.system() == 'Windows':
        # Construye la ruta absoluta al script
        obtener_procesos_script = os.path.join(settings.BASE_DIR, 'monitor_procesos_Windows/scripts/obtener_procesos.ps1')
        
        # Ejecuta el script de PowerShell y captura la salida
        result = subprocess.run(['powershell', '-File', obtener_procesos_script], capture_output=True, text=True)
        
        # Convierte la salida JSON en una lista de diccionarios
        procesos = []
        if result.returncode == 0:
            try:
                import json
                procesos = json.loads(result.stdout)
            except json.JSONDecodeError:
                procesos = []
        else: 
            procesos = []

        for proceso in procesos:
            proceso['cpu'] = proceso['CPU'] if proceso['CPU'] is not None else 'N/A'
            proceso['memoria'] = f"{proceso['Memory']} MB"  # Redondear y mostrar con dos decimales

        if proceso.get('CPU') is not None:
            proceso['cpu'] = f"{proceso['CPU']:.2f}%"  # Formatear con dos decimales
        else:
            proceso['cpu'] = 'N/A'  # Si no tiene valor, poner N/A o 0%


        for proceso in procesos:
        # Si la CPU es un valor numérico, conviértelo en porcentaje
            if proceso.get('CPU') is not None:
                proceso['cpu'] = f"{proceso['CPU']:.2f}%"  # Formatear con dos decimales
            else:
                proceso['cpu'] = 'N/A'  # Si no tiene valor, poner N/A o 0%

        # Para la memoria, puedes redondear a dos decimales y agregar la unidad 'MB'
        proceso['memoria'] = f"{proceso['Memory']:.2f} MB"  # Redondear la memoria a dos decimales

        #Verificacion de la salida del script en python
        result = subprocess.run(['powershell', '-File', obtener_procesos_script], capture_output=True, text=True)

        # Verifica la salida del script
        # print(f"Resultado del script: {result.stdout}")
    else:
        
        # Construye la ruta absoluta al script
        result = os.path.join(settings.BASE_DIR, 'monitor_procesos_Windows/scripts/show_all_process.sh')

        # Ejecuta el script
        subprocess.run(['bash', result])

        # Ruta al archivo CSV generado por el script
        csv_file_path = os.path.join(settings.BASE_DIR, 'monitor_procesos_Windows/scripts/db.csv')

        # Lee el archivo CSV y convierte los datos en una lista de diccionarios
        procesos = []
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=['User', 'Id', 'CPU', 'Memory', 'VSZ', 'RSS', 'TTY', 'Name'], delimiter=';')
            for row in reader:
                try:
                    row['cpu'] = f"{float(row['CPU']):.2f}%" if row['CPU'].replace('.', '', 1).isdigit() else 'N/A'
                except ValueError:
                    row['cpu'] = 'N/A'
                try:
                    row['memoria'] = f"{float(row['Memory']):.2f} MB" if row['Memory'].replace('.', '', 1).isdigit() else 'N/A'
                except ValueError:
                    row['memoria'] = 'N/A'
                procesos.append(row)

    if result.returncode != 0:
        print(f"Error en el script: {result.stderr}")

    # Renderiza la página HTML con la lista de procesos
    return render(request, 'monitor_procesos.html', {'procesos': procesos})

def terminar_proceso_windows(request):
    if request.method == 'POST':

        if platform.system() == 'Windows':
            process_id = request.POST.get('process_id')
            
            # Construye la ruta absoluta al script
            terminar_proceso_script = os.path.join(settings.BASE_DIR, 'monitor_procesos_Windows/scripts/terminar_procesos.ps1')
            
            # Ejecutar el script para terminar el proceso y capturar cualquier error
            result = subprocess.run(['powershell', '-File', terminar_proceso_script, '-processId', process_id], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error al terminar el proceso {process_id}: {result.stderr}")
        else:
            process_id = request.POST.get('process_id')
        
            # Construye la ruta absoluta al script
            terminar_proceso_script = os.path.join(settings.BASE_DIR, 'monitor_procesos_Windows/scripts/kill_process.sh')
            
            # Ejecutar el script para terminar el proceso y capturar cualquier error
            result = subprocess.run(['bash', terminar_proceso_script, process_id], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error al terminar el proceso {process_id}: {result.stderr}")

        

    return redirect('monitor_procesos_windows')

