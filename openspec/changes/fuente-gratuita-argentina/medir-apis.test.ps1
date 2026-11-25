$ErrorActionPreference = 'Stop'
$scriptPath = Join-Path $PSScriptRoot 'medir-apis.ps1'
if (!(Test-Path $scriptPath)) {
    throw 'RED: falta el script que normaliza las respuestas'
}
. $scriptPath

function Assert-Equal($actual, $expected, $description) {
    if ($actual -cne $expected) {
        throw "$description. Esperado: $expected. Obtenido: $actual"
    }
}

$seen = [datetimeoffset]'2026-11-25T14:00:00Z'
$openLiga = [pscustomobject]@{
    matchID = 83243
    team1 = @{ teamName = 'Werder Bremen' }
    team2 = @{ teamName = 'Hamburg' }
    matchDateTimeUTC = '2026-11-22T16:30:00Z'
    matchIsFinished = $true
    matchResults = @(
        @{ resultTypeID = 2; pointsTeam1 = 4; pointsTeam2 = 0 },
        @{ resultTypeID = 1; pointsTeam1 = 0; pointsTeam2 = 0 }
    )
    goals = @()
}
$row = Convert-MatchSnapshot -Provider OpenLigaDB -Match $openLiga -ObservedAt $seen
Assert-Equal $row.Estado 'FINALIZADO' 'Final de OpenLigaDB'
Assert-Equal $row.Marcador '4-0' 'Priorizar marcador final sobre entretiempo'
Assert-Equal $row.HoraPartidoUtc '2026-11-22T16:30:00Z' 'Hora UTC'
Assert-Equal $row.HoraConsultaUtc '2026-11-25T14:00:00Z' 'Hora de observacion'

$football = [pscustomobject]@{
    id = 1
    homeTeam = @{ name = 'Werder Bremen' }
    awayTeam = @{ name = 'Hamburg' }
    utcDate = '2026-11-22T17:30:00+01:00'
    status = 'FINISHED'
    score = @{ fullTime = @{ home = 0; away = 0 }; regularTime = $null }
}
$row = Convert-MatchSnapshot -Provider FootballData -Match $football -ObservedAt $seen
Assert-Equal $row.Marcador '0-0' 'Cero es un marcador valido'
Assert-Equal $row.HoraPartidoUtc '2026-11-22T16:30:00Z' 'Convertir offset a UTC'
$football.score.fullTime.away = $null
$row = Convert-MatchSnapshot -Provider FootballData -Match $football -ObservedAt $seen
Assert-Equal $row.Marcador '' 'Resultado incompleto'
$football.score = @{ regularTime = @{ home = 1; away = 1 }; fullTime = @{ home = 2; away = 1 } }
$row = Convert-MatchSnapshot -Provider FootballData -Match $football -ObservedAt $seen
Assert-Equal $row.Marcador '1-1' 'Tiempo reglamentario separado'
$openLiga.matchIsFinished = $false
$openLiga.matchResults = @(@{ resultTypeID = 1; pointsTeam1 = 1; pointsTeam2 = 0 })
$openLiga.goals = @(@{ scoreTeam1 = 1; scoreTeam2 = 1; matchMinute = 50 })
$row = Convert-MatchSnapshot -Provider OpenLigaDB -Match $openLiga -ObservedAt $seen
Assert-Equal $row.Marcador '1-1' 'Último gol antes que el entretiempo'
Assert-Equal $row.Estado 'NO_FINALIZADO' 'Estado de OpenLigaDB sin final confirmado'
function Invoke-RestMethod {
    Write-Output -NoEnumerate @(@{ matchID = 1 }, @{ matchID = 2 })
}
$rows = @(Get-MedicionApi 'https://api.openligadb.de/getmatchdata/bl1/2026/11')
Assert-Equal $rows.Count 2 'La lista HTTP se expande en partidos individuales'
Assert-Equal $rows[1].matchID 2 'Cada elemento tiene datos de un partido'
Write-Output 'GREEN: 12 comprobaciones superadas.'


$script:requestLog = @()
$script:fixtureOpenLiga = $openLiga
$script:fixtureFootballData = $football
function Invoke-RestMethod {
    param($Uri, $Headers, $TimeoutSec, $ErrorAction)
    $script:requestLog += $Uri
    if ($Uri -like '*/getlastchangedate/*') { return '2026-11-25T14:00:00Z' }
    if ($Uri -like '*/getmatchdata/*') { return $script:fixtureOpenLiga }
    Assert-Equal $Headers['X-Auth-Token'] 'token-simulado' 'Enviar token en cabecera'
    [pscustomobject]@{ matches = @($script:fixtureFootballData) }
}
function Start-Sleep { param([int]$Seconds) }

$oldToken = $env:FOOTBALL_DATA_TOKEN
$csv = Join-Path ([IO.Path]::GetTempPath()) ("prode-c01-test-{0}.csv" -f [guid]::NewGuid())
try {
    $env:FOOTBALL_DATA_TOKEN = 'token-simulado'
    Invoke-MedicionApis -Jornada 11 -Muestras 2 -Csv $csv
    $rows = @(Import-Csv -LiteralPath $csv)
    Assert-Equal $rows.Count 4 'Dos fuentes por muestra'
    Assert-Equal @($rows | Where-Object Proveedor -eq 'FootballData').Count 2 'Registrar football-data.org'
    Assert-Equal @($script:requestLog | Where-Object {$_ -like '*/getmatchdata/*'}).Count 1 'Reutilizar jornada si no hubo cambios'
    Assert-Equal ((Get-Content -LiteralPath $csv -Raw).Contains('token-simulado')) $false 'El CSV no expone el token'
} finally {
    $env:FOOTBALL_DATA_TOKEN = $oldToken
    if (Test-Path -LiteralPath $csv) { Remove-Item -LiteralPath $csv }
}
Write-Output 'Prueba de CSV y sondeo combinado superada.'
