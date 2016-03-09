Param (
        [Parameter(ValueFromPipeline=$true)]
        [string]$Csv = ".\tp.csv",
        [string]$output = ".\touchpanelUpdate_log",
        [string]$BuildNumber = "1",
        [string]$ElkServer = "http://avreports.byu.edu:9200/updates/TP_"+$BuildNumber
    )

Import-Module PSFTP

. .\Get-Telnet.ps1
. .\Log.ps1
. .\LogToELK.ps1

#CONSTANTS
$Port = "41795"

#Flip top values
$fliptop = ".\firmware\ft600_1.500.0013.puf"
$flipVersionNo = "1.012.0017"
$hdProjectTime = "January 22, 2016 16:02:57"
$fliptop_img = "ft.vtz"

#TecLite values
$teclite = ".\firmware\tpmc-4sm_11.92.113.001.puf"
$liteVersionNo = "1.012.0017"
$hdProjectTime = "January 22, 2016 16:02:57"
$teclite_img = "lite.vtz"

#HD Values
$hd = ".\firmware\tsxxx0_series_1.012.0017.002.puf"
$hdVersionNo = "1.012.0017"
$hdProjectTime = "January 22, 2016 16:02:57"
$hd_img = "hd.vtz"



$fliptopPath = "$($pwd)\vtz\$($fliptop_img)"
$teclitePath = "$($pwd)\vtz\$($teclite_img)"
$telnetDump = ".\telnetdump"
$hdPath = "$($pwd)\vtz\$($hd_img)"

$username = "anonymous"
$password = $username | ConvertTo-SecureString -AsPlainText -Force

#logBuffer - we empty this on success, or on failure write it up to ELK. 
$logBuffer = @()

#-----
#Is this necessary?
#-----
$cred = new-object -typename System.Management.Automation.PSCredential -argumentlist $username, $password

#Variables
$Hnames = @()
$Ip = @()
$fw = ""

