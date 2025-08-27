# API Documentation

## Overview
This document describes the API endpoints for the Oracle Fusion HCM User Management Tool.

## Base URL
- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication
All API calls require Oracle Fusion HCM credentials passed in the request body or query parameters.

## Endpoints

### User Management
- `GET /users/` - Get all users
- `POST /users/details` - Get comprehensive user details
- `POST /users/roles/assign` - Assign role to user
- `POST /users/roles/remove` - Remove role from user
- `POST /users/roles/bulk-assign` - Bulk role assignment

### Data Security
- `POST /users/data-security/assign` - Assign data security context
- `POST /users/data-security/bulk-assign` - Bulk data security assignment

### Areas of Responsibility
- `GET /areas-of-responsibility/` - Get all AORs
- `POST /areas-of-responsibility/assign` - Assign AOR to user
- `POST /areas-of-responsibility/remove` - Remove AOR from user
- `POST /areas-of-responsibility/bulk-assign` - Bulk AOR assignment

### Password Management
- `POST /users/password/reset` - Reset user password
- `POST /users/password/update` - Update user password

### File Operations
- `POST /upload/excel` - Upload Excel file for bulk operations
- `GET /users/download` - Download users as Excel file

### Search
- `POST /users/search` - Search users with criteria
- `POST /areas-of-responsibility/search` - Search AORs

## Error Handling
All endpoints return appropriate HTTP status codes and error messages in JSON format.

## Rate Limiting
API calls are subject to rate limiting based on Oracle Fusion HCM API limits.
