# terminar_proceso.ps1
param (
    [int]$processId
)

Stop-Process -Id $processId -Force
