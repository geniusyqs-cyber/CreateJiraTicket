param(
    [string]$Summary = "DAIAI Story ticket summary",
    [string]$Description = "",
    [string]$DescriptionFile = ".\description.txt"
)

if (-not $env:JIRA_API_TOKEN) {
    Write-Error "环境变量 JIRA_API_TOKEN 未设置。请先设置后再运行。"
    exit 1
}

if (-not $env:JIRA_EMAIL) {
    Write-Error "环境变量 JIRA_EMAIL 未设置。请先设置后再运行。"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($Description)) {
    if (-not (Test-Path $DescriptionFile)) {
        Write-Error "Description file not found: $DescriptionFile"
        exit 1
    }
    $Description = Get-Content $DescriptionFile -Raw
}

python .\create_daiai_ticket.py `
  --summary "$Summary" `
  --description "$Description" `
  --type "Story" `
  --project "DAIAI"
