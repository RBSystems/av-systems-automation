    Function logToElk {

    Param (
            [Parameter(ValueFromPipeline=$true)]
            [string]$Message,
            [string]$BuildNo = "BULDNUMBERGOESHERE",
            [string]$ActiveHostName,
            [string]$ActiveHostIP,
            [string]$ServerAddress,
            [bool]$Success,
            [string]$Logs
        )
        $timestamp = Get-Date
        $timestamp = $timestamp.ToUniversalTime().GetDateTimeFormats('F')[0]


        $Params = @{BuildNo=$BuildNo; TPName=$ActiveHostName; TPAddress=$ActiveHostIP; Success=$Success ;Message=$Message; Timestamp=$timestamp; Logs=$Logs}
        $JSON = $Params | convertto-json


        Write-Host("PARAMS__________")
        Write-Host($Params)

        Invoke-WebRequest -Uri $ServerAddress -Method POST -Body $JSON
}

