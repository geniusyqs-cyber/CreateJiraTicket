param(
    [string]$Summary = "[Bug] Missing Archive Data for hk.item_master & hk.item_price_ma Caused factordb.idea-lists DAG Failure",
    [string]$DescriptionFile = ".\description.txt",
    [string]$Labels = "",
    [string]$Priority = "High (migrated)",
    [string]$Assignee = "",
    [string]$Components = "MSCN-DATA",
    [string]$Parent = "MSCN-2738"
)

if (-not (Test-Path $DescriptionFile)) {
    Write-Error "Description file not found: $DescriptionFile"
    exit 1
}

if (-not $env:JIRA_API_TOKEN) {
    Write-Error "Environment variable JIRA_API_TOKEN is not set. Please set it and retry."
    exit 1
}

if (-not $env:JIRA_EMAIL) {
    Write-Error "Environment variable JIRA_EMAIL is not set. Please set it and retry."
    exit 1
}

$desc = Get-Content $DescriptionFile -Raw

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Error "Python not found or not available. Please install Python and ensure 'python' is in PATH."
    exit 1
}

$pythonExe = $pythonCmd.Source
$script = ".\create_mscn_bug_ticket.py"
$args = @(
    "--summary", $Summary,
    "--description", $desc,
    "--type", "Bug",
    "--project", "MSCN"
)

if (-not [string]::IsNullOrWhiteSpace($Priority)) {
    $args += "--priority"
    $args += $Priority
}
if (-not [string]::IsNullOrWhiteSpace($Assignee)) {
    $args += "--assignee"
    $args += $Assignee
}
if (-not [string]::IsNullOrWhiteSpace($Labels)) {
    $args += "--labels"
    $args += $Labels
}
if (-not [string]::IsNullOrWhiteSpace($Components)) {
    $args += "--components"
    $args += $Components
}
if (-not [string]::IsNullOrWhiteSpace($Parent)) {
     $args += "--parent"
     $args += $Parent
}

try {
    Write-Host "Running: $pythonExe $script $($args -join ' ')"
    $output = & $pythonExe $script @args 2>&1
    $exit = $LASTEXITCODE
    if ($output) { Write-Host $output }
    if ($exit -ne 0) {
        Write-Error "create_mscn_bug_ticket.py returned non-zero exit code: $exit"
        exit $exit
    }
    Write-Host "Bug ticket created successfully."
} catch {
    Write-Error "Error executing bug creation script: $_"
    exit 1
}
