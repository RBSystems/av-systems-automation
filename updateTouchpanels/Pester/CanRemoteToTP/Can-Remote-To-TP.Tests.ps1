$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$sut = (Split-Path -Leaf $MyInvocation.MyCommand.Path) -replace '\.Tests\.', '.'
. "$here\$sut"

Describe "Can-Remote-To-TP" {
    It "telnets to a touchpanel" {
        Can-Remote-To-TP | Should be $true
    }
}
