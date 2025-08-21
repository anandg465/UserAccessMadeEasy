# Placeholder for Oracle API integration
# This module will handle Oracle API calls and mapping logic

import requests
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger("oracle_client")

class OracleClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password

    def create_user(self, user_data):
        url = f"{self.base_url}/hcmRestApi/scim/Users"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            response = requests.post(
                url,
                json=user_data,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=30
            )
            if response.status_code in (200, 201):
                return {"success": True, "data": response.json()}
            else:
                logger.error(f"Oracle API error: {response.status_code} {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code,
                    "request": user_data,
                    "response": response.text
                }
        except Exception as e:
            logger.exception("Exception during Oracle API call")
            return {"success": False, "error": str(e), "request": user_data}

    def get_user(self, username):
        # Use double quotes for username in filter as required by Oracle
        filter_query = f'userName eq "{username}"'
        url = f"{self.base_url}/hcmRestApi/scim/Users?filter={filter_query}"
        headers = {
            "Accept": "application/json"
        }
        try:
            response = requests.get(
                url,
                headers=headers,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=30
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                logger.error(f"Oracle API get_user error: {response.status_code} {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code,
                    "request": username,
                    "response": response.text
                }
        except Exception as e:
            logger.exception("Exception during Oracle API get_user call")
            return {"success": False, "error": str(e), "request": username}

    def get_all_users(self):
        url = f"{self.base_url}/hcmRestApi/scim/Users"
        headers = {
            "Accept": "application/json"
        }
        all_users = []
        start_index = 1
        count = 500
        total_results = None
        try:
            while True:
                params = {"startIndex": start_index, "count": count}
                logger.info(f"Fetching users: url={url}, params={params}")
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    auth=HTTPBasicAuth(self.username, self.password),
                    timeout=60
                )
                logger.info(f"Response status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    users = data.get("Resources", [])
                    logger.info(f"Fetched {len(users)} users, total so far: {len(all_users) + len(users)}, totalResults: {data.get('totalResults')}, startIndex: {start_index}")
                    all_users.extend(users)
                    # Persist totalResults from the first page
                    if total_results is None:
                        total_results = data.get("totalResults", len(all_users))
                    # Stop if less than 'count' users returned (last page)
                    if len(users) < count or len(all_users) >= total_results:
                        break
                    start_index += len(users)
                else:
                    logger.error(f"Oracle API get_all_users error: {response.status_code} {response.text}")
                    return {
                        "success": False,
                        "error": response.text,
                        "status_code": response.status_code,
                        "response": response.text
                    }
            logger.info(f"Final user count: {len(all_users)}")
            return {"success": True, "data": {"Resources": all_users, "totalResults": total_results}}
        except Exception as e:
            logger.exception("Exception during Oracle API get_all_users call")
            return {"success": False, "error": str(e)}

    def bulk_create_users(self, users_data):
        # TODO: Implement Oracle API call for bulk user creation
        pass 