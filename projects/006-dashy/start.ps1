$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$cache = Join-Path $projectRoot '.cache'
$node = Join-Path $cache 'runtime/node.exe'
$builtApp = Join-Path $cache 'source/dashy-6c56436d5f044d3c53371891c9d9a8c8df8c4606/dist/index.html'
if (!(Test-Path -LiteralPath $builtApp) -or !(Test-Path -LiteralPath $node)) {
  & (Join-Path $projectRoot 'src/bootstrap.ps1')
}
try {
  $health = Invoke-RestMethod -Uri 'http://127.0.0.1:8060/healthz' -TimeoutSec 2
} catch { $health = $null }
if ($health.status -eq 'ok' -and $health.version -eq '4.6.14') {
  Write-Output 'Dashy is already running: http://127.0.0.1:8060/'
  exit 0
}
$serverFile = Join-Path $projectRoot 'src/server.cjs'
$process = Start-Process -FilePath $node -ArgumentList @('"' + $serverFile + '"') -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $cache 'server.log') -RedirectStandardError (Join-Path $cache 'server-error.log')
for ($attempt = 0; $attempt -lt 20; $attempt++) {
  Start-Sleep -Milliseconds 500
  if ($process.HasExited) { throw 'Dashy failed to start. See .cache/server-error.log.' }
  try {
    $health = Invoke-RestMethod -Uri 'http://127.0.0.1:8060/healthz' -TimeoutSec 2
    if ($health.status -eq 'ok') { Write-Output 'Dashy is running: http://127.0.0.1:8060/'; exit 0 }
  } catch { }
}
throw 'Dashy did not respond. See .cache/server.log and server-error.log.'
