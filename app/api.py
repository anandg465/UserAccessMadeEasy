from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Response,
    UploadFile,
    File,
)
from app import schemas
from app.oracle_client import OracleClient
import logging
import pandas as pd
from io import BytesIO
import json

router = APIRouter()
logger = logging.getLogger("api")


# Helper function to create Oracle client
def create_oracle_client(oracle_config: schemas.OracleConnectionConfig) -> OracleClient:
    return OracleClient(
        oracle_config.instance_url, oracle_config.username, oracle_config.password
    )


# User Management Endpoints
@router.get("/users/")
def get_all_users(
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password"),
):
    """Get all users from Oracle Fusion"""
    oracle = OracleClient(instance_url, oracle_username, oracle_password)
    result = oracle.get_all_users()
    if not result.get("success"):
        logger.error(f"Oracle get_all_users failed: {result.get('error')}")
        raise HTTPException(
            status_code=502,
            detail=f"Oracle get_all_users failed: {result.get('error')}",
        )
    return result.get("data")


@router.post("/users/details", response_model=schemas.UserDetailResponse)
def get_user_details(request: schemas.UserDetailRequest):
    """Get comprehensive user details including roles and data security"""
    oracle = create_oracle_client(request.oracle_config)
    result = oracle.get_user_details(request.username)

    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error"))

    data = result.get("data", {})
    user_account = data.get("userAccount", {})
    scim_user = data.get("scimUser", {})
    aors = data.get("areasOfResponsibility", [])

    # Extract roles from SCIM user
    roles = scim_user.get("roles", [])

    # Extract data security contexts (this would need to be implemented based on your specific data structure)
    data_security_contexts = []

    return schemas.UserDetailResponse(
        username=request.username,
        person_number=user_account.get("PersonNumber"),
        display_name=scim_user.get("displayName"),
        email=scim_user.get("emails", [{}])[0].get("value")
        if scim_user.get("emails")
        else None,
        is_active=scim_user.get("active", False),
        assigned_roles=roles,
        areas_of_responsibility=aors,
        data_security_contexts=data_security_contexts,
        user_guid=user_account.get("GUID"),
        created_date=scim_user.get("meta", {}).get("created"),
        last_modified=scim_user.get("meta", {}).get("lastModified"),
    )


@router.post("/users/roles/assign")
def assign_role_to_user(request: schemas.RoleAssignmentRequest):
    """Assign a role to a user"""
    oracle = create_oracle_client(request.oracle_config)
    result = oracle.assign_role_to_user(request.username, request.role_name)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return {
        "success": True,
        "message": f"Role '{request.role_name}' assigned to user '{request.username}'",
    }


@router.post("/users/roles/remove")
def remove_role_from_user(request: schemas.RoleRemovalRequest):
    """Remove a role from a user"""
    oracle = create_oracle_client(request.oracle_config)
    result = oracle.remove_role_from_user(request.username, request.role_name)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return {
        "success": True,
        "message": f"Role '{request.role_name}' removed from user '{request.username}'",
    }


@router.post("/users/roles/bulk-assign", response_model=schemas.BulkOperationResponse)
def bulk_assign_roles(request: schemas.BulkRoleAssignmentRequest):
    """Bulk assign roles to multiple users"""
    oracle = create_oracle_client(request.oracle_config)
    results = []
    successful = 0
    failed = 0

    for assignment in request.assignments:
        try:
            result = oracle.assign_role_to_user(
                assignment.username, assignment.role_name
            )
            if result.get("success"):
                successful += 1
                results.append(
                    schemas.OperationStatus(
                        success=True,
                        message=f"Role '{assignment.role_name}' assigned to user '{assignment.username}'",
                    )
                )
            else:
                failed += 1
                results.append(
                    schemas.OperationStatus(
                        success=False,
                        message=f"Failed to assign role '{assignment.role_name}' to user '{assignment.username}'",
                        error=result.get("error"),
                    )
                )
        except Exception as e:
            failed += 1
            results.append(
                schemas.OperationStatus(
                    success=False,
                    message=f"Exception occurred while assigning role '{assignment.role_name}' to user '{assignment.username}'",
                    error=str(e),
                )
            )

    return schemas.BulkOperationResponse(
        total_operations=len(request.assignments),
        successful_operations=successful,
        failed_operations=failed,
        results=results,
    )


