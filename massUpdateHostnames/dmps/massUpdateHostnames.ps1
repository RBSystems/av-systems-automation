Param (
        [Parameter(ValueFromPipeline=$true)]
        [string]$Csv = "c:\repos\import.csv",
        [string]$output = ".\output.txt"
    )

. .\Get-Telnet.ps1

$Hnames = @()
$Ip = @()

Import-Csv $Csv -Delimiter "," | `
    ForEach-Object { 
        $Hnames += $_.Host;
        $Ip += $_.IP;
    }

$Ip | Foreach {
    $cmds = @()
    $Where = [array]::IndexOf($Ip, $_ )
    $H = $Hnames[$Where]
    $cmds += "hostname $H"
    $cmds += "reboot"
    #Write-Host("$H , $cmd , $_ ")
    Get-Telnet -RemoteHost "$_" -Port "41795" -OutputPath "$output" -Commands $cmds
}

#Get-Telnet -RemoteHost "10.6.36.51" -Port "41795" -OutputPath "C:\repos\output.txt" -Commands  "hostname"