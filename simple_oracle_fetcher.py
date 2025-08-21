#!/usr/bin/env python3
"""
Simple Oracle Fusion Resource Fetcher
Alternative approach using Python's built-in HTTP server
"""

import http.server
import socketserver
import json
import requests
import base64
import os
import socket
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class OracleFusionHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            html_content = self.get_html_content()
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/download_error_log':
            log_file = 'update_errors.log'
            if os.path.exists(log_file):
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Disposition', 'attachment; filename="update_errors.log"')
                self.end_headers()
                with open(log_file, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Log file not found.')
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/fetch_resources':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                result = self.fetch_oracle_resources(data)
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                error_result = {'error': str(e)}
                self.wfile.write(json.dumps(error_result).encode('utf-8'))
        elif self.path == '/update_person_info':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                result = self.update_person_information(data)
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                error_result = {'error': str(e)}
                self.wfile.write(json.dumps(error_result).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def fetch_oracle_resources(self, data):
        """Fetch resources from Oracle Fusion API"""
        base_url = data.get('base_url', '').rstrip('/')
        username = data.get('username')
        password = data.get('password')
        
        if not all([base_url, username, password]):
            return {'error': 'Missing required parameters'}
        
        # Construct the Oracle Fusion API URL
        api_url = f"{base_url}/fscmRestApi/resources/11.13.18.05/projectEnterpriseLaborResources"
        
        # Prepare authentication
        auth = (username, password)
        
        # Fetch all resources with pagination
        all_resources = []
        offset = 0
        limit = 25
        
        while True:
            try:
                # Make request to Oracle Fusion
                params = {
                    'limit': limit,
                    'offset': offset
                }
                
                print(f"Fetching page: offset={offset}, limit={limit}")
                
                response = requests.get(
                    api_url,
                    params=params,
                    auth=auth,
                    headers={
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    timeout=30
                )
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 401:
                    return {'error': 'Authentication failed. Please check your username and password.'}
                elif response.status_code == 403:
                    return {'error': 'Access denied. You may not have permission to access this resource.'}
                elif response.status_code == 404:
                    return {'error': 'API endpoint not found. Please check your base URL.'}
                elif response.status_code != 200:
                    return {'error': f'HTTP {response.status_code}: {response.text}'}
                
                # Parse response
                data = response.json()
                
                if 'items' in data and data['items']:
                    all_resources.extend(data['items'])
                    print(f"Fetched {len(data['items'])} resources (total: {len(all_resources)})")
                    
                    # Check if we've reached the end
                    if len(data['items']) < limit:
                        break
                    
                    offset += limit
                else:
                    print("No more items found")
                    break
                
            except requests.exceptions.Timeout:
                return {'error': 'Request timeout. The Oracle Fusion server took too long to respond.'}
            except requests.exceptions.ConnectionError:
                return {'error': 'Connection error. Please check your base URL and internet connection.'}
            except Exception as e:
                print(f"Error fetching data: {str(e)}")
                return {'error': f'Error fetching data: {str(e)}'}
        
        print(f"Total resources fetched: {len(all_resources)}")
        return {
            'success': True,
            'resources': all_resources,
            'count': len(all_resources),
            'timestamp': datetime.now().isoformat()
        }
    
    def update_person_information(self, data):
        """Update person information from HCM for selected resources, logging failures."""
        import threading
        try:
            print("[DEBUG] update_person_information called")
            base_url = data.get('base_url', '').rstrip('/')
            username = data.get('username')
            password = data.get('password')
            resource_ids = data.get('resource_ids', [])
            
            if not all([base_url, username, password]):
                print("[DEBUG] Missing required parameters")
                return {'error': 'Missing required parameters'}
            
            if not resource_ids:
                print("[DEBUG] No resource IDs provided for update")
                return {'error': 'No resource IDs provided for update'}
            
            # Construct the Oracle Fusion API URL for person information update
            api_url = f"{base_url}/fscmRestApi/resources/11.13.18.05/projectEnterpriseLaborResources/action/updatePersonInformationFromHCM"
            
            # Prepare authentication
            auth = (username, password)
            
            log_file = 'update_errors.log'
            log_lock = threading.Lock()
            success_ids = []
            failed = []
            for rid in resource_ids:
                request_body = {"resourceIds": [rid]}
                try:
                    print(f"[DEBUG] Sending POST for ResourceId: {rid}")
                    response = requests.post(
                        api_url,
                        json=request_body,
                        auth=auth,
                        headers={
                            'Accept': 'application/json',
                            'Content-Type': 'application/vnd.oracle.adf.action+json'
                        },
                        timeout=10
                    )
                    print(f"[DEBUG] Response for ResourceId {rid}: status {response.status_code}")
                    if response.status_code == 200:
                        result_data = response.json()
                        # Check for result string in response
                        if 'result' in result_data and 'success' in result_data['result'].lower():
                            success_ids.append(rid)
                        else:
                            failed.append((rid, result_data.get('result', 'Unknown error')))
                    else:
                        failed.append((rid, f"HTTP {response.status_code}: {response.text}"))
                except Exception as e:
                    print(f"[DEBUG] Exception for ResourceId {rid}: {str(e)}")
                    failed.append((rid, str(e)))
            # Write failures to log only if there are failures
            if failed:
                with log_lock:
                    with open(log_file, 'w') as f:
                        f.write(f"Update errors log - {datetime.now().isoformat()}\n\n")
                        for rid, err in failed:
                            f.write(f"ResourceId: {rid} | Error: {err}\n")
            elif os.path.exists(log_file):
                # Remove old log if no failures this time
                os.remove(log_file)
            print(f"[DEBUG] update_person_information finished: {len(success_ids)} success, {len(failed)} failed")
            return {
                'success': True,
                'updated_count': len(success_ids),
                'failed_count': len(failed),
                'failed_log': log_file if failed else None,
                'updated_ids': success_ids,
                'failed_ids': [rid for rid, _ in failed],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"[ERROR] update_person_information exception: {str(e)}")
            return {'error': f'Unexpected server error: {str(e)}'}
    
    def get_html_content(self):
        """Return the HTML content for the web interface"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oracle Fusion Resource Fetcher (Simple Server)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .form-section {
            padding: 40px;
            border-bottom: 1px solid #eee;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
            font-size: 1.1em;
        }

        .form-group input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .password-container {
            position: relative;
        }

        .password-toggle {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.2em;
            color: #666;
            transition: color 0.3s ease;
        }

        .password-toggle:hover {
            color: #667eea;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            width: 100%;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .results-section {
            padding: 40px;
            display: none;
        }

        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
        }

        .results-count {
            font-size: 1.2em;
            color: #2c3e50;
            font-weight: 600;
        }

        .export-btn {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s ease;
        }

        .export-btn:hover {
            transform: translateY(-1px);
        }

        .table-container {
            overflow-x: auto;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .filters-section {
            margin-bottom: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }

        .filters-row {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .filter-group {
            flex: 1;
            min-width: 200px;
        }

        .filter-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #2c3e50;
            font-size: 0.9em;
        }

        .filter-group input, .filter-group select {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.9em;
        }

        .filter-group input:focus, .filter-group select:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
        }

        .filter-actions {
            display: flex;
            gap: 10px;
            align-items: end;
        }

        .filter-btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 600;
        }

        .filter-btn:hover {
            background: #2980b9;
        }

        .clear-btn {
            background: #95a5a6;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
        }

        .clear-btn:hover {
            background: #7f8c8d;
        }

        .results-summary {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding: 10px 15px;
            background: #ecf0f1;
            border-radius: 6px;
            font-size: 0.9em;
        }

        .sortable-header {
            cursor: pointer;
            user-select: none;
            position: relative;
            padding-right: 20px;
        }

        .sortable-header:hover {
            background: #e8f4fd;
        }

        .sort-icon {
            position: absolute;
            right: 5px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.8em;
            color: #7f8c8d;
        }

        .sort-icon.active {
            color: #3498db;
        }

        .resource-details {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #27ae60;
        }

        .details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }

        .detail-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #e1e8ed;
        }

        .detail-label {
            font-weight: 600;
            color: #2c3e50;
            font-size: 0.9em;
            margin-bottom: 5px;
        }

        .detail-value {
            color: #34495e;
            font-size: 1em;
        }

        .detail-value.null {
            color: #95a5a6;
            font-style: italic;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #c33;
        }

        .success {
            background: #efe;
            color: #363;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #363;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .server-info {
            background: #e8f4fd;
            color: #2c3e50;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #3498db;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Oracle Fusion Resource Fetcher</h1>
            <p>Simple HTTP Server - No CORS issues!</p>
        </div>

        <div class="form-section">
            <div class="server-info">
                <strong>✅ Simple HTTP Server Active:</strong> This tool uses Python's built-in HTTP server to bypass CORS restrictions.
            </div>

            <form id="fetchForm">
                <div class="form-group">
                    <label for="baseUrl">Base URL:</label>
                    <input type="url" id="baseUrl" required placeholder="https://your-instance.oraclecloud.com">
                    <small style="color: #666; margin-top: 5px; display: block;">
                        Example: https://your-instance.oraclecloud.com
                    </small>
                </div>

                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" required placeholder="Enter your Oracle Fusion username">
                </div>

                <div class="form-group">
                    <label for="password">Password:</label>
                    <div class="password-container">
                        <input type="password" id="password" required placeholder="Enter your password">
                        <button type="button" class="password-toggle" onclick="togglePassword()">👁️</button>
                    </div>
                </div>

                <button type="submit" class="btn" id="fetchBtn">
                    <span class="loading" style="display: none;"></span>
                    Fetch Resources
                </button>
            </form>
        </div>

        <div class="results-section" id="resultsSection">
            <div class="results-header">
                <div class="results-count" id="resultsCount"></div>
                <div style="display: flex; gap: 10px;">
                    <button class="export-btn" onclick="exportToCSV()">Export to CSV</button>
                    <button class="export-btn" style="background: linear-gradient(135deg, #e67e22 0%, #f39c12 100%);" onclick="showUpdateSection()">Update Person Info</button>
                </div>
            </div>
            
            <div class="resource-details" id="resourceDetails" style="display: none;">
                <h3 style="margin-bottom: 15px; color: #2c3e50;">📊 Resource Summary</h3>
                <div class="details-grid" id="detailsGrid">
                    <!-- Resource details will be populated here -->
                </div>
            </div>
            
            <div class="filters-section" id="filtersSection" style="display: none;">
                <h3 style="margin-bottom: 15px; color: #2c3e50;">🔍 Filter Resources</h3>
                <div class="filters-row">
                    <div class="filter-group">
                        <label for="filterName">Resource Name</label>
                        <input type="text" id="filterName" placeholder="Filter by name..." onkeyup="applyFilters()">
                    </div>
                    <div class="filter-group">
                        <label for="filterEmail">Email</label>
                        <input type="text" id="filterEmail" placeholder="Filter by email..." onkeyup="applyFilters()">
                    </div>
                    <div class="filter-group">
                        <label for="filterRole">Project Role</label>
                        <input type="text" id="filterRole" placeholder="Filter by role..." onkeyup="applyFilters()">
                    </div>
                    <div class="filter-group">
                        <label for="filterPool">Resource Pool</label>
                        <input type="text" id="filterPool" placeholder="Filter by pool..." onkeyup="applyFilters()">
                    </div>
                </div>
                <div class="filters-row">
                    <div class="filter-group">
                        <label for="filterManager">Manager</label>
                        <input type="text" id="filterManager" placeholder="Filter by manager..." onkeyup="applyFilters()">
                    </div>
                    <div class="filter-group">
                        <label for="filterPersonNumber">Person Number</label>
                        <input type="text" id="filterPersonNumber" placeholder="Filter by person number..." onkeyup="applyFilters()">
                    </div>
                    <div class="filter-group">
                        <label for="filterStatus">Staffing Status</label>
                        <select id="filterStatus" onchange="applyFilters()">
                            <option value="">All Status</option>
                            <option value="true">Manage Staffing</option>
                            <option value="false">No Staffing</option>
                        </select>
                    </div>
                    <div class="filter-actions">
                        <button class="filter-btn" onclick="applyFilters()">Apply Filters</button>
                        <button class="clear-btn" onclick="clearFilters()">Clear All</button>
                    </div>
                </div>
            </div>
            
            <div class="results-summary" id="resultsSummary" style="display: none;">
                <div>
                    <span id="filteredCount">0</span> of <span id="totalCount">0</span> resources shown
                </div>
                <div>
                    <button onclick="toggleFilters()" style="background: #3498db; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 0.8em;">Toggle Filters</button>
                </div>
            </div>
            
            <div class="update-section" id="updateSection" style="display: none; margin-bottom: 20px; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #e67e22;">
                <h3 style="margin-bottom: 15px; color: #2c3e50;">🔄 Update Person Information from HCM</h3>
                <p style="margin-bottom: 15px; color: #666;">Select resources to update their person information (Name, Image, Phone Number, Email, From Date, To Date, Manager) from HCM.</p>
                
                <div style="margin-bottom: 15px;">
                    <button onclick="selectAllResources()" style="background: #3498db; color: white; border: none; padding: 8px 15px; border-radius: 4px; margin-right: 10px; cursor: pointer;">Select All</button>
                    <button onclick="deselectAllResources()" style="background: #95a5a6; color: white; border: none; padding: 8px 15px; border-radius: 4px; margin-right: 10px; cursor: pointer;">Deselect All</button>
                    <span id="selectedCount" style="color: #2c3e50; font-weight: 600;">0 resources selected</span>
                </div>
                
                <div style="max-height: 300px; overflow-y: auto; border: 1px solid #ddd; border-radius: 4px; padding: 10px; background: white;">
                    <div id="resourceSelectionList">
                        <!-- Resource selection checkboxes will be populated here -->
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
                    <button onclick="updatePersonInformation()" id="updateBtn" style="background: linear-gradient(135deg, #e67e22 0%, #f39c12 100%); color: white; border: none; padding: 12px 25px; border-radius: 6px; cursor: pointer; font-weight: 600; display: none;">Update Selected Resources</button>
                    <button onclick="hideUpdateSection()" style="background: #95a5a6; color: white; border: none; padding: 12px 25px; border-radius: 6px; margin-left: 10px; cursor: pointer;">Cancel</button>
                </div>
            </div>
            
            <div class="table-container">
                <table id="resultsTable">
                    <thead id="tableHead">
                        <!-- Headers will be populated dynamically -->
                    </thead>
                    <tbody id="tableBody">
                        <!-- Data will be populated dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let allResources = [];
        let filteredResources = [];
        let currentSort = { column: null, direction: 'asc' };

        // Toggle password visibility
        function togglePassword() {
            const passwordInput = document.getElementById('password');
            const toggleBtn = document.querySelector('.password-toggle');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggleBtn.textContent = '🙈';
            } else {
                passwordInput.type = 'password';
                toggleBtn.textContent = '👁️';
            }
        }

        // Show results
        function showResults() {
            const resultsSection = document.getElementById('resultsSection');
            const resultsCount = document.getElementById('resultsCount');
            const resourceDetails = document.getElementById('resourceDetails');
            const filtersSection = document.getElementById('filtersSection');
            const resultsSummary = document.getElementById('resultsSummary');
            
            if (resultsSection) {
                resultsSection.style.display = 'block';
            }
            if (resultsCount) {
                resultsCount.textContent = `Total Resources: ${allResources.length}`;
            }
            
            // Show additional sections
            if (resourceDetails) resourceDetails.style.display = 'block';
            if (filtersSection) filtersSection.style.display = 'block';
            if (resultsSummary) resultsSummary.style.display = 'block';
            
            // Initialize filtered resources
            filteredResources = [...allResources];
            
            // Populate resource details and table
            populateResourceDetails();
            createTableHeaders();
            populateTableData();
            updateResultsSummary();
        }

        // Populate resource details summary
        function populateResourceDetails() {
            const detailsGrid = document.getElementById('detailsGrid');
            if (!detailsGrid || allResources.length === 0) return;

            const details = calculateResourceDetails();
            
            detailsGrid.innerHTML = `
                <div class="detail-item">
                    <div class="detail-label">Total Resources</div>
                    <div class="detail-value">${allResources.length}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Unique Roles</div>
                    <div class="detail-value">${details.uniqueRoles}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Resource Pools</div>
                    <div class="detail-value">${details.uniquePools}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">With Email</div>
                    <div class="detail-value">${details.withEmail}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">With Manager</div>
                    <div class="detail-value">${details.withManager}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Manage Staffing</div>
                    <div class="detail-value">${details.manageStaffing}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Average Bill Rate</div>
                    <div class="detail-value">${details.avgBillRate}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Average Cost Rate</div>
                    <div class="detail-value">${details.avgCostRate}</div>
                </div>
            `;
        }

        // Calculate resource details
        function calculateResourceDetails() {
            const roles = new Set();
            const pools = new Set();
            let withEmail = 0;
            let withManager = 0;
            let manageStaffing = 0;
            let totalBillRate = 0;
            let totalCostRate = 0;
            let billRateCount = 0;
            let costRateCount = 0;

            allResources.forEach(resource => {
                if (resource.PrimaryProjectRoleName) roles.add(resource.PrimaryProjectRoleName);
                if (resource.ResourcePoolName) pools.add(resource.ResourcePoolName);
                if (resource.Email) withEmail++;
                if (resource.ManagerName) withManager++;
                if (resource.ManageResourceStaffingFlag === true) manageStaffing++;
                if (resource.BillRate) {
                    totalBillRate += parseFloat(resource.BillRate);
                    billRateCount++;
                }
                if (resource.CostRate) {
                    totalCostRate += parseFloat(resource.CostRate);
                    costRateCount++;
                }
            });

            return {
                uniqueRoles: roles.size,
                uniquePools: pools.size,
                withEmail,
                withManager,
                manageStaffing,
                avgBillRate: billRateCount > 0 ? (totalBillRate / billRateCount).toFixed(2) : 'N/A',
                avgCostRate: costRateCount > 0 ? (totalCostRate / costRateCount).toFixed(2) : 'N/A'
            };
        }

        // Toggle filters visibility
        function toggleFilters() {
            const filtersSection = document.getElementById('filtersSection');
            if (filtersSection) {
                filtersSection.style.display = filtersSection.style.display === 'none' ? 'block' : 'none';
            }
        }

        // Apply filters (updated for specific fields)
        function applyFilters() {
            const nameFilter = document.getElementById('filterName').value.toLowerCase();
            const emailFilter = document.getElementById('filterEmail').value.toLowerCase();
            const roleFilter = document.getElementById('filterRole').value.toLowerCase();
            const poolFilter = document.getElementById('filterPool').value.toLowerCase();
            const managerFilter = document.getElementById('filterManager').value.toLowerCase();
            const personNumberFilter = document.getElementById('filterPersonNumber').value.toLowerCase();
            const statusFilter = document.getElementById('filterStatus').value;

            filteredResources = allResources.filter(resource => {
                const name = (resource.ResourceName || '').toLowerCase();
                const email = (resource.Email || '').toLowerCase();
                const role = (resource.PrimaryProjectRoleName || '').toLowerCase();
                const pool = (resource.ResourcePoolName || '').toLowerCase();
                const manager = (resource.ManagerName || '').toLowerCase();
                const personNumber = (resource.PersonNumber || '').toLowerCase();
                const staffing = resource.ManageResourceStaffingFlag;

                return (!nameFilter || name.includes(nameFilter)) &&
                       (!emailFilter || email.includes(emailFilter)) &&
                       (!roleFilter || role.includes(roleFilter)) &&
                       (!poolFilter || pool.includes(poolFilter)) &&
                       (!managerFilter || manager.includes(managerFilter)) &&
                       (!personNumberFilter || personNumber.includes(personNumberFilter)) &&
                       (!statusFilter || staffing.toString() === statusFilter);
            });

            populateTableData();
            updateResultsSummary();
        }

        // Clear all filters
        function clearFilters() {
            document.getElementById('filterName').value = '';
            document.getElementById('filterEmail').value = '';
            document.getElementById('filterRole').value = '';
            document.getElementById('filterPool').value = '';
            document.getElementById('filterManager').value = '';
            document.getElementById('filterPersonNumber').value = '';
            document.getElementById('filterStatus').value = '';
            
            filteredResources = [...allResources];
            populateTableData();
            updateResultsSummary();
        }

        // Update results summary
        function updateResultsSummary() {
            const filteredCount = document.getElementById('filteredCount');
            const totalCount = document.getElementById('totalCount');
            
            if (filteredCount) filteredCount.textContent = filteredResources.length;
            if (totalCount) totalCount.textContent = allResources.length;
        }

        // Create table headers with sorting (updated for specific fields)
        function createTableHeaders() {
            const thead = document.getElementById('tableHead');
            if (!thead) {
                console.error('Table head element not found');
                return;
            }
            
            thead.innerHTML = '';
            
            // Define the specific fields to display in the table
            const displayFields = [
                'ResourceName',
                'ResourceId', 
                'FirstName',
                'LastName',
                'Email',
                'PersonNumber'
            ];
            
            const tr = document.createElement('tr');
            displayFields.forEach(key => {
                const th = document.createElement('th');
                th.className = 'sortable-header';
                th.onclick = () => sortTable(key);
                
                const label = document.createElement('span');
                // Create user-friendly labels
                const fieldLabels = {
                    'ResourceName': 'Resource Name',
                    'ResourceId': 'Resource ID',
                    'FirstName': 'First Name',
                    'LastName': 'Last Name',
                    'Email': 'Email',
                    'PersonNumber': 'HCM Person Number'
                };
                label.textContent = fieldLabels[key] || key;
                th.appendChild(label);
                
                const sortIcon = document.createElement('span');
                sortIcon.className = 'sort-icon';
                sortIcon.textContent = '↕';
                th.appendChild(sortIcon);
                
                tr.appendChild(th);
            });
            thead.appendChild(tr);
        }

        // Sort table
        function sortTable(column) {
            const direction = currentSort.column === column && currentSort.direction === 'asc' ? 'desc' : 'asc';
            currentSort = { column, direction };

            filteredResources.sort((a, b) => {
                let aVal = a[column];
                let bVal = b[column];

                // Handle null/undefined values
                if (aVal === null || aVal === undefined) aVal = '';
                if (bVal === null || bVal === undefined) bVal = '';

                // Convert to string for comparison
                aVal = String(aVal).toLowerCase();
                bVal = String(bVal).toLowerCase();

                if (direction === 'asc') {
                    return aVal.localeCompare(bVal);
                } else {
                    return bVal.localeCompare(aVal);
                }
            });

            // Update sort icons
            updateSortIcons(column, direction);
            
            populateTableData();
        }

        // Update sort icons
        function updateSortIcons(activeColumn, direction) {
            const headers = document.querySelectorAll('.sortable-header');
            headers.forEach(header => {
                const icon = header.querySelector('.sort-icon');
                const column = header.querySelector('span').textContent;
                
                if (column === activeColumn) {
                    icon.textContent = direction === 'asc' ? '↑' : '↓';
                    icon.className = 'sort-icon active';
                } else {
                    icon.textContent = '↕';
                    icon.className = 'sort-icon';
                }
            });
        }

        // Populate table data (updated for specific fields)
        function populateTableData() {
            const tbody = document.getElementById('tableBody');
            if (!tbody) {
                console.error('Table body element not found');
                return;
            }
            
            tbody.innerHTML = '';

            // Define the specific fields to display in the table
            const displayFields = [
                'ResourceName',
                'ResourceId', 
                'FirstName',
                'LastName',
                'Email',
                'PersonNumber'
            ];

            filteredResources.forEach(resource => {
                const tr = document.createElement('tr');
                displayFields.forEach(key => {
                    const td = document.createElement('td');
                    const value = resource[key];
                    
                    if (value !== null && value !== undefined) {
                        td.textContent = value;
                        td.className = 'detail-value';
                    } else {
                        td.textContent = '';
                        td.className = 'detail-value null';
                    }
                    
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
        }

        // Fetch resources using server
        async function fetchAllResources(baseUrl, username, password) {
            const requestData = {
                base_url: baseUrl,
                username: username,
                password: password
            };

            console.log('Sending request to server...');
            
            const response = await fetch('/fetch_resources', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            return data.resources || [];
        }

        // Handle form submission
        document.getElementById('fetchForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const baseUrl = document.getElementById('baseUrl').value.trim();
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            const fetchBtn = document.getElementById('fetchBtn');
            const loadingSpinner = fetchBtn?.querySelector('.loading');
            
            try {
                // Show loading state
                if (fetchBtn) {
                    fetchBtn.disabled = true;
                }
                if (loadingSpinner) {
                    loadingSpinner.style.display = 'inline-block';
                }
                if (fetchBtn) {
                    fetchBtn.textContent = 'Fetching Resources...';
                }

                // Fetch all resources through server
                allResources = await fetchAllResources(baseUrl, username, password);
                
                // Create and populate table
                createTableHeaders();
                populateTableData();
                
                showResults();

            } catch (error) {
                console.error('Error:', error);
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error';
                errorDiv.textContent = `Error: ${error.message}`;
                
                const formSection = document.querySelector('.form-section');
                if (formSection) {
                    formSection.insertBefore(errorDiv, formSection.firstChild);
                    
                    // Remove error message after 10 seconds
                    setTimeout(() => {
                        if (errorDiv.parentNode) {
                            errorDiv.parentNode.removeChild(errorDiv);
                        }
                    }, 10000);
                }
                
            } finally {
                // Reset button state
                if (fetchBtn) {
                    fetchBtn.disabled = false;
                }
                if (loadingSpinner) {
                    loadingSpinner.style.display = 'none';
                }
                if (fetchBtn) {
                    fetchBtn.textContent = 'Fetch Resources';
                }
            }
        });

        // Export to CSV
        function exportToCSV() {
            if (filteredResources.length === 0) {
                alert('No data to export.');
                return;
            }

            // Get all unique keys
            const allKeys = new Set();
            allResources.forEach(resource => {
                Object.keys(resource).forEach(key => allKeys.add(key));
            });
            const sortedKeys = Array.from(allKeys).sort();

            // Create CSV content
            const csvContent = [
                sortedKeys.join(','),
                ...filteredResources.map(resource => 
                    sortedKeys.map(key => {
                        const value = resource[key];
                        // Escape commas and quotes in CSV
                        const escapedValue = value !== null && value !== undefined ? 
                            `"${String(value).replace(/"/g, '""')}"` : '';
                        return escapedValue;
                    }).join(',')
                )
            ].join('\\n');

            // Create and download file
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', `oracle_fusion_resources_${new Date().toISOString().split('T')[0]}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // --- Advanced Selection Filters for Update Person Info ---
        let updateFilterField = 'ResourceName';
        let updateFilterType = 'contains';
        let updateFilterValue = '';

        function renderUpdateFilters() {
            const updateSection = document.getElementById('updateSection');
            if (!updateSection) return;
            let filterHtml = `
                <div style="margin-bottom: 10px; display: flex; gap: 10px; align-items: flex-end; flex-wrap: wrap;">
                    <div>
                        <label style="font-size:0.9em; font-weight:600; color:#2c3e50;">Field</label><br>
                        <select id="updateFilterField" style="padding:6px 10px; border-radius:4px; border:1px solid #ddd;">
                            <option value="ResourceName">Resource Name</option>
                            <option value="Email">Email</option>
                            <option value="PersonNumber">Person Number</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:0.9em; font-weight:600; color:#2c3e50;">Type</label><br>
                        <select id="updateFilterType" style="padding:6px 10px; border-radius:4px; border:1px solid #ddd;">
                            <option value="contains">Contains</option>
                            <option value="begins">Begins with</option>
                            <option value="notbegins">Doesn't begin with</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:0.9em; font-weight:600; color:#2c3e50;">Value</label><br>
                        <input id="updateFilterValue" type="text" style="padding:6px 10px; border-radius:4px; border:1px solid #ddd; min-width:180px;" placeholder="Type to filter...">
                    </div>
                    <div>
                        <button onclick="applyUpdateSelectionFilter()" class="filter-btn" style="margin-bottom:2px;">Apply</button>
                        <button onclick="clearUpdateSelectionFilter()" class="clear-btn" style="margin-bottom:2px;">Clear</button>
                    </div>
                </div>
            `;
            let filterContainer = document.getElementById('updateFilterContainer');
            if (!filterContainer) {
                filterContainer = document.createElement('div');
                filterContainer.id = 'updateFilterContainer';
                updateSection.insertBefore(filterContainer, updateSection.querySelector('div[style*="max-height"]'));
            }
            filterContainer.innerHTML = filterHtml;
            // Set event listeners
            document.getElementById('updateFilterField').value = updateFilterField;
            document.getElementById('updateFilterType').value = updateFilterType;
            document.getElementById('updateFilterValue').value = updateFilterValue;
            document.getElementById('updateFilterField').onchange = function() {
                updateFilterField = this.value;
                applyUpdateSelectionFilter();
            };
            document.getElementById('updateFilterType').onchange = function() {
                updateFilterType = this.value;
                applyUpdateSelectionFilter();
            };
            document.getElementById('updateFilterValue').oninput = function() {
                updateFilterValue = this.value;
                applyUpdateSelectionFilter();
            };
        }

        function applyUpdateSelectionFilter() {
            // Filter the resource selection list based on the advanced filter
            let filtered = filteredResources.filter(resource => {
                const val = (resource[updateFilterField] || '').toLowerCase();
                const filterVal = (updateFilterValue || '').toLowerCase();
                if (!filterVal) return true;
                if (updateFilterType === 'contains') {
                    return val.includes(filterVal);
                } else if (updateFilterType === 'begins') {
                    return val.startsWith(filterVal);
                } else if (updateFilterType === 'notbegins') {
                    return !val.startsWith(filterVal);
                }
                return true;
            });
            populateResourceSelection(filtered);
        }

        function clearUpdateSelectionFilter() {
            updateFilterValue = '';
            document.getElementById('updateFilterValue').value = '';
            applyUpdateSelectionFilter();
        }

        // --- END Advanced Selection Filters ---

        // Show update section (render advanced filters)
        function showUpdateSection() {
            const updateSection = document.getElementById('updateSection');
            if (updateSection) {
                updateSection.style.display = 'block';
                renderUpdateFilters();
                populateResourceSelection();
            }
        }

        // Hide update section
        function hideUpdateSection() {
            const updateSection = document.getElementById('updateSection');
            if (updateSection) {
                updateSection.style.display = 'none';
            }
        }

        // Populate resource selection list (support advanced filter param)
        function populateResourceSelection(filteredList) {
            const selectionList = document.getElementById('resourceSelectionList');
            if (!selectionList) return;

            const list = filteredList || filteredResources;
            selectionList.innerHTML = '';

            list.forEach((resource, index) => {
                const div = document.createElement('div');
                div.style.cssText = 'display: flex; align-items: center; gap: 10px; padding: 8px; border-bottom: 1px solid #eee;';
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `resource_${index}`;
                checkbox.value = resource.ResourceId || resource.resourceId || resource.id;
                checkbox.onchange = updateSelectedCount;
                
                const label = document.createElement('label');
                label.htmlFor = `resource_${index}`;
                label.style.cssText = 'flex: 1; cursor: pointer; font-size: 0.9em;';
                
                // Create a readable label with the specific fields
                const resourceName = resource.ResourceName || 'Unknown';
                const resourceId = resource.ResourceId || 'N/A';
                const firstName = resource.FirstName || '';
                const lastName = resource.LastName || '';
                const email = resource.Email || 'No Email';
                const personNumber = resource.PersonNumber || 'N/A';
                
                const fullName = [firstName, lastName].filter(Boolean).join(' ') || 'No Name';
                
                label.textContent = `${resourceName} (${fullName}) - ${email} - ID: ${resourceId}`;
                
                div.appendChild(checkbox);
                div.appendChild(label);
                selectionList.appendChild(div);
            });

            updateSelectedCount();
        }

        // Update selected count
        function updateSelectedCount() {
            const checkboxes = document.querySelectorAll('#resourceSelectionList input[type="checkbox"]:checked');
            const selectedCount = document.getElementById('selectedCount');
            const updateBtn = document.getElementById('updateBtn');
            
            if (selectedCount) {
                selectedCount.textContent = `${checkboxes.length} resources selected`;
            }
            
            if (updateBtn) {
                updateBtn.style.display = checkboxes.length > 0 ? 'inline-block' : 'none';
            }
        }

        // Select all resources (updated for filtered data)
        function selectAllResources() {
            const checkboxes = document.querySelectorAll('#resourceSelectionList input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = true;
            });
            updateSelectedCount();
        }

        // Deselect all resources
        function deselectAllResources() {
            const checkboxes = document.querySelectorAll('#resourceSelectionList input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
            updateSelectedCount();
        }

        // Show success message (persistent until closed)
        function showPersistentSuccess(html) {
            // Remove any existing success messages
            document.querySelectorAll('.success').forEach(el => el.remove());
            const successDiv = document.createElement('div');
            successDiv.className = 'success';
            successDiv.innerHTML = html + '<br><button onclick="this.parentNode.remove();" style="margin-top:8px;background:#95a5a6;color:white;padding:8px 15px;border:none;border-radius:4px;cursor:pointer;">Close</button>';
            const formSection = document.querySelector('.form-section');
            if (formSection) {
                formSection.insertBefore(successDiv, formSection.firstChild);
            }
        }

        // Update person information (use persistent success message)
        async function updatePersonInformation() {
            const checkboxes = document.querySelectorAll('#resourceSelectionList input[type="checkbox"]:checked');
            
            if (checkboxes.length === 0) {
                alert('Please select at least one resource to update.');
                return;
            }

            const resourceIds = Array.from(checkboxes).map(cb => parseInt(cb.value));
            const baseUrl = document.getElementById('baseUrl').value.trim();
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            const updateBtn = document.getElementById('updateBtn');
            const originalText = updateBtn.textContent;
            
            try {
                // Show loading state
                updateBtn.disabled = true;
                updateBtn.textContent = 'Updating...';

                const requestData = {
                    base_url: baseUrl,
                    username: username,
                    password: password,
                    resource_ids: resourceIds
                };

                console.log('Sending update request for resources:', resourceIds);
                
                const response = await fetch('/update_person_info', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Server error: ${response.status} - ${errorText}`);
                }

                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }

                // Show persistent success message
                let html = `<strong>✅ Update Successful!</strong><br>
                    Updated ${data.updated_count} resources<br>
                    Failed to update ${data.failed_count} resources.`;
                if (data.failed_count > 0 && data.failed_log) {
                    html += `<br><button onclick="downloadErrorLog()" style="margin-top:8px;background:#c0392b;color:white;padding:8px 15px;border:none;border-radius:4px;cursor:pointer;">Download Error Log</button>`;
                }
                html += `<br>Timestamp: ${new Date(data.timestamp).toLocaleString()}`;
                showPersistentSuccess(html);

                // Hide update section
                hideUpdateSection();

            } catch (error) {
                console.error('Error:', error);
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error';
                errorDiv.textContent = `Update Error: ${error.message}`;
                
                const formSection = document.querySelector('.form-section');
                if (formSection) {
                    formSection.insertBefore(errorDiv, formSection.firstChild);
                    
                    // Remove error message after 10 seconds
                    setTimeout(() => {
                        if (errorDiv.parentNode) {
                            errorDiv.parentNode.removeChild(errorDiv);
                        }
                    }, 10000);
                }
                
            } finally {
                // Reset button state
                updateBtn.disabled = false;
                updateBtn.textContent = originalText;
            }
        }

        // Download error log
        function downloadErrorLog() {
            window.open('/download_error_log', '_blank');
        }
    </script>
</body>
</html>
        """

def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

if __name__ == '__main__':
    print("🚀 Starting Simple Oracle Fusion Resource Fetcher...")
    
    # Find available port
    port = find_available_port(8000, 10)  # Start with 8000, try up to 8009
    if not port:
        print("❌ Error: No available ports found between 8000-8009")
        exit(1)
    
    print(f"📱 Open your browser and go to one of these URLs:")
    print(f"   • http://localhost:{port}")
    print(f"   • http://127.0.0.1:{port}")
    print("🔧 This server uses Python's built-in HTTP server")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        with socketserver.TCPServer(("", port), OracleFusionHandler) as httpd:
            print(f"✅ Server started successfully on port {port}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}") 