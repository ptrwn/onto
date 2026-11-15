import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI(title="Story Knowledge Graph API")

bearer_scheme = HTTPBearer(auto_error=False)


def verify_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    expected_token = os.getenv("API_TOKEN")

    if not expected_token:
        raise RuntimeError("API_TOKEN is not configured")

    if credentials is None or not secrets.compare_digest(
        credentials.credentials,
        expected_token,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/foo", dependencies=[Depends(verify_token)])
async def foo():
    return "bar"


@app.get("/health")
async def health():
    return {"status": "ok"}
