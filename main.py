from fastapi import FastAPI, Form, Request, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI()

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# Serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def list_issues(request: Request):
		async with httpx.AsyncClient() as client:
			resp = await client.get(
				f"https://api.github.com/repos/{GITHUB_REPO}/issues",
				headers={"Authorization": f"token {GITHUB_TOKEN}"}
			)
		issues = resp.json()
		return templates.TemplateResponse("issues.html", {"request": request, "issues": issues})

@app.get("/create", response_class=HTMLResponse)
async def form_page(request: Request):
	return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def submit_feedback(
	title: str = Form(...),
	description: str = Form(...),
	email: str = Form(None),
	severity: str = Form(None)
):
	issue_body = f"**Description:**\n{description}\n\n**Submitted by:** {email or 'Anonymous'}\n**Severity:** {severity or 'N/A'}"

	async with httpx.AsyncClient() as client:
		resp = await client.post(
			f"https://api.github.com/repos/{GITHUB_REPO}/issues",
			json={"title": title, "body": issue_body},
			headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
		)

	if resp.status_code == 201:
		return RedirectResponse(url="/thanks", status_code=303)
	else:
		print(resp.text)
		return RedirectResponse(url="/error", status_code=303)

@app.get("/issue/{issue_number}", response_class=HTMLResponse)
async def edit_issue(request: Request, issue_number: int = Path(...)):
	async with httpx.AsyncClient() as client:
		resp = await client.get(
			f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}",
			headers={"Authorization": f"token {GITHUB_TOKEN}"}
		)
	issue = resp.json()
	return templates.TemplateResponse("issue.html", {"request": request, "issue": issue})

@app.post("/issue/{issue_number}")
async def update_issue(
	issue_number: int = Path(...),
	title: str = Form(...),
	description: str = Form(...)
):
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
	if resp.status_code == 200:
		return RedirectResponse(url="/issues", status_code=303)
	else:
		return RedirectResponse(url="/error", status_code=303)

@app.get("/thanks", response_class=HTMLResponse)
async def thanks(request: Request):
	return templates.TemplateResponse("thanks.html", {"request": request})

@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request):
	return templates.TemplateResponse("error.html", {"request": request})
