# Enhanced Oracle Fusion HCM API Client
# This module handles Oracle API calls for User Accounts and Areas of Responsibility

import requests
from requests.auth import HTTPBasicAuth
import logging
import json
from typing import Dict, List, Optional, Any
from urllib.parse import quote

logger = logging.getLogger("oracle_client")

class OracleClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.api_version = "11.13.18.05"  # Oracle Fusion HCM API version

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Generic method to make API requests to Oracle Fusion"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=60
            )
            
            logger.info(f"Oracle API {method} {url} - Status: {response.status_code}")
            
            if response.status_code in (200, 201, 204):
                return {
                    "success": True,
                    "data": response.json() if response.content else None,
                    "status_code": response.status_code
                }
            else:
                logger.error(f"Oracle API error: {response.status_code} {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.exception(f"Exception during Oracle API {method} call to {endpoint}")
            return {"success": False, "error": str(e)}

    # User Accounts API Methods
    def get_user_account(self, guid: str) -> Dict:
        """Get a specific user account by GUID"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/userAccounts/{guid}"
        return self._make_request("GET", endpoint)

    def get_all_user_accounts(self, params: Optional[Dict] = None) -> Dict:
        """Get all user accounts with optional filtering"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/userAccounts"
        return self._make_request("GET", endpoint, params=params)

    def create_user_account(self, user_data: Dict) -> Dict:
        """Create a new user account"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/userAccounts"
        return self._make_request("POST", endpoint, data=user_data)

    def update_user_account(self, guid: str, user_data: Dict) -> Dict:
        """Update an existing user account"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/userAccounts/{guid}"
        return self._make_request("PATCH", endpoint, data=user_data)

    def delete_user_account(self, guid: str) -> Dict:
        """Delete a user account"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/userAccounts/{guid}"
        return self._make_request("DELETE", endpoint)

    def reset_user_password(self, guid: str, password_data: Dict) -> Dict:
        """Reset a user account password"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/userAccounts/{guid}/action/resetPassword"
        return self._make_request("POST", endpoint, data=password_data)

    def update_user_password(self, guid: str, password_data: Dict) -> Dict:
        """Update a user account password"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/userAccounts/{guid}/action/updatePassword"
        return self._make_request("POST", endpoint, data=password_data)

    def autoprovision_roles(self, guid: str) -> Dict:
        """Trigger roles autoprovisioning process"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/userAccounts/{guid}/action/autoprovisionRoles"
        return self._make_request("POST", endpoint)

    # Areas of Responsibility API Methods
    def get_areas_of_responsibility(self, params: Optional[Dict] = None) -> Dict:
        """Get all areas of responsibility"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/areasOfResponsibility"
        return self._make_request("GET", endpoint, params=params)

    def get_area_of_responsibility(self, aor_id: str) -> Dict:
        """Get a specific area of responsibility"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/areasOfResponsibility/{aor_id}"
        return self._make_request("GET", endpoint)

    def create_area_of_responsibility(self, aor_data: Dict) -> Dict:
        """Create a new area of responsibility"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/areasOfResponsibility"
        return self._make_request("POST", endpoint, data=aor_data)

    def update_area_of_responsibility(self, aor_id: str, aor_data: Dict) -> Dict:
        """Update an area of responsibility"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/areasOfResponsibility/{aor_id}"
        return self._make_request("PATCH", endpoint, data=aor_data)

    def delete_area_of_responsibility(self, aor_id: str) -> Dict:
        """Delete an area of responsibility"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/areasOfResponsibility/{aor_id}"
        return self._make_request("DELETE", endpoint)

    def reassign_responsibility(self, aor_id: str, reassign_data: Dict) -> Dict:
        """Reassign a responsibility"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/areasOfResponsibility/{aor_id}/action/reassign"
        return self._make_request("POST", endpoint, data=reassign_data)

    def find_areas_of_responsibility(self, search_criteria: Dict) -> Dict:
        """Find areas of responsibility using advanced search"""
        endpoint = f"/hcmRestApi/resources/{self.api_version}/areasOfResponsibility/action/findByAdvancedSearch"
        return self._make_request("POST", endpoint, data=search_criteria)

    # Enhanced User Management Methods
    def get_user_details(self, username: str) -> Dict:
        """Get comprehensive user details including roles and data security"""
        # First get user account
        user_result = self.get_user_by_username(username)
        if not user_result.get("success"):
            return user_result
        
        user_data = user_result.get("data", {})
        user_guid = user_data.get("GUID")
        
        if not user_guid:
            return {"success": False, "error": "User GUID not found"}
        
        # Get user account details
        account_result = self.get_user_account(user_guid)
        if not account_result.get("success"):
            return account_result
        
        # Get areas of responsibility for this user
        aor_params = {"q": f"userAccountId eq {user_guid}"}
        aor_result = self.get_areas_of_responsibility(aor_params)
        
        # Combine all data
        combined_data = {
            "userAccount": account_result.get("data"),
            "areasOfResponsibility": aor_result.get("data") if aor_result.get("success") else [],
            "scimUser": user_data
        }
        
        return {"success": True, "data": combined_data}

    def get_user_by_username(self, username: str) -> Dict:
        """Get user by username using SCIM API"""
        filter_query = f'userName eq "{username}"'
        url = f"{self.base_url}/hcmRestApi/scim/Users?filter={quote(filter_query)}"
        headers = {"Accept": "application/json"}
        
        try:
            response = requests.get(
                url,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                users = data.get("Resources", [])
                if users:
                    return {"success": True, "data": users[0]}
                else:
                    return {"success": False, "error": "User not found"}
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_role_to_user(self, username: str, role_name: str) -> Dict:
        """Assign a role to a user"""
        # First get user details
        user_result = self.get_user_by_username(username)
        if not user_result.get("success"):
            return user_result
        
        user_data = user_result.get("data")
        current_roles = user_data.get("roles", [])
        
        # Check if role already exists
        for role in current_roles:
            if role.get("value") == role_name:
                return {"success": False, "error": "Role already assigned to user"}
        
        # Add new role
        new_role = {
            "value": role_name,
            "displayName": role_name,
            "description": f"Role assigned via API: {role_name}"
        }
        current_roles.append(new_role)
        
        # Update user
        update_data = {"roles": current_roles}
        return self.update_user_scim(user_data.get("id"), update_data)

    def remove_role_from_user(self, username: str, role_name: str) -> Dict:
        """Remove a role from a user"""
        # First get user details
        user_result = self.get_user_by_username(username)
        if not user_result.get("success"):
            return user_result
        
        user_data = user_result.get("data")
        current_roles = user_data.get("roles", [])
        
        # Remove role
        updated_roles = [role for role in current_roles if role.get("value") != role_name]
        
        if len(updated_roles) == len(current_roles):
            return {"success": False, "error": "Role not found for user"}
        
        # Update user
        update_data = {"roles": updated_roles}
        return self.update_user_scim(user_data.get("id"), update_data)

    def update_user_scim(self, user_id: str, update_data: Dict) -> Dict:
        """Update user via SCIM API"""
        url = f"{self.base_url}/hcmRestApi/scim/Users/{user_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = requests.patch(
                url,
                json=update_data,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=30
            )
            
            if response.status_code in (200, 204):
                return {"success": True, "data": response.json() if response.content else None}
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Legacy methods for backward compatibility
    def create_user(self, user_data):
        return self.create_user_account(user_data)

    def get_user(self, username):
        return self.get_user_by_username(username)

    def get_all_users(self):
        url = f"{self.base_url}/hcmRestApi/scim/Users"
        headers = {"Accept": "application/json"}
        all_users = []
        start_index = 1
        count = 500
        
        try:
            while True:
                params = {"startIndex": start_index, "count": count}
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    auth=HTTPBasicAuth(self.username, self.password),
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    users = data.get("Resources", [])
                    all_users.extend(users)
                    
                    if len(users) < count:
                        break
                    start_index += count
                else:
                    return {
                        "success": False,
                        "error": response.text,
                        "status_code": response.status_code
                    }
            
            return {"success": True, "data": {"Resources": all_users}}
        except Exception as e:
            return {"success": False, "error": str(e)} 