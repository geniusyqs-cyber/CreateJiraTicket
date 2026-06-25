param(
    [string]$DescriptionFile = ".\description.txt"
)

if (-not (Test-Path $DescriptionFile)) {
    Write-Error "Description file not found: $DescriptionFile"
    exit 1
}

if (-not $env:JIRA_API_TOKEN) {
    Write-Error "环境变量 JIRA_API_TOKEN 未设置。请先设置后再运行。"
    exit 1
}

if (-not $env:JIRA_EMAIL) {
    Write-Error "环境变量 JIRA_EMAIL 未设置。请先设置后再运行。"
    exit 1
}

$desc = Get-Content $DescriptionFile -Raw

python .\create_mscn_ticket.py `
  --summary "Panaray Data File Generation Failure - Empty Single Metric Causes Postgres Integer Type Conversion Error" `
  --description "$desc" `
  --type "Story" `
  --project "MSCN" `
  --priority "Medium (migrated)" `
  --assignee "5b43012c27c98e2ce5156c54" `
  --components "MSCN-DATA" `
  --parent "MSCN-2738"
