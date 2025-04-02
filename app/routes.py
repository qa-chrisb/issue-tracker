from fastapi import APIRouter, Form, Request, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services import list_github_issues, create_github_issue, get_github_issue, update_github_issue
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Index

@router.get("/", response_class=HTMLResponse)
async def list_issues(request: Request):
    issues = await list_github_issues()
    return templates.TemplateResponse("issues/list.html", {"request": request, "issues": issues})

@router.get("/create", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("issues/create.html", {"request": request})

# Issues

@router.post("/issue")
async def submit_feedback(
    title: str = Form(...),
    description: str = Form(...),
    email: str = Form(None),
    severity: str = Form(None)
):
    success = await create_github_issue(title, description, email, severity)
    if success:
        return RedirectResponse(url="thanks", status_code=303)
    else:
        return RedirectResponse(url="error", status_code=303)

@router.get("/issue/{issue_number}", response_class=HTMLResponse)
async def edit_issue(request: Request, issue_number: int = Path(...)):
    issue = await get_github_issue(issue_number)
    return templates.TemplateResponse("issues/edit.html", {"request": request, "issue": issue})

@router.post("/issue/{issue_number}")
async def update_issue(
    issue_number: int = Path(...),
    title: str = Form(...),
    description: str = Form(...)
):
    success = await update_github_issue(issue_number, title, description)
    if success:
        return RedirectResponse(url="thanks", status_code=303)
    else:
        return RedirectResponse(url="error", status_code=303)

# Status

@router.get("/thanks", response_class=HTMLResponse)
async def thanks(request: Request):
    return templates.TemplateResponse("status/thanks.html", {"request": request})

@router.get("/error", response_class=HTMLResponse)
async def error_page(request: Request):
    return templates.TemplateResponse("status/error.html", {"request": request})