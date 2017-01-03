$fourMonths = (Get-Date).AddDays(-120)
$eighteenMonths = (Get-Date).AddDays(-540)
$tmpPaths = @("D:\trmp")
$encodesPath = "D:\CR"
$manifestPath = "D:\reaper"

$encodesArr = Get-ChildItem $encodesPath -Recurse | Where-Object {$_.LastWriteTime -lt $fourMonths}

$fourMonthEncodes = New-Object System.Collections.ArrayList($null)

#TMPs
$tmpPaths | ForEach-Object {
    $obj = $_
    $tempArr = Get-ChildItem $obj -Recurse | Where-Object {$_.LastWriteTime -lt $fourMonths}

    $tempArr | ForEach-Object {
        $fourMonthEncodes_tmp.Add($_.FullName)
    }
}

#Four Month Profile
$fourMonthEncodesArr | ForEach-Object {
    $fourMonthEncodes.Add($_.FullName)
}


$manifest = Join-Path -Path $manifestPath -ChildPath "fourMonth.csv"

$fourMonthEncodes | export-csv $fourMonthManifest -NoTypeInformation
