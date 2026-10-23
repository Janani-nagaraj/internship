import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from config import KEYCLOAK_JWKS_URL

security = HTTPBearer()
jwks_client = PyJWKClient(KEYCLOAK_JWKS_URL)


def verify_keycloak_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_exp": True, "verify_iss": False, "verify_aud": False},
        )
        return {
            "user_id": payload.get("sub"),
            "username": payload.get("preferred_username"),
            "name": payload.get("name"),
            "email": payload.get("email"),
            "roles": payload.get("realm_access", {}).get("roles", []),
    
               }
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid or expired Keycloak token: {exc}")
    except Exception:
        raise HTTPException(status_code=401, detail="Could not verify Keycloak token")


# ---------- Role-based access control ----------

def require_user_or_admin(user=Depends(verify_keycloak_token)):
    roles = user.get("roles", [])
    if "admin" not in roles and "user" not in roles:
        raise HTTPException(status_code=403, detail="Access denied. Admin or user role required.")
    return user


def require_admin(user=Depends(verify_keycloak_token)):
    if "admin" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="Access denied. Admin role required.")
    return user


def require_user(user=Depends(verify_keycloak_token)):
    roles = user.get("roles", [])
    if "user" not in roles or "admin" in roles:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Use the candidate's own token (role 'user', not admin).",
        )
    return user
