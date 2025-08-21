from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from app import schemas, crud
from app.deps import get_db
from app.oracle_client import OracleClient
import logging
import pandas as pd
from io import BytesIO

router = APIRouter()
logger = logging.getLogger("api")

@router.get("/users/")
def get_all_users(
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password")
):
    oracle = OracleClient(instance_url, oracle_username, oracle_password)
    result = oracle.get_all_users()
    if not result.get("success"):
        logger.error(f"Oracle get_all_users failed: {result.get('error')}")
        raise HTTPException(status_code=502, detail=f"Oracle get_all_users failed: {result.get('error')}")
    return result.get("data")

@router.get("/users/download")
def download_all_users_excel(
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password")
):
    oracle = OracleClient(instance_url, oracle_username, oracle_password)
    result = oracle.get_all_users()
    if not result.get("success"):
        logger.error(f"Oracle get_all_users failed: {result.get('error')}")
        raise HTTPException(status_code=502, detail=f"Oracle get_all_users failed: {result.get('error')}")
    users = result.get("data", {}).get("Resources", [])
    rows = []
    for user in users:
        roles = user.get("roles", [])
        if roles:
            for role in roles:
                row = {
                    "userName": user.get("userName"),
                    "email": user.get("emails", [{}])[0].get("value") if user.get("emails") else None,
                    "firstName": user.get("name", {}).get("givenName"),
                    "lastName": user.get("name", {}).get("familyName"),
                    "displayName": user.get("displayName"),
                    "active": user.get("active"),
                    "userType": user.get("userType"),
                    "title": user.get("title"),
                    "organization": user.get("organization"),
                    "department": user.get("department"),
                    "manager": user.get("manager", {}).get("displayName") if user.get("manager") else None,
                    "created": user.get("meta", {}).get("created"),
                    "lastModified": user.get("meta", {}).get("lastModified"),
                    "externalId": user.get("externalId"),
                    "employeeNumber": user.get("employeeNumber"),
                    "costCenter": user.get("costCenter"),
                    "division": user.get("division"),
                    "role_value": role.get("value"),
                    "role_displayName": role.get("displayName"),
                    "role_description": role.get("description"),
                }
                rows.append(row)
        else:
            row = {
                "userName": user.get("userName"),
                "email": user.get("emails", [{}])[0].get("value") if user.get("emails") else None,
                "firstName": user.get("name", {}).get("givenName"),
                "lastName": user.get("name", {}).get("familyName"),
                "displayName": user.get("displayName"),
                "active": user.get("active"),
                "userType": user.get("userType"),
                "title": user.get("title"),
                "organization": user.get("organization"),
                "department": user.get("department"),
                "manager": user.get("manager", {}).get("displayName") if user.get("manager") else None,
                "created": user.get("meta", {}).get("created"),
                "lastModified": user.get("meta", {}).get("lastModified"),
                "externalId": user.get("externalId"),
                "employeeNumber": user.get("employeeNumber"),
                "costCenter": user.get("costCenter"),
                "division": user.get("division"),
                "role_value": None,
                "role_displayName": None,
                "role_description": None,
            }
            rows.append(row)
    df = pd.DataFrame(rows)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="oracle_users.xlsx"'
    }
    return Response(content=output.read(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@router.get("/users/{username}")
def get_user_from_oracle(
    username: str,
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password")
):
    oracle = OracleClient(instance_url, oracle_username, oracle_password)
    result = oracle.get_user(username)
    if not result.get("success"):
        logger.error(f"Oracle get_user failed: {result.get('error')}")
        raise HTTPException(status_code=502, detail=f"Oracle get_user failed: {result.get('error')}")
    # Flatten to only the specified fields, including roles
    users = result.get("data", {}).get("Resources", [])
    rows = []
    for user in users:
        roles = user.get("roles", [])
        if roles:
            for role in roles:
                row = {
                    "userName": user.get("userName"),
                    "email": user.get("emails", [{}])[0].get("value") if user.get("emails") else None,
                    "firstName": user.get("name", {}).get("givenName"),
                    "lastName": user.get("name", {}).get("familyName"),
                    "displayName": user.get("displayName"),
                    "active": user.get("active"),
                    "userType": user.get("userType"),
                    "title": user.get("title"),
                    "organization": user.get("organization"),
                    "department": user.get("department"),
                    "manager": user.get("manager", {}).get("displayName") if user.get("manager") else None,
                    "created": user.get("meta", {}).get("created"),
                    "lastModified": user.get("meta", {}).get("lastModified"),
                    "externalId": user.get("externalId"),
                    "employeeNumber": user.get("employeeNumber"),
                    "costCenter": user.get("costCenter"),
                    "division": user.get("division"),
                    "role_value": role.get("value"),
                    "role_displayName": role.get("displayName"),
                    "role_description": role.get("description"),
                }
                rows.append(row)
        else:
            row = {
                "userName": user.get("userName"),
                "email": user.get("emails", [{}])[0].get("value") if user.get("emails") else None,
                "firstName": user.get("name", {}).get("givenName"),
                "lastName": user.get("name", {}).get("familyName"),
                "displayName": user.get("displayName"),
                "active": user.get("active"),
                "userType": user.get("userType"),
                "title": user.get("title"),
                "organization": user.get("organization"),
                "department": user.get("department"),
                "manager": user.get("manager", {}).get("displayName") if user.get("manager") else None,
                "created": user.get("meta", {}).get("created"),
                "lastModified": user.get("meta", {}).get("lastModified"),
                "externalId": user.get("externalId"),
                "employeeNumber": user.get("employeeNumber"),
                "costCenter": user.get("costCenter"),
                "division": user.get("division"),
                "role_value": None,
                "role_displayName": None,
                "role_description": None,
            }
            rows.append(row)
    return rows

@router.get("/users/{username}/download")
def download_single_user_excel(
    username: str,
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password")
):
    oracle = OracleClient(instance_url, oracle_username, oracle_password)
    result = oracle.get_user(username)
    if not result.get("success"):
        logger.error(f"Oracle get_user failed: {result.get('error')}")
        raise HTTPException(status_code=502, detail=f"Oracle get_user failed: {result.get('error')}")
    users = result.get("data", {}).get("Resources", [])
    rows = []
    for user in users:
        roles = user.get("roles", [])
        if roles:
            for role in roles:
                row = {
                    "userName": user.get("userName"),
                    "email": user.get("emails", [{}])[0].get("value") if user.get("emails") else None,
                    "firstName": user.get("name", {}).get("givenName"),
                    "lastName": user.get("name", {}).get("familyName"),
                    "displayName": user.get("displayName"),
                    "active": user.get("active"),
                    "userType": user.get("userType"),
                    "title": user.get("title"),
                    "organization": user.get("organization"),
                    "department": user.get("department"),
                    "manager": user.get("manager", {}).get("displayName") if user.get("manager") else None,
                    "created": user.get("meta", {}).get("created"),
                    "lastModified": user.get("meta", {}).get("lastModified"),
                    "externalId": user.get("externalId"),
                    "employeeNumber": user.get("employeeNumber"),
                    "costCenter": user.get("costCenter"),
                    "division": user.get("division"),
                    "role_value": role.get("value"),
                    "role_displayName": role.get("displayName"),
                    "role_description": role.get("description"),
                }
                rows.append(row)
        else:
            row = {
                "userName": user.get("userName"),
                "email": user.get("emails", [{}])[0].get("value") if user.get("emails") else None,
                "firstName": user.get("name", {}).get("givenName"),
                "lastName": user.get("name", {}).get("familyName"),
                "displayName": user.get("displayName"),
                "active": user.get("active"),
                "userType": user.get("userType"),
                "title": user.get("title"),
                "organization": user.get("organization"),
                "department": user.get("department"),
                "manager": user.get("manager", {}).get("displayName") if user.get("manager") else None,
                "created": user.get("meta", {}).get("created"),
                "lastModified": user.get("meta", {}).get("lastModified"),
                "externalId": user.get("externalId"),
                "employeeNumber": user.get("employeeNumber"),
                "costCenter": user.get("costCenter"),
                "division": user.get("division"),
                "role_value": None,
                "role_displayName": None,
                "role_description": None,
            }
            rows.append(row)
    df = pd.DataFrame(rows)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    headers = {
        'Content-Disposition': f'attachment; filename="oracle_user_{username}.xlsx"'
    }
    return Response(content=output.read(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(payload: schemas.UserCreateWithOracle, db: Session = Depends(get_db)):
    # Call Oracle API
    oracle = OracleClient(payload.instance_url, payload.oracle_username, payload.oracle_password)
    oracle_result = oracle.create_user(payload.user.dict())
    if not oracle_result or not oracle_result.get("success"):
        error_msg = f"Oracle API call failed: {oracle_result.get('error')}"
        logger.error(error_msg)
        crud.create_log(
            db,
            action="create_user",
            username=payload.user.username,
            status="failed",
            message=error_msg + f" | Oracle response: {oracle_result.get('response')}"
        )
        raise HTTPException(status_code=502, detail=error_msg)
    # Create in local DB
    db_user = crud.get_user_by_username(db, payload.user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = crud.create_user(db, payload.user)
    crud.create_log(
        db,
        action="create_user",
        username=user.username,
        status="success",
        message="User created in Oracle and local DB. Oracle response: " + str(oracle_result.get('data'))
    )
    return user

@router.get("/logs/", response_model=list[schemas.LogResponse])
def get_logs(db: Session = Depends(get_db)):
    return db.query(crud.models.Log).all()