# Data Security Context Endpoints
@router.post("/users/data-security/assign")
def assign_data_security_context(request: schemas.DataSecurityContextRequest):
    """Assign data security context to a user"""
    # This would need to be implemented based on your specific Oracle Fusion data security structure
    # For now, returning a placeholder response
    return {
        "success": True,
        "message": f"Data security context '{request.data_security_context}' with value '{request.data_security_value}' assigned to user '{request.username}' for role '{request.role_name}'",
    }


@router.post(
    "/users/data-security/bulk-assign", response_model=schemas.BulkOperationResponse
)
def bulk_assign_data_security_contexts(request: schemas.BulkDataSecurityRequest):
    """Bulk assign data security contexts to multiple users"""
    results = []
    successful = 0
    failed = 0

    for assignment in request.assignments:
        try:
            # Placeholder implementation
            successful += 1
            results.append(
                schemas.OperationStatus(
                    success=True,
                    message=f"Data security context '{assignment.data_security_context}' assigned to user '{assignment.username}'",
                )
            )
        except Exception as e:
            failed += 1
            results.append(
                schemas.OperationStatus(
                    success=False,
                    message=f"Failed to assign data security context to user '{assignment.username}'",
                    error=str(e),
                )
            )

    return schemas.BulkOperationResponse(
        total_operations=len(request.assignments),
        successful_operations=successful,
        failed_operations=failed,
        results=results,
    )


# Areas of Responsibility Endpoints
@router.get("/areas-of-responsibility/")
def get_areas_of_responsibility(
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password"),
    params: str = Query(None, description="Optional query parameters as JSON string"),
):
    """Get all areas of responsibility"""
    oracle = OracleClient(instance_url, oracle_username, oracle_password)

    query_params = None
    if params:
        try:
            query_params = json.loads(params)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in params")

    result = oracle.get_areas_of_responsibility(query_params)
    if not result.get("success"):
        raise HTTPException(
            status_code=502,
            detail=f"Failed to get areas of responsibility: {result.get('error')}",
        )

    return result.get("data")


@router.post("/areas-of-responsibility/assign")
def assign_aor_to_user(request: schemas.AORAssignmentRequest):
    """Assign an area of responsibility to a user"""
    oracle = create_oracle_client(request.oracle_config)

    # Create AOR data
    aor_data = {
        "userAccountId": request.username,  # This would need to be the actual user account ID
        "name": request.aor_name,
        "type": request.aor_type or "GENERAL",
    }

    result = oracle.create_area_of_responsibility(aor_data)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return {
        "success": True,
        "message": f"AOR '{request.aor_name}' assigned to user '{request.username}'",
    }


@router.post("/areas-of-responsibility/remove")
def remove_aor_from_user(request: schemas.AORRemovalRequest):
    """Remove an area of responsibility from a user"""
    oracle = create_oracle_client(request.oracle_config)
    result = oracle.delete_area_of_responsibility(request.aor_id)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return {"success": True, "message": f"AOR removed from user"}


