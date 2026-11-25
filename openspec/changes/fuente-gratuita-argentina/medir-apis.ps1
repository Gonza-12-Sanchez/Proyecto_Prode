param(
    [ValidateRange(1, 34)][int]$Jornada = 11,
    [ValidateRange(1, 200)][int]$Muestras = 1,
    [switch]$SoloOpenLiga,
    [string]$Csv = (Join-Path ([IO.Path]::GetTempPath()) ("prode-c01-{0}.csv" -f (Get-Date -Format 'yyyyMMdd-HHmmss-fff')))
)

function Format-Utc($value) {
    ([datetimeoffset]$value).UtcDateTime.ToString("yyyy-MM-ddTHH:mm:ss'Z'")
}

function Convert-MatchSnapshot {
    param(
        [ValidateSet('OpenLigaDB', 'FootballData')][string]$Provider,
        $Match,
        [datetimeoffset]$ObservedAt
    )
    if ($Provider -eq 'OpenLigaDB') {
        $id = $Match.matchID
        $homeTeamName = $Match.team1.teamName
        $away = $Match.team2.teamName
        $kickoff = $Match.matchDateTimeUTC
        $status = if ($Match.matchIsFinished) { 'FINALIZADO' } else { 'NO_FINALIZADO' }
        if ($Match.matchIsFinished) {
            $score = $Match.matchResults | Where-Object resultTypeID -eq 2 | Select-Object -First 1
            $goalsHome = $score.pointsTeam1
            $goalsAway = $score.pointsTeam2
        } else {
            $goal = $Match.goals | Where-Object { $null -ne $_.scoreTeam1 -and $null -ne $_.scoreTeam2 } |
                Sort-Object { [int]$_.scoreTeam1 + [int]$_.scoreTeam2 } -Descending | Select-Object -First 1
            $goalsHome = $goal.scoreTeam1
            $goalsAway = $goal.scoreTeam2
        }
    } else {
        $id = $Match.id
        $homeTeamName = $Match.homeTeam.name
        $away = $Match.awayTeam.name
        $kickoff = $Match.utcDate
        $status = $Match.status
        $score = if ($null -ne $Match.score.regularTime) { $Match.score.regularTime } else { $Match.score.fullTime }
        $goalsHome = $score.home
        $goalsAway = $score.away
    }
    [pscustomobject]@{
        Proveedor = $Provider
        HoraConsultaUtc = Format-Utc $ObservedAt
        IdPartido = $id
        HoraPartidoUtc = Format-Utc $kickoff
        Local = $homeTeamName
        Visitante = $away
        Estado = $status
        Marcador = if ($null -ne $goalsHome -and $null -ne $goalsAway) { "$goalsHome-$goalsAway" } else { '' }
    }
}

function Get-MedicionApi([string]$Uri, [hashtable]$Headers = @{}) {
    try {
        $response = Invoke-RestMethod -Uri $Uri -Headers $Headers -TimeoutSec 12 -ErrorAction Stop
        $response
    } catch {
        $hostName = ([uri]$Uri).Host
        if ($null -ne $_.Exception.Response) {
            $statusCode = [int]$_.Exception.Response.StatusCode
            throw "$hostName devolvio HTTP $statusCode."
        }
        throw "Sin respuesta HTTP de $hostName. Verifica la red y vuelve a intentar."
    }
}

function Invoke-MedicionApis {
    param([int]$Jornada, [int]$Muestras, [switch]$SoloOpenLiga, [string]$Csv)
    if (Test-Path -LiteralPath $Csv) { throw 'El CSV existe. Elegi una ruta nueva.' }
    $headers = @{}
    if (!$SoloOpenLiga) {
        $token = $env:FOOTBALL_DATA_TOKEN
        if ([string]::IsNullOrWhiteSpace($token)) {
            $secure = Read-Host 'Token de football-data.org' -AsSecureString
            $token = [System.Net.NetworkCredential]::new('', $secure).Password
        }
        if ([string]::IsNullOrWhiteSpace($token)) { throw 'Falta el token de football-data.org.' }
        $headers['X-Auth-Token'] = $token.Trim()
    }

    $ligaPath = "bl1/2026/$Jornada"
    $ligaUri = "https://api.openligadb.de/getmatchdata/$ligaPath"
    $fechaUri = "https://api.openligadb.de/getlastchangedate/$ligaPath"
    $footballUri = "https://api.football-data.org/v4/competitions/BL1/matches?season=2026&matchday=$Jornada"
    $ligaMatches = @()
    $ultimaVersion = $null
    $version = $null
    $nextTick = [datetimeoffset]::UtcNow

    for ($i = 0; $i -lt $Muestras; $i++) {
        if ($i -gt 0) {
            $delay = [math]::Ceiling(($nextTick - [datetimeoffset]::UtcNow).TotalSeconds)
            if ($delay -gt 0) { Start-Sleep -Seconds $delay }
        }
        $nextTick = [datetimeoffset]::UtcNow.AddMinutes(1)
        $rows = @()
        $errors = @()
        try {
            if ($Muestras -gt 1) { $version = Get-MedicionApi $fechaUri }
            if (!$ligaMatches.Count -or $version -ne $ultimaVersion) {
                $ligaMatches = @(Get-MedicionApi $ligaUri)
                $ultimaVersion = $version
            }
            $seen = [datetimeoffset]::UtcNow
            foreach ($match in $ligaMatches) {
                $rows += Convert-MatchSnapshot -Provider OpenLigaDB -Match $match -ObservedAt $seen
            }
        } catch {
            if ($_.Exception.Message -notmatch '^(Sin respuesta HTTP de |api\.openligadb\.de devolvio HTTP )') {
                $errors += 'Respuesta de OpenLigaDB no interpretable.'
            } else { $errors += $_.Exception.Message }
        }
        if (!$SoloOpenLiga) {
            try {
                $football = Get-MedicionApi $footballUri $headers
                $seen = [datetimeoffset]::UtcNow
                foreach ($match in $football.matches) {
                    $rows += Convert-MatchSnapshot -Provider FootballData -Match $match -ObservedAt $seen
                }
            } catch {
                if ($_.Exception.Message -notmatch '^(Sin respuesta HTTP de |api\.football-data\.org devolvio HTTP )') {
                    $errors += 'Respuesta de football-data.org no interpretable.'
                } else { $errors += $_.Exception.Message }
            }
        }
        if ($rows.Count) {
            $rows | Export-Csv -LiteralPath $Csv -NoTypeInformation -Encoding UTF8 -Append
            if ($Muestras -eq 1) { $rows | Format-Table IdPartido,HoraPartidoUtc,Local,Visitante,Estado,Marcador,Proveedor }
        }
        $utc = Format-Utc ([datetimeoffset]::UtcNow)
        foreach ($message in $errors) { Write-Warning "$utc $message" }
        if ($errors -match 'HTTP (401|403|429)\.') { throw 'Ensayo interrumpido: revisa el acceso o espera la renovacion de la cuota.' }
        Write-Host "Muestra $($i + 1)/$Muestras, $utc, $($rows.Count) partidos registrados"
    }
    if (!(Test-Path -LiteralPath $Csv)) { throw 'El ensayo no obtuvo partidos.' }
    Write-Host "CSV: $Csv"
}

if ($MyInvocation.InvocationName -ne '.') {
    $ErrorActionPreference = 'Stop'
    Invoke-MedicionApis -Jornada $Jornada -Muestras $Muestras -SoloOpenLiga:$SoloOpenLiga -Csv $Csv
}
