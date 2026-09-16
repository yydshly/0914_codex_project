$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$revision = '6c56436d5f044d3c53371891c9d9a8c8df8c4606'
$cache = Join-Path $projectRoot '.cache'
$upstream = Join-Path $cache "source/dashy-$revision"
$node = Join-Path $cache 'runtime/node.exe'
$yarn = Join-Path $cache 'tools/node_modules/yarn/bin/yarn.js'
New-Item -ItemType Directory -Path $cache -Force | Out-Null
if (!(Test-Path -LiteralPath (Join-Path $upstream 'package.json'))) {
  $archive = Join-Path $cache 'dashy.zip'
  Invoke-WebRequest -Uri "https://codeload.github.com/Lissy93/dashy/zip/$revision" -OutFile $archive
  Expand-Archive -LiteralPath $archive -DestinationPath (Join-Path $cache 'source') -Force
}
if (!(Test-Path -LiteralPath $node) -or !(Test-Path -LiteralPath $yarn)) {
  & npm.cmd install --prefix (Join-Path $cache 'tools') node@24.19.0 yarn@1.22.22 --no-audit --no-fund
  if ($LASTEXITCODE -ne 0) { throw 'Runtime installation failed.' }
  New-Item -ItemType Directory -Path (Split-Path $node -Parent) -Force | Out-Null
  Copy-Item -LiteralPath (Join-Path $cache 'tools/node_modules/node/bin/node.exe') -Destination $node
}
$env:PATH = (Split-Path $node -Parent) + ';' + $env:PATH
$env:USER_DATA_DIR = Join-Path $projectRoot 'user-data'
$env:VITE_APP_ROUTING_MODE = 'hash'
Push-Location $upstream
try {
  & $node $yarn install --frozen-lockfile --non-interactive --network-timeout 120000
  if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
  & $node 'node_modules/vite/bin/vite.js' build
  if ($LASTEXITCODE -ne 0) { throw 'Dashy build failed.' }
} finally { Pop-Location }
Write-Output 'Ready. Run start.ps1 to open the local demo.'