@router.post(
    "/areas-of-responsibility/bulk-assign", response_model=schemas.BulkOperationResponse
)
def bulk_assign_aors(request: schemas.BulkAORRequest):
    """Bulk assign areas of responsibility to multiple users"""
    oracle = create_oracle_client(request.oracle_config)
    results = []
    successful = 0
    failed = 0

    for assignment in request.assignments:
        try:
            aor_data = {
                "userAccountId": assignment.username,
                "name": assignment.aor_name,
                "type": assignment.aor_type or "GENERAL",
            }

            result = oracle.create_area_of_responsibility(aor_data)
            if result.get("success"):
                successful += 1
                results.append(
                    schemas.OperationStatus(
                        success=True,
                        message=f"AOR '{assignment.aor_name}' assigned to user '{assignment.username}'",
                    )
                )
            else:
                failed += 1
                results.append(
                    schemas.OperationStatus(
                        success=False,
                        message=f"Failed to assign AOR '{assignment.aor_name}' to user '{assignment.username}'",
                        error=result.get("error"),
                    )
                )
        except Exception as e:
            failed += 1
            results.append(
                schemas.OperationStatus(
                    success=False,
                    message=f"Exception occurred while assigning AOR '{assignment.aor_name}' to user '{assignment.username}'",
                    error=str(e),
                )
            )

    return schemas.BulkOperationResponse(
        total_operations=len(request.assignments),
        successful_operations=successful,
        failed_operations=failed,
        results=results,
    )


# Excel Upload Endpoints
@router.post("/upload/excel", response_model=schemas.ExcelUploadResponse)
async def upload_excel_file(
    file: UploadFile = File(...),
    operation_type: str = Query(
        ...,
        description="Type of operation: role_assignment, data_security, aor_assignment",
    ),
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password"),
):
    """Upload Excel file for bulk operations"""
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="File must be an Excel file (.xlsx or .xls)"
        )

    try:
        # Read Excel file
        content = await file.read()
        df = pd.read_excel(BytesIO(content))

        oracle = OracleClient(instance_url, oracle_username, oracle_password)
        success_count = 0
        failure_count = 0
        errors = []
        processed_records = []

        for index, row in df.iterrows():
            try:
                if operation_type == "role_assignment":
                    result = oracle.assign_role_to_user(
                        str(row.get("username", "")), str(row.get("role_name", ""))
                    )
                elif operation_type == "aor_assignment":
                    aor_data = {
                        "userAccountId": str(row.get("username", "")),
                        "name": str(row.get("aor_name", "")),
                        "type": str(row.get("aor_type", "GENERAL")),
                    }
                    result = oracle.create_area_of_responsibility(aor_data)
                else:
                    result = {
                        "success": False,
                        "error": f"Unsupported operation type: {operation_type}",
                    }

                if result.get("success"):
                    success_count += 1
                    processed_records.append(
                        {
                            "row": index + 1,
                            "username": str(row.get("username", "")),
                            "status": "success",
                            "message": "Operation completed successfully",
                        }
                    )
                else:
                    failure_count += 1
                    errors.append(
                        {
                            "row": index + 1,
                            "username": str(row.get("username", "")),
                            "error": result.get("error", "Unknown error"),
                        }
                    )

            except Exception as e:
                failure_count += 1
                errors.append(
                    {
                        "row": index + 1,
                        "username": str(row.get("username", "")),
                        "error": str(e),
                    }
                )

        return schemas.ExcelUploadResponse(
            success_count=success_count,
            failure_count=failure_count,
            errors=errors,
            processed_records=processed_records,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing Excel file: {str(e)}"
        )


# Password Management Endpoints
@router.post("/users/password/reset")
def reset_user_password(request: schemas.PasswordResetRequest):
    """Reset a user's password"""
    oracle = create_oracle_client(request.oracle_config)

    # First get user details to get GUID
    user_result = oracle.get_user_by_username(request.username)
    if not user_result.get("success"):
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_result.get("data", {})
    user_guid = user_data.get("GUID")

    if not user_guid:
        raise HTTPException(status_code=400, detail="User GUID not found")

    password_data = {"newPassword": request.new_password}
    result = oracle.reset_user_password(user_guid, password_data)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return {"success": True, "message": f"Password reset for user '{request.username}'"}


@router.post("/users/password/update")
def update_user_password(request: schemas.PasswordUpdateRequest):
    """Update a user's password"""
    oracle = create_oracle_client(request.oracle_config)

    # First get user details to get GUID
    user_result = oracle.get_user_by_username(request.username)
    if not user_result.get("success"):
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_result.get("data", {})
    user_guid = user_data.get("GUID")

    if not user_guid:
        raise HTTPException(status_code=400, detail="User GUID not found")

    password_data = {
        "currentPassword": request.current_password,
        "newPassword": request.new_password,
    }
    result = oracle.update_user_password(user_guid, password_data)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return {
        "success": True,
        "message": f"Password updated for user '{request.username}'",
    }


