Param (
        [Parameter(ValueFromPipeline=$true)]
        [string]$Csv = ".\tp.csv",
        [string]$output = ".\touchpanelUpdateOutput.txt" #,
        #[string]$firmwarePath
    )

Import-Module PSFTP
. .\Get-Telnet.ps1

$Hnames = @()
$Ip = @()
$Port = "41795"
$fw = ""
$fliptop = ".\firmware\ft600_1.500.0013.puf"
$teclite = ".\firmware\tpmc-4sm_11.92.113.001.puf"
$hd = ".\firmware\tsxxx0_series_1.012.0017.002.puf"

$fliptop_img = ".\vtz\fliptop\"
$teclite_img = ".\vtz\tpms\"
$hd_img = ".\vtz\hd\"


$username = "anonymous"
$password = $username | ConvertTo-SecureString -AsPlainText -Force
$cred = new-object -typename System.Management.Automation.PSCredential -argumentlist $username, $password

Import-Csv $Csv -Delimiter "," | `
    ForEach-Object { 
        $Hnames += $_.Host;
        $Ip += $_.IP;
    }

Write-Host ($Hnames)

$Ip | Foreach {
    $cmds = @()
    $InnerIP = $_

    Write-Host ($_)
    
    $Where = [array]::IndexOf($Ip, $InnerIP )
    $H = $Hnames[$Where]

    $IPTablePath_preEdit = "c:\repos\av-systems-automation\updateTouchpanels\" + $H + "_IPTable.csv"
    $IPTablePath = "c:\repos\av-systems-automation\updateTouchpanels\" + $H + "_IPTable.csv"
    
    $firmwareUpdatePath = "c:\repos\av-systems-automation\updateTouchpanels\" + $H + "_FW.csv"
    New-Item $IPTablePath -ItemType file -force
    
    #Get IPTable
    $IPTableEntry_Type = @();
    $IPTableEntry_Address = @();
    $IPTableEntry_IPID = @();
    Get-Telnet -RemoteHost "$InnerIP" -Commands "iptable" -OutputPath $IPTablePath_preEdit


    ##Determine firmware by output of iptable
    
    Set-FTPConnection -Credentials $cred -Server $InnerIP -Session TPSession -UsePassive 
    $Session = Get-FTPConnection -Session TPSession 

    $c = Get-Content $IPTablePath -Encoding byte -TotalCount 20
    [System.Text.Encoding]::Unicode.GetString($c)
    $c = [char[]](Get-Content $IPTablePath -Encoding byte -TotalCount 20)
    $c_edited = @()
    $c_edited += $c[2]
    $c_edited += $c[4]
    $tpType = -join $c_edited
    if ($tpType -match 'FT')
    {
        Add-FTPItem -Session $Session -Path "/FIRMWARE/" -LocalPath $fliptop
        $deviceType = "flip";
    }
    elseif ($tpType -match 'TS')
    {
        Add-FTPItem -Session $Session -Path "/FIRMWARE/" -LocalPath $teclite
        $deviceType = "HD";
    }
    elseif ($tpType -match 'TP')
    {
        Add-FTPItem -Session $Session -Path "/FIRMWARE/" -LocalPath $hd 
        $deviceType = "lite";
    }
    else {
        exit
    }

    New-Item $IPTablePath -ItemType file -force
    Get-Content $IPTablePath_preEdit | Where-Object {($_ -notmatch 'IP Table') -and ($_ -notmatch '-')} | Set-Content $IPTablePath

    ##Update Firmware
    #Wait for Touchpanel to come back

    do {
        Write-Host "waiting..."
        sleep 3      
    } until(Test-NetConnection $InnerIP -Port 41795 | ? { $_.TcpTestSucceeded } )

    New-Item $firmwareUpdatePath -ItemType file -force
    Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "puf"

    #Initialize
    do {
        Write-Host "waiting..."
        sleep 3      
    } until(Test-NetConnection $InnerIP -Port 41795 | ? { $_.TcpTestSucceeded } )
    Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "initialize","y"

    #betacleanup
    do {
        Write-Host "waiting..."
        sleep 3      
    } until(Test-NetConnection $InnerIP -Port 41795 | ? { $_.TcpTestSucceeded } )
    Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "betacleanup","y"

    ############
    #Load project
    do {
        Write-Host "waiting..."
        sleep 3      
    } until(Test-NetConnection $InnerIP -Port 41795 | ? { $_.TcpTestSucceeded } )

    if ($tpType -match 'FT')
    {
        #Add-FTPItem -Session $Session -Path "/USER/" -LocalPath $fliptop_img
        $deviceType = "flip";
    }
    elseif ($tpType -match 'TS')
    {
        #Add-FTPItem -Session $Session -Path "/USER/" -LocalPath $teclite_img
        $deviceType = "HD";
    }
    elseif ($tpType -match 'TP')
    {
        #Add-FTPItem -Session $Session -Path "/USER/" -LocalPath $hd_img 
        $deviceType = "lite";
    }


    #Recursively discover, mkdir and pushy files from local to remote
    
    $files = Get-ChildItem -Path $fliptop_img -File
    $dirs = Get-ChildItem -Path $fliptop_img -Directory
    $fPath = "/DISPLAY"

    $files | foreach {
        $p = $fliptop_img + "\" + $_.FullName + "." + $_.Extension
        Add-FTPItem -Session $Session -Path $fPath -LocalPath $fliptop_img
    }

    $dirs | foreach {
        $remotePath = "/DISPLAY/" + $_.Name
        New-FTPItem -Path $remotePath -Name $_.Name -Session $Session
        $subFiles = $_ | Get-ChildItem -File
        $subDirs = $_ | Get-ChildItem -Directory
    }

    #Project Load
    do {
        Write-Host "waiting..."
        sleep 3      
    } until(Test-NetConnection $InnerIP -Port 41795 | ? { $_.TcpTestSucceeded } )
    Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "projectload","y"


    #Parse IPTable
    Import-Csv $IPTablePath -Delimiter " " | `
    ForEach-Object { 
        $IPTableEntry_IPID += $_.CIP_ID
        $IPTableEntry_Type += $_.Type
        $IPTableEntry_Address += $_."IP Address/SiteName"
    }
    $IPTableEntry_IPID | Foreach {
        $IPTable_Where = [array]::IndexOf($IPTableEntry_IPID, $_ )
        $T = $IPTableEntry_Type[$IPTable_Where]
        $A = $IPTableEntry_Address[$IPTableEntry_Address]
        $IPTableOutput = ".\IPTableOutput.txt"

        if ($T -eq "Gway")
        {
            Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$IPTableOutput" -Commands "ADDMaster $_ $A"
        }
        else
        {
            Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$IPTableOutput" -Commands "ADDSlave $_ $A"            
        }
    }
}