Import-Csv $Csv -Delimiter "," | `
    ForEach-Object { 
        $Hnames += $_.Host;
        $Ip += $_.IP;
    }

$Now = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"

$output = "$($output)_1.txt"#"$($Now).txt"

New-Item $telnetDump -ItemType file -force
#We don't need this - we take care of this in the Log function
#New-Item $output -ItemType file -force

$Ip | Foreach {
    try {
        $cmds = @()
        $InnerIP = $_
        $logBuffer.Clear()
    
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Updating $($InnerIP)"
    
        #get The hostname associated with this IP - create an array of objects with two properties and run a
        #function of that.
        $Where = [array]::IndexOf($Ip, $InnerIP )
        $H = $Hnames[$Where]

        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "$($H)"

        #This is the IP table denoting what? Where the touchpanel is? 
        $IPTablePath_preEdit = ".\IPtables\" + $H + "Pre_IPTable.csv"
        $IPTablePath = ".\IPtables\" + $H + "_IPTable.csv"
    
        $firmwareUpdatePath = ".\FirmwareCSV\" + $H + "_FW.csv"
        New-Item $IPTablePath -ItemType file -force
        New-Item $IPTablePath_preEdit -ItemType file -force

        #Get IPTable
        $IPTableEntry_Type = @();
        $IPTableEntry_Address = @();
        $IPTableEntry_IPID = @();

        while (!(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )) {
            Write-Host "waiting..."
            sleep 3      
        }
        #remove all of the exess.puf files from the box, otherwise he firmware update won'tw ork. 
        $out = Get-Telnet -RemoteHost "$InnerIP" -Commands "cd \ROMDISK\user\system","erase *.puf" 

        #---------------
        #Get the IPTable

        while (!(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )) {
            Write-Host "waiting..."
            sleep 3      
        }
        $out = Get-Telnet -RemoteHost "$InnerIP" -Commands "iptable" -OutputPath $IPTablePath_preEdit
    
        New-Item $IPTablePath -ItemType file -force
        "CIP_ID Type Status Port IpAddress" | Add-Content $IPTablePath
        $ipTableHolder = ((Get-Content $IPTablePath_preEdit | Where-Object {($_ -notmatch 'IP Table') -and ($_ -notmatch '-')}) -replace "\s+", " ")
        $ipTableHolder.Trim() | Add-Content $IPTablePath

    
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Obtained IPTable for $($InnerIP)"

        #------------------------------------------------------------
        #VERIFY THAT THE UPGRADE IS NEEDED. 
        #------------------------------------------------------------

        #Verify that the machine is a touchpanel, and what type

        $c = Get-Content $IPTablePath_preEdit -Encoding byte -TotalCount 20

        ##Determine firmware by output of iptable
        [System.Text.Encoding]::Unicode.GetString($c)
        $c = [char[]](Get-Content $IPTablePath_preEdit -Encoding byte -TotalCount 20)
        $c_edited = @()
        $c_edited += $c[0]
        $c_edited += $c[1]
        $tpType = -join $c_edited

        if ($tpType -match 'FT')
        {
            $firmwareRegex = "\[v($($flipVersionNo))\ "
            $projectRegex = "Date=($($flipProjectTime))"
        }
        elseif ($tpType -match 'TS')
        {
            $firmwareRegex = "\[v($($hdVersionNo))\ "
            $projectRegex = "Date=($($hdProjectTime))"
        }
        elseif ($tpType -match 'TP')
        {
            $firmwareRegex = "\[v($($liteVersionNo))\ "
            $projectRegex = "Date=($($liteProjectTime))"
        } else {
            exit
        }


        ##------------------------------------------------------------
        #Check the firmware version and project date against expected values. 

        $success = $true 

        #FIRMWARE VERSION
        $VersionOut = Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath $telnetDump -Commands "version"            

        #Check for a match
        if ($VersionOut -notmatch $firmwareRegex)
        {
            $success = $false 
            $ErrorList += "Incorrect Firmware Version: " + $VersionOut +"`n"
        }
        else {
             $message = "Verified Firmware version."
             $logBuffer += Log -BuildNo $BuildNumber -File $output -Message $message
        }

        #PROJECT DATE (Program)
        $ProjectOut = Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath $telnetDump -Commands "cd \romdisk\user\display", "type .\~.LocalInfo.vtpage"

        if ($ProjectOut -notmatch $projectRegex)
        {
            $success = $false 
            $ErrorList += "Incorrect ProjectDate Version: " + $ProjectOut +"`n"
        }
        else {
             $message = "Verified Project Date."
             $logBuffer += Log -BuildNo $BuildNumber -File $output -Message $message 
        }

        #If we're up to date, log it an move on. 
        if ($success -eq $true) {
            $message = "Touchpanel up to date, no upgrade needed."
            $logBuffer += Log -BuildNo $BuildNumber -File $output -Message $message 
            
            $logToSend = ""
            $logBuffer | Foreach {
            $logToSend += $_
            }

            logToElk -Message "Touchpanel already up to date - no need to update." -BuildNo $BuildNumber -ActiveHostName $H -ActiveHostIp $InnerIP -ServerAddress $ELKServer -Success $true -Logs $logToSend
            #return
        }

        #---------------
        #Initialize
        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )

        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Initializing $($InnerIP)"
        Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "initialize","y"
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Initialized."

        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )

    
    
    

        #---------------
        #Send the firmware via FTP

        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Starting the FTP Session"

        Set-FTPConnection -Credentials $cred -Server $InnerIP -Session TPSession -UsePassive 
        $Session = Get-FTPConnection -Session TPSession 
    
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message ("Adding item " + $tpType + " to the FTP Session")


        if ($tpType -match 'FT')
        {
            $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Adding FlipTop Firmware"
            Add-FTPItem -Session $Session -Path "/FIRMWARE/" -LocalPath $fliptop
            $deviceType = "flip";
        }
        elseif ($tpType -match 'TS')
        {
            $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Adding hd Firmware"
            Add-FTPItem -Session $Session -Path "/FIRMWARE/" -LocalPath $hd
            $deviceType = "HD";
        }
        elseif ($tpType -match 'TP')
        {
            $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Adding lite Firmware"
            Add-FTPItem -Session $Session -Path "/FIRMWARE/" -LocalPath $teclite 
            $deviceType = "lite";
        }
        else {
            exit
        }
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Device Type: $($deviceType)"
    
        #---------------------
        #Update Firmware
        #Wait for Touchpanel to come back
        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )

        New-Item $firmwareUpdatePath -ItemType file -force
        Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "puf"
    
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Updated firmware"

        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )

        Sleep 60
        
        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )
        
        do {
            Write-Host "waiting..."
            sleep 3      
            $matches = Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$telnetDump" -Commands " "
        } until ($matches -notmatch "The System is busy.")
        #---------------
        #betacleanup
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Running betacleanup..."
        Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "betacleanup","y"
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Betacleanup complete"

        #---------------
        #Load project via FTP
        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )

        $projName = ""
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Uploading project..."
        switch ($tpType) {
            'FT'
            {
                Add-FTPItem -LocalPath "$($fliptopPath)" -Overwrite -Session $Session
                $projName = $fliptop_img
            }        
            'TS'
            {
                Add-FTPItem -LocalPath "$($hdPath)" -Overwrite -Session $Session
                $projName = $hd_img
            }        
            'TP'
            {
                Add-FTPItem -LocalPath "$($teclitePath)" -Overwrite -Session $Session
                $projName = $teclite_img
            }
        }

        #---------------
        #Project Load
        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )
    
        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Loading project..."

        if ($tpType -notmatch 'TS'){
            Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "cd \FTP","MOVEFILE $($projName) \ROMDISK\User\Display","reboot"
        }
        else
        {
            Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "cd \FTP","MOVEFILE $($projName) \ROMDISK\user\Display","reboot"
        }
    
        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )
        Sleep 60

        Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$firmwareUpdatePath" -Commands "projectload"

        do {
            Write-Host "waiting..."
            sleep 3      
        } until(Test-NetConnection $InnerIP -Port $Port | ? { $_.TcpTestSucceeded } )
    
    


        #---------------
        #Reload IPTable

        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Reloading IPTable for $($InnerIP)"

        $iptable = Import-Csv $IPTablePath -Delimiter " "

        Write-Host("THIS IS THE IP TABLE BEING LOADED")
        Write-Host($iptable)

        $iptable | Foreach {
            $IPTableOutput = ".\IPTableOutput.txt"


            if ($_.Type -eq "Gway")
            {
                $generatedCommand = "ADDMaster $($_.CIP_ID)  $($_.IpAddress)"

                write-host($generatedCommand)

                Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$IPTableOutput" -Commands $generatedCommand
                $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Adding Master entry for $($_.CIP_ID + " " +$_.IpAddress)"
            }
            else
            {
                Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath "$IPTableOutput" -Commands "ADDSlave $($_.CIP_ID)  $($_.IpAddress)"
                $logBuffer += Log -BuildNo $BuildNumber -File $output -Message "Adding Slave entry for $($_.CIP_ID + $_.IpAddress)"
            }
        }
        #----------------------------------------------------------
        #END UPDATE
        #----------------------------------------------------------

        #----------------------------------------------------------
        #BEGIN VALIDATION
        #----------------------------------------------------------
        #We need to check success/failure. 
        $success = $true 


        #FIRMWARE VERSION
        $VersionOut = Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath $VersionOut -Commands "version"            


        #Check for a match
        if ($VersionOut -notmatch $firmwareRegex)
        {
            $success = $false 
            $ErrorList += "Incorrect Firmware Version: " + $VersionOut +"`n"
        }
        else {
             $message = "Verified Firmware version."
             $logBuffer += Log -BuildNo $BuildNumber -File $output -Message $message
        }

        #PROJECT DATE (Program)
        $ProjectOut = Get-Telnet -RemoteHost "$InnerIP" -Port "$Port" -OutputPath $ProjectOut -Commands "cd \romdisk\user\display", "type .\~.LocalInfo.vtpage"

        if ($ProjectOut -notmatch $projectRegex)
        {
            $success = $false 
            $ErrorList += "Incorrect ProjectDate Version: " + $ProjectOut +"`n"
        }
        else {
             $message = "Verified Project Date."
             $logBuffer += Log -BuildNo $BuildNumber -File $output -Message $message 
        }


        #IPTABLES

        $VerifyIPTable = ".\IPtables\" + $H + "Verify_IPTable.csv"
        $VerifyParseIPTable = ".\IPtables\VerifyParseIPTable.csv"
        New-Item $VerifyIPTable -ItemType file -force
        New-Item $VerifyParseIPTable -ItemType file -force

        Get-Telnet -RemoteHost "$InnerIP" -Commands "iptable" -OutputPath $VerifyIPTable

    

        "CIP_ID Type Status Port IpAddress" | Add-Content $VerifyParseIPTable
        $ipTableHolder = ((Get-Content $VerifyIPTable | Where-Object {($_ -notmatch 'IP Table') -and ($_ -notmatch '-')}) -replace "\s+", " ")
        $ipTableHolder.Trim() | Add-Content $VerifyParseIPTable

        $verifyIpTable = Import-Csv $VerifyParseIPTable -Delimiter " "


        $compare = Compare-Object $verifyIpTable $iptable

        Write-Host("VERIFICATION DATA--------------------------------------------------------")
        Write-Host("VERSION: ")
        Write-Host($VersionOut)
        Write-Host("END VERSION")
        Write-Host("PROJECT: ")
        Write-Host($ProjectOut)
        Write-Host("END PROJECT")
        Write-Host("IPTABLE: ")
        Write-Host($VerifyIPTable)
        Write-Host("END IPTABLE")
        Write-Host("/VERIFICATION DATA--------------------------------------------------------")


        if (diff $verifyIpTable $iptable)
        {
            $success = $false 
            $ErrorList += "Incorrect IPTable : " + $VerifyIPTable +"`n"
        }
        else {
             $message = "Verified IPTable"  + $VerifyIPTable
             $logBuffer += Log -BuildNo $BuildNumber -File $output -Message $message
        }
    
        $logBuffer += $ErrorList
        Write-Host($logBuffer)

        $logToSend = ""
        $logBuffer | Foreach {
            $logToSend += $_
        }

        if($success -eq $true) {
            logToElk -Message "Updating TouchPanel" -BuildNo $BuildNumber -ActiveHostName $H -ActiveHostIp $InnerIP -ServerAddress $ELKServer -Success $success -Logs $logToSend
        } else {
            logToElk -Message "Updating TouchPanel" -BuildNo $BuildNumber -ActiveHostName $H -ActiveHostIp $InnerIP -ServerAddress $ELKServer -Success $success -Logs $logToSend
        }
    }
    catch{

        $logBuffer += Log -BuildNo $BuildNumber -File $output -Message $_
        $logToSend = ""
        $logBuffer | Foreach {
            $logToSend += $_
        }
        logToElk -Message "Updating TouchPanel" -BuildNo $BuildNumber -ActiveHostName $H -ActiveHostIp $InnerIP -ServerAddress $ELKServer -Success $false -Logs $logToSend
        throw $_
    }
}
