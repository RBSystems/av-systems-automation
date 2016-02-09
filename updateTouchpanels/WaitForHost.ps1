Param (
        [Parameter(ValueFromPipeline=$true)]
        [string]$Host,
        [int32]$Port = 22
    )

do {
    Write-Host "waiting..."
    sleep 3
    } until(Test-NetConnection $Host -Port $Port | ? { $_.TcpTestSucceeded } )