import httpx
import os

GITHUB_TOKEN = os.getenv("TOKEN")
GITHUB_REPO = os.getenv("REPO")

async def list_github_issues():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/issues",
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
    issues = resp.json()
    # Filter out pull requests
    filtered_issues = [issue for issue in issues if "pull_request" not in issue]
    return filtered_issues

async def create_github_issue(title, description, email, severity):
    issue_body = f"**Description:**\n{description}\n\n**Submitted by:** {email or 'Anonymous'}\n**Severity:** {severity or 'N/A'}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.github.com/repos/{GITHUB_REPO}/issues",
            json={"title": title, "body": issue_body},
            headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
        )
    return resp.status_code == 201

async def get_github_issue(issue_number):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}",
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
    return resp.json()

async def update_github_issue(issue_number, title, description):
    update_payload = {
        "title": title,
        "body": description
    }
    async with httpx.AsyncClient() as client:
        resp = await client.patch(
            f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}",
            json=update_payload,
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
    return resp.status_code == 200