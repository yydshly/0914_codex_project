$ErrorActionPreference = 'Stop'
$pidFile = Join-Path $PSScriptRoot '.cache/server.pid'
if (!(Test-Path -LiteralPath $pidFile)) { Write-Output 'No saved Dashy process.'; exit 0 }
$serverPid = [int](Get-Content -LiteralPath $pidFile)
$running = Get-CimInstance Win32_Process -Filter "ProcessId = $serverPid"
$serverFile = Join-Path $PSScriptRoot 'src/server.cjs'
if ($running -and $running.CommandLine.Contains($serverFile)) {
  Stop-Process -Id $serverPid
  Write-Output 'Dashy stopped.'
} else { Write-Output 'The saved process is no longer this demo. Nothing stopped.' }
