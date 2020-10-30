function Add-Watcher {
    param(
        [String] $Path = ".",
        [String] $FileFilter = "*"
    )

    $AttributeFilter = [IO.NotifyFilters]::FileName,
                       [IO.NotifyFilters]::LastWrite
    $ChangeTypes = [System.IO.WatcherChangeTypes]::All
    $Timeout = 1000

    try {
        $watcher = New-Object `
            -TypeName IO.FileSystemWatcher `
            -ArgumentList $Path, $FileFilter `
            -Property @{
                IncludeSubdirectories = $true
                NotifyFilter = $AttributeFilter
            }

        do {
            $result = $watcher.WaitForChanged($ChangeTypes, $Timeout)
            if ($result.TimedOut) { continue }

            Invoke-Action -Change $result
        } while ($true)
    } finally {
        $watcher.Dispose()
    }
}

function Invoke-Action {
    param (
        [Parameter(Mandatory)]
        [System.IO.WaitForChangedResult] $ChangeInformation
    )

    tox -e linting,py -p auto -o
}


Add-Watcher -FileFilter *.py
