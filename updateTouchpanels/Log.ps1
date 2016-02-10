<#
.SYNOPSIS
    Simple function to write a log file entry
.PARAMETER Message
    The message you wish to append to the file
.PARAMETER File
    Full path and file name of where you want the script to save the output.
.INPUTS
    String input from Pipeline.
.OUTPUTS
    Log file at specified location
.EXAMPLE
    Get-Content "c:\scripts\commands.txt" | Get-Telnet -RemoteHost "192.168.10.1" -OutputPath "\\server\share\ciscoswitch.txt" -WaitTime 1500
    Get-Telnet -Commands (Get-Content "c:\scripts\commands.txt") -RemoteHost "192.168.10.1" -OutputPath "\\server\share\ciscoswitch.txt" -WaitTime 1500
    
    Two examples of how to use Get-Content to pull a series of commands from a text file
    and execute them.
.NOTES
    Author:            Dan Clegg
       
    Changelog:
       1.0             Initial Release
#>

Function Log
{
    Param (
            [Parameter(ValueFromPipeline=$true)]
            [string]$File,
            [string]$Message
        )

    filter timestamp {"$(Get-Date -Format o): $_"}

    if ((Test-Path $File) -eq $false) {
        New-Item -Path $File -ItemType File
        }
    $line = & "`n" + $Message | timestamp
    Write-Host($line)
    Add-Content -Path $File -Value $line
}