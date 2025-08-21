#!/usr/bin/env python3
"""
Oracle Fusion API Proxy Server
Bypasses CORS restrictions by making server-side requests to Oracle Fusion
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import base64
import json
import os
import socket
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oracle Fusion Resource Fetcher (Server Proxy)</title>
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

        .form-group input, .form-group select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus, .form-group select:focus {
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

        .progress-section {
            padding: 40px;
            display: none;
        }

        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e1e8ed;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 15px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
        }

        .progress-text {
            text-align: center;
            color: #666;
            font-size: 1.1em;
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

        .field-selector {
            margin-bottom: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }

        .field-selector h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }

        .field-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
        }

        .field-checkbox {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .field-checkbox input[type="checkbox"] {
            width: auto;
            margin: 0;
        }

        .field-checkbox label {
            margin: 0;
            font-size: 0.9em;
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
            <p>Server-side proxy solution - No CORS issues!</p>
        </div>

        <div class="form-section">
            <div class="server-info">
                <strong>✅ Server Proxy Active:</strong> This tool uses a server-side proxy to bypass CORS restrictions. 
                Your requests are sent through the server, not directly from the browser.
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

                <div class="field-selector">
                    <h3>Select Fields to Display:</h3>
                    <div class="field-grid" id="fieldGrid">
                        <!-- Fields will be populated dynamically -->
                    </div>
                </div>

                <button type="submit" class="btn" id="fetchBtn">
                    <span class="loading" style="display: none;"></span>
                    Fetch Resources
                </button>
            </form>
        </div>

        <div class="progress-section" id="progressSection">
            <h3>Fetching Resources...</h3>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="progress-text" id="progressText">Initializing...</div>
        </div>

        <div class="results-section" id="resultsSection">
            <div class="results-header">
                <div class="results-count" id="resultsCount"></div>
                <button class="export-btn" onclick="exportToCSV()">Export to CSV</button>
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
        let selectedFields = [];

        // Available fields based on Oracle Fusion API documentation
        const availableFields = [
            { key: 'ResourceId', label: 'Resource ID' },
            { key: 'PersonId', label: 'Person ID' },
            { key: 'PersonNumber', label: 'Person Number' },
            { key: 'HCMPersonName', label: 'HCM Person Name' },
            { key: 'FirstName', label: 'First Name' },
            { key: 'LastName', label: 'Last Name' },
            { key: 'ResourceName', label: 'Resource Name' },
            { key: 'Email', label: 'Email' },
            { key: 'FromDate', label: 'From Date' },
            { key: 'ToDate', label: 'To Date' },
            { key: 'PhoneNumber', label: 'Phone Number' },
            { key: 'ManagerId', label: 'Manager ID' },
            { key: 'ManagerName', label: 'Manager Name' },
            { key: 'ManagerEmail', label: 'Manager Email' },
            { key: 'CalendarId', label: 'Calendar ID' },
            { key: 'CalendarName', label: 'Calendar Name' },
            { key: 'PrimaryProjectRoleId', label: 'Primary Project Role ID' },
            { key: 'PrimaryProjectRoleName', label: 'Primary Project Role Name' },
            { key: 'BillRate', label: 'Bill Rate' },
            { key: 'BillRateCurrencyCode', label: 'Bill Rate Currency' },
            { key: 'CostRate', label: 'Cost Rate' },
            { key: 'CostRateCurrencyCode', label: 'Cost Rate Currency' },
            { key: 'ManageResourceStaffingFlag', label: 'Manage Resource Staffing' },
            { key: 'ResourcePoolId', label: 'Resource Pool ID' },
            { key: 'ResourcePoolName', label: 'Resource Pool Name' },
            { key: 'PoolMembershipFromDate', label: 'Pool Membership From Date' },
            { key: 'ProjectId', label: 'Project ID' },
            { key: 'ProjectName', label: 'Project Name' },
            { key: 'ExternalId', label: 'External ID' }
        ];

        // Initialize field selector
        function initializeFieldSelector() {
            const fieldGrid = document.getElementById('fieldGrid');
            fieldGrid.innerHTML = '';

            availableFields.forEach(field => {
                const div = document.createElement('div');
                div.className = 'field-checkbox';
                div.innerHTML = `
                    <input type="checkbox" id="field_${field.key}" value="${field.key}" checked>
                    <label for="field_${field.key}">${field.label}</label>
                `;
                fieldGrid.appendChild(div);
            });
        }

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

        // Get selected fields
        function getSelectedFields() {
            const checkboxes = document.querySelectorAll('#fieldGrid input[type="checkbox"]:checked');
            return Array.from(checkboxes).map(cb => cb.value);
        }

        // Show progress
        function showProgress() {
            const progressSection = document.getElementById('progressSection');
            const resultsSection = document.getElementById('resultsSection');
            
            if (progressSection) {
                progressSection.style.display = 'block';
            }
            if (resultsSection) {
                resultsSection.style.display = 'none';
            }
        }

        // Hide progress
        function hideProgress() {
            const progressSection = document.getElementById('progressSection');
            if (progressSection) {
                progressSection.style.display = 'none';
            }
        }

        // Update progress
        function updateProgress(current, total) {
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            
            if (!progressFill || !progressText) {
                console.warn('Progress elements not found');
                return;
            }
            
            const percentage = total > 0 ? (current / total) * 100 : 0;
            progressFill.style.width = percentage + '%';
            progressText.textContent = 
                `Fetched ${current} of ${total} records (${Math.round(percentage)}%)`;
        }

        // Show results
        function showResults() {
            const resultsSection = document.getElementById('resultsSection');
            const resultsCount = document.getElementById('resultsCount');
            
            if (resultsSection) {
                resultsSection.style.display = 'block';
            }
            if (resultsCount) {
                resultsCount.textContent = `Total Resources: ${allResources.length}`;
            }
        }

        // Create table headers
        function createTableHeaders() {
            const thead = document.getElementById('tableHead');
            if (!thead) {
                console.error('Table head element not found');
                return;
            }
            
            thead.innerHTML = '';
            
            const tr = document.createElement('tr');
            selectedFields.forEach(field => {
                const th = document.createElement('th');
                th.textContent = availableFields.find(f => f.key === field)?.label || field;
                tr.appendChild(th);
            });
            thead.appendChild(tr);
        }

        // Populate table data
        function populateTableData() {
            const tbody = document.getElementById('tableBody');
            if (!tbody) {
                console.error('Table body element not found');
                return;
            }
            
            tbody.innerHTML = '';

            allResources.forEach(resource => {
                const tr = document.createElement('tr');
                selectedFields.forEach(field => {
                    const td = document.createElement('td');
                    const value = resource[field];
                    td.textContent = value !== null && value !== undefined ? value : '';
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
        }

        // Fetch resources using server proxy
        async function fetchAllResources(baseUrl, username, password) {
            const requestData = {
                base_url: baseUrl,
                username: username,
                password: password
            };

            console.log('Sending request to server proxy...');
            
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
            
            selectedFields = getSelectedFields();
            
            if (selectedFields.length === 0) {
                alert('Please select at least one field to display.');
                return;
            }

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
                
                showProgress();
                updateProgress(0, 'Connecting to Oracle Fusion...');

                // Fetch all resources through server proxy
                allResources = await fetchAllResources(baseUrl, username, password);
                
                updateProgress(allResources.length, allResources.length);
                
                // Create and populate table
                createTableHeaders();
                populateTableData();
                
                hideProgress();
                showResults();

            } catch (error) {
                console.error('Error:', error);
                hideProgress();
                
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
            if (allResources.length === 0) {
                alert('No data to export.');
                return;
            }

            // Create CSV content
            const headers = selectedFields.map(field => 
                availableFields.find(f => f.key === field)?.label || field
            );
            
            const csvContent = [
                headers.join(','),
                ...allResources.map(resource => 
                    selectedFields.map(field => {
                        const value = resource[field];
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

        // Initialize the page
        document.addEventListener('DOMContentLoaded', function() {
            initializeFieldSelector();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/fetch_resources', methods=['POST'])
def fetch_resources():
    """Proxy endpoint to fetch Oracle Fusion resources"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        base_url = data.get('base_url', '').rstrip('/')
        username = data.get('username')
        password = data.get('password')
        
        if not all([base_url, username, password]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
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
                    return jsonify({'error': 'Authentication failed. Please check your username and password.'}), 401
                elif response.status_code == 403:
                    return jsonify({'error': 'Access denied. You may not have permission to access this resource.'}), 403
                elif response.status_code == 404:
                    return jsonify({'error': 'API endpoint not found. Please check your base URL.'}), 404
                elif response.status_code != 200:
                    return jsonify({'error': f'HTTP {response.status_code}: {response.text}'}), response.status_code
                
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
                return jsonify({'error': 'Request timeout. The Oracle Fusion server took too long to respond.'}), 408
            except requests.exceptions.ConnectionError:
                return jsonify({'error': 'Connection error. Please check your base URL and internet connection.'}), 503
            except Exception as e:
                print(f"Error fetching data: {str(e)}")
                return jsonify({'error': f'Error fetching data: {str(e)}'}), 500
        
        print(f"Total resources fetched: {len(all_resources)}")
        return jsonify({
            'success': True,
            'resources': all_resources,
            'count': len(all_resources),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Oracle Fusion Proxy Server...")
    
    # Check for environment variable first, then find available port
    port = os.environ.get('FLASK_PORT')
    if port:
        try:
            port = int(port)
        except ValueError:
            port = None
    
    if not port:
        port = find_available_port(5001, 10)  # Start with 5001, try up to 5010
        if not port:
            print("❌ Error: No available ports found between 5001-5010")
            exit(1)
    
    print(f"📱 Open your browser and go to one of these URLs:")
    print(f"   • http://localhost:{port}")
    print(f"   • http://127.0.0.1:{port}")
    print(f"   • http://0.0.0.0:{port}")
    print("🔧 This server bypasses CORS restrictions by making server-side requests")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=port)
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        print("🔄 Trying alternative host binding...")
        try:
            app.run(debug=True, host='localhost', port=port)
        except OSError as e2:
            print(f"❌ Error with localhost: {e2}")
            print("🔄 Trying 0.0.0.0 binding...")
            app.run(debug=True, host='0.0.0.0', port=port) 