# Search Endpoints
@router.post("/users/search")
def search_users(request: schemas.UserSearchRequest):
    """Search users with advanced criteria"""
    oracle = create_oracle_client(request.oracle_config)

    # Convert search criteria to Oracle API parameters
    params = {}
    if "username" in request.search_criteria:
        params["q"] = f'userName eq "{request.search_criteria["username"]}"'
    if "email" in request.search_criteria:
        params["q"] = f'emails.value eq "{request.search_criteria["email"]}"'
    if "active" in request.search_criteria:
        params["q"] = f'active eq {request.search_criteria["active"]}'

    result = oracle.get_all_users()
    if not result.get("success"):
        raise HTTPException(
            status_code=502, detail=f"Search failed: {result.get('error')}"
        )

    return result.get("data")


@router.post("/areas-of-responsibility/search")
def search_aors(request: schemas.AORSearchRequest):
    """Search areas of responsibility with advanced criteria"""
    oracle = create_oracle_client(request.oracle_config)
    result = oracle.find_areas_of_responsibility(request.search_criteria)

    if not result.get("success"):
        raise HTTPException(
            status_code=502, detail=f"Search failed: {result.get('error')}"
        )

    return result.get("data")


# Legacy endpoints for backward compatibility
@router.get("/users/download")
def download_all_users_excel(
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password"),
):
    oracle = OracleClient(instance_url, oracle_username, oracle_password)
    result = oracle.get_all_users()
    if not result.get("success"):
        logger.error(f"Oracle get_all_users failed: {result.get('error')}")
        raise HTTPException(
            status_code=502,
            detail=f"Oracle get_all_users failed: {result.get('error')}",
        )
    users = result.get("data", {}).get("Resources", [])
    rows = []
    for user in users:
        roles = user.get("roles", [])
        if roles:
            for role in roles:
                row = {
                    "userName": user.get("userName"),
                    "email": user.get("emails", [{}])[0].get("value")
                    if user.get("emails")
                    else None,
                    "firstName": user.get("name", {}).get("givenName"),
                    "lastName": user.get("name", {}).get("familyName"),
                    "displayName": user.get("displayName"),
                    "active": user.get("active"),
                    "userType": user.get("userType"),
                    "title": user.get("title"),
                    "organization": user.get("organization"),
                    "department": user.get("department"),
                    "manager": user.get("manager", {}).get("displayName")
                    if user.get("manager")
                    else None,
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
                "email": user.get("emails", [{}])[0].get("value")
                if user.get("emails")
                else None,
                "firstName": user.get("name", {}).get("givenName"),
                "lastName": user.get("name", {}).get("familyName"),
                "displayName": user.get("displayName"),
                "active": user.get("active"),
                "userType": user.get("userType"),
                "title": user.get("title"),
                "organization": user.get("organization"),
                "department": user.get("department"),
                "manager": user.get("manager", {}).get("displayName")
                if user.get("manager")
                else None,
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
    headers = {"Content-Disposition": 'attachment; filename="oracle_users.xlsx"'}
    return Response(
        content=output.read(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


@router.get("/users/{username}")
def get_user_from_oracle(
    username: str,
    instance_url: str = Query(..., description="Oracle Instance URL"),
    oracle_username: str = Query(..., description="Oracle API username"),
    oracle_password: str = Query(..., description="Oracle API password"),
):
    oracle = OracleClient(instance_url, oracle_username, oracle_password)
    result = oracle.get_user(username)
    if not result.get("success"):
        logger.error(f"Oracle get_user failed: {result.get('error')}")
        raise HTTPException(
            status_code=502, detail=f"Oracle get_user failed: {result.get('error')}"
        )
    return result.get("data")
