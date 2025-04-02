# Technical Plan: Client-Facing Bug/Feedback Tracker (Python MVP)

## Overview
Build a lightweight web app that allows non-technical users to submit bug reports and feedback via a form. Submissions are turned into GitHub issues via the GitHub REST API.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: HTML + Tailwind CSS (via CDN)
- **Templates**: Jinja2
- **HTTP Client**: httpx
- **Deployment**: Render, Fly.io, Railway, or similar

## Folder Structure
```
project/
├── main.py
├── templates/
│   ├── form.html
│   ├── thanks.html
│   └── error.html
├── static/
│   └── (optional CSS/images)
├── requirements.txt
└── .env (for GITHUB_TOKEN)
```

## Core Features
- Feedback form at `/`
  - Title
  - Description
  - Optional email
  - Optional severity dropdown
- Form submission posts to `/submit`
- GitHub issue is created with formatted content
- Redirect to `/thanks` or `/error` depending on response

## API Endpoints
### GET `/`
- Returns `form.html`

### POST `/submit`
- Receives form data
- Calls GitHub API to create an issue
- Redirects to `/thanks` or `/error`

### GET `/thanks`
- Returns a success message

### GET `/error`
- Returns an error message

## GitHub API Integration
- Uses personal access token (`GITHUB_TOKEN`)
- Endpoint: `POST https://api.github.com/repos/:owner/:repo/issues`
- Required headers:
  ```json
  {
    "Authorization": "token <GITHUB_TOKEN>",
    "Accept": "application/vnd.github+json"
  }
  ```

## Environment Variables
- `GITHUB_TOKEN`: GitHub token with `repo` access
- `GITHUB_REPO`: Repository in the form `username/repo`

## Milestones (7-Day Plan)
| Day | Task |
|-----|------|
| 1   | Project setup, FastAPI + templates scaffold |
| 2   | Build form UI (form.html with Tailwind) |
| 3   | Connect form → `/submit` endpoint |
| 4   | Integrate GitHub API with `httpx` |
| 5   | Add thanks/error pages, basic error handling |
| 6   | Deploy to Render/Fly.io |
| 7   | Polish, test, and write docs |

## Future Enhancements
- File upload support (e.g. images)
- Email confirmation to submitter
- Admin dashboard to view recent submissions
- CAPTCHA/spam protection
- Self-hosted vs SaaS options

## License & Monetisation
- Start with MIT license or similar
- Offer hosted SaaS version with branding/custom domain support
- Add premium tier with analytics, integrations (Slack, Discord)

