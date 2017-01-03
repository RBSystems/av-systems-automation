##############
# Title: buildOldFileList.ps1
# Author: DGC
# Description: Build a list of files older than specified time period
###############

$fourMonths = (Get-Date).AddDays(-120)
$tmpPaths = @("D:\trmp")
$encodesPath = "D:\CR"
$manifestPath = "D:\reaper"

# Find all files older than (4 * 30) days
$encodesArr = Get-ChildItem $encodesPath -Recurse | Where-Object {$_.LastWriteTime -lt $fourMonths}

# Create list to use as path store
$fourMonthEncodes = New-Object System.Collections.ArrayList($null)

# For each "permanent" artifact, get actual file path
$fourMonthEncodesArr | ForEach-Object {
    $fourMonthEncodes.Add($_.FullName)
}


# Export output as csv
$manifest = Join-Path -Path $manifestPath -ChildPath "fourMonth.csv"
$fourMonthEncodes | export-csv $fourMonthManifest -NoTypeInformation
