from django.shortcuts import render, redirect
import subprocess
from django.conf import settings
import os
import csv

def monitor_procesos(request):
    # Construye la ruta absoluta al script
    obtener_procesos_script = os.path.join(settings.BASE_DIR, 'monitor_procesos_Linux/scripts/show_all_process.sh')

    # Ejecuta el script
    subprocess.run(['bash', obtener_procesos_script])

    # Ruta al archivo CSV generado por el script
    csv_file_path = os.path.join(settings.BASE_DIR, 'monitor_procesos_Linux/scripts/db.csv')

    # Lee el archivo CSV y convierte los datos en una lista de diccionarios
    procesos = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['User', 'Id', 'CPU', 'Memory', 'VSZ', 'RSS', 'TTY', 'Name'], delimiter=';')
        for row in reader:
            row['cpu'] = f"{float(row['CPU']):.2f}%" if row['CPU'] else 'N/A'
            row['memoria'] = f"{float(row['Memory']):.2f} MB" if row['Memory'] else 'N/A'
            procesos.append(row)

    # Renderiza la página HTML con la lista de procesos
    return render(request, 'monitor_procesos.html', {'procesos': procesos})

def terminar_proceso(request):
    if request.method == 'POST':
        process_id = request.POST.get('process_id')
        
        # Construye la ruta absoluta al script
        terminar_proceso_script = os.path.join(settings.BASE_DIR, 'monitor_procesos_Windows/scripts/terminar_procesos.ps1')
        
        # Ejecutar el script para terminar el proceso y capturar cualquier error
        result = subprocess.run(['powershell', '-File', terminar_proceso_script, '-processId', process_id], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error al terminar el proceso {process_id}: {result.stderr}")

    return redirect('monitor_procesos')


