Import-Module PSFTP

$username = "anonymous"
$password = $username | ConvertTo-SecureString -AsPlainText -Force
$cred = new-object -typename System.Management.Automation.PSCredential -argumentlist $username, $password
Set-FTPConnection -Credentials $cred -Server "10.6.36.57" -Session TPSession -UsePassive 
$Session = Get-FTPConnection -Session TPSession 

Function RecursivelyUpload
{   
    Param (
        [Parameter(ValueFromPipeline=$true)]
        [String]$Path,
        [String]$DestinationPath,
        [Object]$FTPSession
    )

#    Import-Module PSFTP

    $files = Get-ChildItem -Path $Path -File
    $dirs = Get-ChildItem -Path $Path -Directory

    $files | foreach {
        $p = $_.FullName #$Path + "\" + $_.FullName
        Write-Host($p)
        $destPath = $DestinationPath + "/" + $_.Name
        Write-Host($destPath)
        #New-FTPItem -Name "test" -Session $Session
        Add-FTPItem -Session $Session -LocalPath $p -Overwrite

    }

    $dirs | foreach {
        $remotePath = $DestinationPath + "/" + $_.Name
        New-FTPItem -Name $_.Name -Session $FTPSession
        RecursivelyUpload -DestinationPath $
    }
}

RecursivelyUpload -Path "C:\repos\av-systems-automation\updateTouchpanels\vtz\fliptop" -FTPSession $Session -DestinationPath "/USER"