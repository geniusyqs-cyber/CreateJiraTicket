# Create Jira Ticket for WON China - MarketSmithChina

这是一个简单脚本，用于在 Jira 项目 `MSCN` 下自动创建 ticket。

## 准备

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 设置环境变量：

- `JIRA_EMAIL`：你的 Atlassian 登录邮箱
- `JIRA_API_TOKEN`：Jira API Token

例如：

```bash
setx JIRA_EMAIL "your-email@example.com"
setx JIRA_API_TOKEN "your-api-token"
```

## 使用方法

```bash
python create_mscn_ticket.py --summary "示例 Ticket 标题" --description "这是一个自动创建的 Jira ticket。"
```

如果你要修改 Jira 项目或 issue 类型：

```bash
python create_mscn_ticket.py --summary "新需求" --description "请处理市场分析需求。" --type "Story" --project MSCN
```

如果你要在 AI EchoSage (DAIAI) 下创建 Story：

```bash
python create_daiai_ticket.py --summary "示例 Story 标题" --description "这是一个自动创建的 AI EchoSage Story ticket。"
```

如果 `MSCN` 需要额外字段，可以用这些参数：

```bash
python create_mscn_ticket.py --summary "新需求" --description "详细描述" \
  --priority "Medium" \
  --assignee "5b10a2844c20165700ede21g" \
  --labels "backend,urgent" \
  --components "Web,API" \
  --fix-versions "v1.0,v1.1"
```

## 默认值

- Jira URL: `https://daicompanies.atlassian.net`
- Project Key: `MSCN`
- Issue Type: `Story`

## 备注

该脚本会调用 Jira Cloud REST API：`POST /rest/api/3/issue`。
如果需要更多字段，可以在 `create_jira_ticket.py` 中扩展 `payload`。
