Function RecursivelyUpload
{   
    Param (
        [Parameter(ValueFromPipeline=$true)]
        [String]$Path,
        [String]$DestinationPath,
        [Object]$FTPSession
    )

    Import-Module PSFTP

    $files = Get-ChildItem -Path $Path -File
    $dirs = Get-ChildItem -Path $Path -Directory

    $files | foreach {
        $p = $Path + "\" + $_.FullName
        $destPath = $DestinationPath + "/" + $_.FullName
        Add-FTPItem -Session $Session -Path $p -LocalPath $p

    }

    $dirs | foreach {
        $remotePath = $DestinationPath + "/" + $_.Name
        New-FTPItem -Path $remotePath -Name $_.Name -Session $FTPSession
        RecursivelyUpload -DestinationPath $
    }
}