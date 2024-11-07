from django.shortcuts import render, redirect
import subprocess
from django.conf import settings
import os

def monitor_procesos(request):
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
    print(f"Resultado del script: {result.stdout}")

    if result.returncode != 0:
        print(f"Error en el script: {result.stderr}")

    # Renderiza la página HTML con la lista de procesos
    return render(request, 'monitor_procesos.html', {'procesos': procesos})

def terminar_proceso(request):
    if request.method == 'POST':
        process_id = request.POST.get('process_id')
        
        # Construye la ruta absoluta al script
        terminar_proceso_script = os.path.join(settings.BASE_DIR, 'monitor_procesos/scripts/terminar_proceso.ps1')
        
        # Llama al script de PowerShell para terminar el proceso
        subprocess.run(['powershell', '-File', terminar_proceso_script, '-processId', process_id])
        
    return redirect('monitor_procesos')

