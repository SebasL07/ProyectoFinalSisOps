# Obtener todos los procesos
$procesos = Get-Process | Select-Object Id, Name, @{Name='CPU';Expression={($_.CPU)}}, @{Name='Memory';Expression={($_.WorkingSet / 1MB)}}

# Convertir a formato JSON y devolverlo
$procesos | ConvertTo-Json
