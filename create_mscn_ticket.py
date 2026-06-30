#!/usr/bin/env python3
"""Create Jira issues in the WON China - MarketSmithChina project (MSCN)."""

import argparse
import os
import sys
import time

try:
    import requests
except ImportError:
    sys.exit("请先安装依赖: pip install -r requirements.txt")


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"请先设置环境变量 {name}")
    return value


def parse_list(value: str):
    return [item.strip() for item in value.split(",") if item.strip()]


def build_description(description: str) -> dict:
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": description}
                ],
            }
        ],
    }


def send_request_with_retry(
    method: str,
    url: str,
    max_retries: int,
    timeout: int,
    **kwargs,
) -> requests.Response:
    for attempt in range(1, max_retries + 1):
        try:
            return requests.request(method, url, timeout=timeout, **kwargs)
        except requests.exceptions.ReadTimeout:
            if attempt == max_retries:
                raise
            wait = 2 ** (attempt - 1)
            print(
                f"请求超时，正在重试 {attempt}/{max_retries}，等待 {wait} 秒...",
                file=sys.stderr,
            )
            time.sleep(wait)
        except requests.exceptions.RequestException as exc:
            if attempt == max_retries:
                raise
            wait = 2 ** (attempt - 1)
            print(
                f"请求失败 ({exc.__class__.__name__})，正在重试 {attempt}/{max_retries}，等待 {wait} 秒...",
                file=sys.stderr,
            )
            time.sleep(wait)


def create_issue(
    base_url: str,
    email: str,
    api_token: str,
    project_key: str,
    summary: str,
    description: str,
    issuetype: str,
    priority: str = None,
    assignee: str = None,
    labels: str = "",
    components: str = "",
    fix_versions: str = "",
    parent: str = "",
    timeout: int = 30,
    max_retries: int = 3,
) -> dict:
    url = base_url.rstrip("/") + "/rest/api/3/issue"
    fields = {
        "project": {"key": project_key},
        "summary": summary,
        "description": build_description(description),
        "issuetype": {"name": issuetype},
    }
    if priority:
        fields["priority"] = {"name": priority}
    if assignee:
        fields["assignee"] = {"accountId": assignee}
    if labels:
        fields["labels"] = parse_list(labels)
    if components:
        fields["components"] = [{"name": name} for name in parse_list(components)]
    if fix_versions:
        fields["fixVersions"] = [{"name": name} for name in parse_list(fix_versions)]
    if parent:
        fields["parent"] = {"key": parent}
    payload = {"fields": fields}
    response = send_request_with_retry(
        "post",
        url,
        auth=(email, api_token),
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
        max_retries=max_retries,
    )
    if response.status_code not in (200, 201):
        raise SystemExit(
            f"创建 Jira issue 失败: {response.status_code}\n{response.text}"
        )
    return response.json()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="在 WON China - MarketSmithChina (MSCN) 下创建 Jira ticket")
    parser.add_argument("--summary", required=True, help="Ticket 标题")
    parser.add_argument("--description", default="", help="Ticket 描述")
    parser.add_argument("--type", default="Story", help="Issue Type，默认 Story")
    parser.add_argument(
        "--project", default="MSCN", help="Jira Project Key，默认 MSCN"
    )
    parser.add_argument(
        "--url",
        default="https://daicompanies.atlassian.net",
        help="Jira 基础 URL，默认 https://daicompanies.atlassian.net",
    )
    parser.add_argument("--priority", default=None, help="Priority, 如 Medium")
    parser.add_argument(
        "--assignee",
        default=None,
        help="Assignee accountId（Jira Cloud），例如 5b10a2844c20165700ede21g",
    )
    parser.add_argument(
        "--labels",
        default="",
        help="Comma-separated labels，例如 bug,backend",
    )
    parser.add_argument(
        "--components",
        default="",
        help="Comma-separated component names",
    )
    parser.add_argument(
        "--fix-versions",
        default="",
        help="Comma-separated fix version names",
    )
    parser.add_argument(
        "--parent",
        default="",
        help="Parent issue key（如 MSCN-123）",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="请求超时时间（秒），默认 30",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="请求失败时重试次数，默认 3",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    email = get_env("JIRA_EMAIL")
    api_token = get_env("JIRA_API_TOKEN")
    issue = create_issue(
        base_url=args.url,
        email=email,
        api_token=api_token,
        project_key=args.project,
        summary=args.summary,
        description=args.description,
        issuetype=args.type,
        priority=args.priority,
        assignee=args.assignee,
        labels=args.labels,
        components=args.components,
        fix_versions=args.fix_versions,
        parent=args.parent,
        timeout=args.timeout,
        max_retries=args.retries,
    )
    issue_key = issue.get("key")
    issue_url = f"{args.url.rstrip('/')}/browse/{issue_key}" if issue_key else None
    print("创建成功:")
    print(f"  Issue Key: {issue_key}")
    if issue_url:
        print(f"  URL: {issue_url}")


if __name__ == "__main__":
    main()
