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
  --summary "Demand Analysis, Roadmap Planning, Schedule Arrangement & Sign-off Led by Product Manager" `
  --description "$desc" `
  --type "Story" `
  --project "MSCN" `
  --priority "Medium (migrated)" `
  --assignee "712020:79e689ed-9b94-4571-961c-3c3095fc5827" `
  --components "MSCN-DATA" `
  --parent "MSCN-2738"
