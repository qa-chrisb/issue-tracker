from pydantic import BaseModel

class Issue(BaseModel):
    title: str
    description: str
    email: str | None = None
    severity: str | None = None

class UpdateIssue(BaseModel):
    title: str
    description: str