from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    is_active: Optional[bool] = True
    user_category: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserCreateWithOracle(BaseModel):
    user: UserCreate
    oracle_username: str
    oracle_password: str

class UserResponse(UserBase):
    id: int
    guid: Optional[str]
    class Config:
        orm_mode = True

class LogResponse(BaseModel):
    id: int
    action: str
    username: Optional[str]
    status: str
    message: Optional[str]
    timestamp: datetime
    class Config:
        orm_mode = True

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class Config:
        orm_mode = True

# New schemas for Oracle Fusion HCM User Management
class OracleConnectionConfig(BaseModel):
    instance_url: str = Field(..., description="Oracle Fusion instance URL")
    username: str = Field(..., description="Oracle API username")
    password: str = Field(..., description="Oracle API password")

class UserDetailRequest(BaseModel):
    username: str = Field(..., description="Username to get details for")
    oracle_config: OracleConnectionConfig

class UserDetailResponse(BaseModel):
    username: str
    person_number: Optional[str]
    display_name: Optional[str]
    email: Optional[str]
    is_active: bool
    assigned_roles: List[Dict[str, Any]]
    areas_of_responsibility: List[Dict[str, Any]]
    data_security_contexts: List[Dict[str, Any]]
    user_guid: Optional[str]
    created_date: Optional[str]
    last_modified: Optional[str]

class RoleAssignmentRequest(BaseModel):
    username: str = Field(..., description="Username to assign role to")
    role_name: str = Field(..., description="Role name to assign")
    oracle_config: OracleConnectionConfig

class RoleRemovalRequest(BaseModel):
    username: str = Field(..., description="Username to remove role from")
    role_name: str = Field(..., description="Role name to remove")
    oracle_config: OracleConnectionConfig

class BulkRoleAssignmentRequest(BaseModel):
    assignments: List[RoleAssignmentRequest]
    oracle_config: OracleConnectionConfig

class DataSecurityContextRequest(BaseModel):
    username: str = Field(..., description="Username to assign data security context to")
    role_name: str = Field(..., description="Role name")
    data_security_context: str = Field(..., description="Data security context name")
    data_security_value: str = Field(..., description="Data security context value")
    oracle_config: OracleConnectionConfig

class BulkDataSecurityRequest(BaseModel):
    assignments: List[DataSecurityContextRequest]
    oracle_config: OracleConnectionConfig

class AORAssignmentRequest(BaseModel):
    username: str = Field(..., description="Username to assign AOR to")
    aor_name: str = Field(..., description="Area of Responsibility name")
    aor_type: Optional[str] = Field(None, description="Type of AOR")
    oracle_config: OracleConnectionConfig

class AORRemovalRequest(BaseModel):
    username: str = Field(..., description="Username to remove AOR from")
    aor_id: str = Field(..., description="Area of Responsibility ID")
    oracle_config: OracleConnectionConfig

class BulkAORRequest(BaseModel):
    assignments: List[AORAssignmentRequest]
    oracle_config: OracleConnectionConfig

class ExcelUploadRequest(BaseModel):
    file_content: str = Field(..., description="Base64 encoded Excel file content")
    operation_type: str = Field(..., description="Type of operation: role_assignment, data_security, aor_assignment")
    oracle_config: OracleConnectionConfig

class ExcelUploadResponse(BaseModel):
    success_count: int
    failure_count: int
    errors: List[Dict[str, Any]]
    processed_records: List[Dict[str, Any]]

class PasswordResetRequest(BaseModel):
    username: str = Field(..., description="Username to reset password for")
    new_password: str = Field(..., description="New password")
    oracle_config: OracleConnectionConfig

class PasswordUpdateRequest(BaseModel):
    username: str = Field(..., description="Username to update password for")
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., description="New password")
    oracle_config: OracleConnectionConfig

class UserSearchRequest(BaseModel):
    search_criteria: Dict[str, Any] = Field(..., description="Search criteria")
    oracle_config: OracleConnectionConfig

class AORSearchRequest(BaseModel):
    search_criteria: Dict[str, Any] = Field(..., description="Search criteria for AOR")
    oracle_config: OracleConnectionConfig

class OperationStatus(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class BulkOperationResponse(BaseModel):
    total_operations: int
    successful_operations: int
    failed_operations: int
    results: List[OperationStatus]

# Configuration schemas
class AppConfig(BaseModel):
    app_name: str = "Oracle Fusion HCM User Management"
    version: str = "1.0.0"
    theme: Dict[str, str] = {
        "primary_color": "#1976d2",
        "secondary_color": "#dc004e",
        "background_color": "#f5f5f5",
        "text_color": "#333333"
    }
    logo_url: Optional[str] = None
    company_name: Optional[str] = None

class ClientBranding(BaseModel):
    primary_color: str = "#1976d2"
    secondary_color: str = "#dc004e"
    accent_color: str = "#ff9800"
    background_color: str = "#f5f5f5"
    text_color: str = "#333333"
    logo_url: Optional[str] = None
    company_name: Optional[str] = None
    favicon_url: Optional[str] = None 