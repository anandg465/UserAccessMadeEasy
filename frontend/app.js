// Oracle Fusion HCM User Management - JavaScript Application

class OracleFusionApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000'; // FastAPI backend URL
        this.oracleConfig = null;
        this.currentSection = 'dashboard';
        this.autoRefreshInterval = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadSettings();
        this.checkConnection();
    }

    setupEventListeners() {
        // Connection form
        document.getElementById('connectionForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.connect();
        });

        // Test connection
        document.getElementById('testConnection').addEventListener('click', () => {
            this.testConnection();
        });

        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.target.closest('.nav-link').dataset.section;
                this.showSection(section);
            });
        });

        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabId = e.target.dataset.tab;
                this.switchTab(tabId);
            });
        });

        // Form submissions
        this.setupFormSubmissions();

        // Settings and Help buttons
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.showModal('settingsModal');
        });

        document.getElementById('helpBtn').addEventListener('click', () => {
            this.showModal('helpModal');
        });

        // Modal close buttons
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modalId = e.target.closest('.modal').id;
                this.closeModal(modalId);
            });
        });

        // Click outside modal to close
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal.id);
                }
            });
        });
    }

    setupFormSubmissions() {
        // Role management forms
        document.getElementById('assignRoleForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.assignRole();
        });

        document.getElementById('removeRoleForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.removeRole();
        });

        // Data security forms
        document.getElementById('assignSecurityForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.assignDataSecurity();
        });

        // AOR forms
        document.getElementById('assignAORForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.assignAOR();
        });

        document.getElementById('removeAORForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.removeAOR();
        });

        // Password management forms
        document.getElementById('resetPasswordForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.resetPassword();
        });

        document.getElementById('updatePasswordForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.updatePassword();
        });

        // Search forms
        document.getElementById('userSearchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.searchUsers();
        });

        document.getElementById('aorSearchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.searchAORs();
        });
    }

    // Connection Management
    async connect() {
        const formData = new FormData(document.getElementById('connectionForm'));
        const config = {
            instance_url: formData.get('instanceUrl'),
            username: formData.get('username'),
            password: formData.get('password')
        };

        this.showLoading();
        
        try {
            // Test the connection first
            const testResult = await this.testConnectionInternal(config);
            if (testResult.success) {
                this.oracleConfig = config;
                this.saveConnectionConfig(config);
                this.showMainApp();
                this.showNotification('Connection established successfully!', 'success');
                this.loadDashboard();
            } else {
                this.showNotification('Connection failed: ' + testResult.error, 'error');
            }
        } catch (error) {
            this.showNotification('Connection error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async testConnection() {
        const formData = new FormData(document.getElementById('connectionForm'));
        const config = {
            instance_url: formData.get('instanceUrl'),
            username: formData.get('username'),
            password: formData.get('password')
        };

        if (!config.instance_url || !config.username || !config.password) {
            this.showNotification('Please fill in all connection fields', 'warning');
            return;
        }

        this.showLoading();
        
        try {
            const result = await this.testConnectionInternal(config);
            if (result.success) {
                this.showNotification('Connection test successful!', 'success');
            } else {
                this.showNotification('Connection test failed: ' + result.error, 'error');
            }
        } catch (error) {
            this.showNotification('Connection test error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async testConnectionInternal(config) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    instance_url: config.instance_url,
                    oracle_username: config.username,
                    oracle_password: config.password
                })
            });

            if (response.ok) {
                return { success: true };
            } else {
                const error = await response.text();
                return { success: false, error: error };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // UI Management
    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show selected section
        document.getElementById(sectionId).classList.add('active');

        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');

        this.currentSection = sectionId;

        // Load section-specific data
        this.loadSectionData(sectionId);
    }

    switchTab(tabId) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');

        // Update tab panels
        const tabContainer = event.target.closest('.management-tabs, .search-tabs');
        const tabContent = tabContainer.nextElementSibling;
        
        tabContent.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        document.getElementById(tabId).classList.add('active');
    }

    showMainApp() {
        document.getElementById('connectionConfig').style.display = 'none';
        document.getElementById('mainApp').style.display = 'flex';
    }

    showModal(modalId) {
        document.getElementById(modalId).style.display = 'flex';
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showNotification(message, type = 'info') {
        const container = document.getElementById('notificationContainer');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="notification-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        container.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    // Data Loading
    loadSectionData(sectionId) {
        switch (sectionId) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'user-details':
                // Clear previous results
                document.getElementById('userDetailsResult').style.display = 'none';
                break;
            case 'logs':
                this.loadLogs();
                break;
        }
    }

    async loadDashboard() {
        if (!this.oracleConfig) return;

        try {
            // Load user count
            await this.loadUserCount();
            
            // Load role count
            await this.loadRoleCount();
            
            // Load AOR count
            await this.loadAORCount();
            
            // Load recent activities
            await this.loadRecentActivities();
        } catch (error) {
            this.showNotification('Error loading dashboard: ' + error.message, 'error');
        }
    }

    async loadUserCount() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/?${new URLSearchParams({
                instance_url: this.oracleConfig.instance_url,
                oracle_username: this.oracleConfig.username,
                oracle_password: this.oracleConfig.password
            })}`);

            if (response.ok) {
                const data = await response.json();
                const count = data.Resources ? data.Resources.length : 0;
                document.getElementById('totalUsers').textContent = count;
            }
        } catch (error) {
            document.getElementById('totalUsers').textContent = 'Error';
        }
    }

    async loadRoleCount() {
        // This would need to be implemented based on your specific role structure
        document.getElementById('activeRoles').textContent = 'N/A';
    }

    async loadAORCount() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/areas-of-responsibility/?${new URLSearchParams({
                instance_url: this.oracleConfig.instance_url,
                oracle_username: this.oracleConfig.username,
                oracle_password: this.oracleConfig.password
            })}`);

            if (response.ok) {
                const data = await response.json();
                const count = data.items ? data.items.length : 0;
                document.getElementById('totalAORs').textContent = count;
            }
        } catch (error) {
            document.getElementById('totalAORs').textContent = 'Error';
        }
    }

    async loadRecentActivities() {
        // This would load from your activity logs
        document.getElementById('recentActivities').textContent = 'N/A';
    }

    // User Management
    async getUserDetails() {
        const username = document.getElementById('userSearchInput').value.trim();
        if (!username) {
            this.showNotification('Please enter a username', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/details`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.displayUserDetails(data);
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayUserDetails(userData) {
        const resultPanel = document.getElementById('userDetailsResult');
        
        resultPanel.innerHTML = `
            <div class="user-details">
                <h3>User Information</h3>
                <div class="user-info-grid">
                    <div class="info-item">
                        <label>Username:</label>
                        <span>${userData.username}</span>
                    </div>
                    <div class="info-item">
                        <label>Person Number:</label>
                        <span>${userData.person_number || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <label>Display Name:</label>
                        <span>${userData.display_name || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <label>Email:</label>
                        <span>${userData.email || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <label>Status:</label>
                        <span class="status-badge ${userData.is_active ? 'active' : 'inactive'}">
                            ${userData.is_active ? 'Active' : 'Inactive'}
                        </span>
                    </div>
                </div>

                <h4>Assigned Roles</h4>
                <div class="roles-list">
                    ${userData.assigned_roles.length > 0 ? 
                        userData.assigned_roles.map(role => `
                            <div class="role-item">
                                <span class="role-name">${role.value || role.displayName}</span>
                                <span class="role-description">${role.description || ''}</span>
                            </div>
                        `).join('') : 
                        '<p>No roles assigned</p>'
                    }
                </div>

                <h4>Areas of Responsibility</h4>
                <div class="aor-list">
                    ${userData.areas_of_responsibility.length > 0 ? 
                        userData.areas_of_responsibility.map(aor => `
                            <div class="aor-item">
                                <span class="aor-name">${aor.name || aor.displayName}</span>
                                <span class="aor-type">${aor.type || 'General'}</span>
                            </div>
                        `).join('') : 
                        '<p>No areas of responsibility assigned</p>'
                    }
                </div>

                <h4>Data Security Contexts</h4>
                <div class="security-list">
                    ${userData.data_security_contexts.length > 0 ? 
                        userData.data_security_contexts.map(security => `
                            <div class="security-item">
                                <span class="security-context">${security.context}</span>
                                <span class="security-value">${security.value}</span>
                            </div>
                        `).join('') : 
                        '<p>No data security contexts assigned</p>'
                    }
                </div>
            </div>
        `;

        resultPanel.style.display = 'block';
    }

    // Role Management
    async assignRole() {
        const username = document.getElementById('assignUsername').value.trim();
        const roleName = document.getElementById('assignRoleName').value.trim();

        if (!username || !roleName) {
            this.showNotification('Please fill in all fields', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/roles/assign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    role_name: roleName,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message, 'success');
                document.getElementById('assignRoleForm').reset();
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async removeRole() {
        const username = document.getElementById('removeUsername').value.trim();
        const roleName = document.getElementById('removeRoleName').value.trim();

        if (!username || !roleName) {
            this.showNotification('Please fill in all fields', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/roles/remove`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    role_name: roleName,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message, 'success');
                document.getElementById('removeRoleForm').reset();
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    // Bulk Operations
    async bulkAssignRoles() {
        const bulkData = document.getElementById('bulkRoleData').value.trim();
        if (!bulkData) {
            this.showNotification('Please enter bulk data', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        const lines = bulkData.split('\n').filter(line => line.trim());
        const assignments = [];

        for (const line of lines) {
            const [username, roleName] = line.split(',').map(item => item.trim());
            if (username && roleName) {
                assignments.push({
                    username: username,
                    role_name: roleName,
                    oracle_config: this.oracleConfig
                });
            }
        }

        if (assignments.length === 0) {
            this.showNotification('No valid assignments found', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/roles/bulk-assign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    assignments: assignments,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(`Bulk operation completed: ${result.successful_operations} successful, ${result.failed_operations} failed`, 'success');
                document.getElementById('bulkRoleData').value = '';
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    // Data Security
    async assignDataSecurity() {
        const username = document.getElementById('securityUsername').value.trim();
        const roleName = document.getElementById('securityRoleName').value.trim();
        const securityContext = document.getElementById('securityContext').value.trim();
        const securityValue = document.getElementById('securityValue').value.trim();

        if (!username || !roleName || !securityContext || !securityValue) {
            this.showNotification('Please fill in all fields', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/data-security/assign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    role_name: roleName,
                    data_security_context: securityContext,
                    data_security_value: securityValue,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message, 'success');
                document.getElementById('assignSecurityForm').reset();
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async bulkAssignSecurity() {
        const bulkData = document.getElementById('bulkSecurityData').value.trim();
        if (!bulkData) {
            this.showNotification('Please enter bulk data', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        const lines = bulkData.split('\n').filter(line => line.trim());
        const assignments = [];

        for (const line of lines) {
            const [username, roleName, securityContext, securityValue] = line.split(',').map(item => item.trim());
            if (username && roleName && securityContext && securityValue) {
                assignments.push({
                    username: username,
                    role_name: roleName,
                    data_security_context: securityContext,
                    data_security_value: securityValue,
                    oracle_config: this.oracleConfig
                });
            }
        }

        if (assignments.length === 0) {
            this.showNotification('No valid assignments found', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/data-security/bulk-assign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    assignments: assignments,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(`Bulk security assignment completed: ${result.successful_operations} successful, ${result.failed_operations} failed`, 'success');
                document.getElementById('bulkSecurityData').value = '';
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    // Areas of Responsibility
    async assignAOR() {
        const username = document.getElementById('aorUsername').value.trim();
        const aorName = document.getElementById('aorName').value.trim();
        const aorType = document.getElementById('aorType').value;

        if (!username || !aorName) {
            this.showNotification('Please fill in all required fields', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/areas-of-responsibility/assign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    aor_name: aorName,
                    aor_type: aorType,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message, 'success');
                document.getElementById('assignAORForm').reset();
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async removeAOR() {
        const username = document.getElementById('removeAORUsername').value.trim();
        const aorId = document.getElementById('removeAORId').value.trim();

        if (!username || !aorId) {
            this.showNotification('Please fill in all fields', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/areas-of-responsibility/remove`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    aor_id: aorId,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message, 'success');
                document.getElementById('removeAORForm').reset();
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async bulkAssignAORs() {
        const bulkData = document.getElementById('bulkAORData').value.trim();
        if (!bulkData) {
            this.showNotification('Please enter bulk data', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        const lines = bulkData.split('\n').filter(line => line.trim());
        const assignments = [];

        for (const line of lines) {
            const [username, aorName, aorType] = line.split(',').map(item => item.trim());
            if (username && aorName) {
                assignments.push({
                    username: username,
                    aor_name: aorName,
                    aor_type: aorType || 'GENERAL',
                    oracle_config: this.oracleConfig
                });
            }
        }

        if (assignments.length === 0) {
            this.showNotification('No valid assignments found', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/areas-of-responsibility/bulk-assign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    assignments: assignments,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(`Bulk AOR assignment completed: ${result.successful_operations} successful, ${result.failed_operations} failed`, 'success');
                document.getElementById('bulkAORData').value = '';
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    // Excel Upload
    async uploadExcelFile() {
        const fileInput = document.getElementById('excelFile');
        const operationType = document.getElementById('operationType').value;

        if (!fileInput.files[0]) {
            this.showNotification('Please select a file', 'warning');
            return;
        }

        if (!operationType) {
            this.showNotification('Please select an operation type', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('operation_type', operationType);
            formData.append('instance_url', this.oracleConfig.instance_url);
            formData.append('oracle_username', this.oracleConfig.username);
            formData.append('oracle_password', this.oracleConfig.password);

            const response = await fetch(`${this.apiBaseUrl}/upload/excel`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                this.displayUploadResult(result);
                this.showNotification(`Upload completed: ${result.success_count} successful, ${result.failure_count} failed`, 'success');
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayUploadResult(result) {
        const resultPanel = document.getElementById('uploadResult');
        
        resultPanel.innerHTML = `
            <h3>Upload Results</h3>
            <div class="upload-summary">
                <div class="summary-item">
                    <span class="label">Total Records:</span>
                    <span class="value">${result.success_count + result.failure_count}</span>
                </div>
                <div class="summary-item">
                    <span class="label">Successful:</span>
                    <span class="value success">${result.success_count}</span>
                </div>
                <div class="summary-item">
                    <span class="label">Failed:</span>
                    <span class="value error">${result.failure_count}</span>
                </div>
            </div>

            ${result.errors.length > 0 ? `
                <h4>Errors</h4>
                <div class="error-list">
                    ${result.errors.map(error => `
                        <div class="error-item">
                            <span class="error-row">Row ${error.row}:</span>
                            <span class="error-message">${error.error}</span>
                        </div>
                    `).join('')}
                </div>
            ` : ''}

            ${result.processed_records.length > 0 ? `
                <h4>Processed Records</h4>
                <div class="processed-list">
                    ${result.processed_records.map(record => `
                        <div class="processed-item">
                            <span class="processed-row">Row ${record.row}:</span>
                            <span class="processed-status">${record.status}</span>
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        `;

        resultPanel.style.display = 'block';
    }

    // Template Downloads
    downloadTemplate(type) {
        let content = '';
        let filename = '';

        switch (type) {
            case 'role_assignment':
                content = 'username,role_name\njohn.doe,HR_MANAGER\njane.smith,EMPLOYEE';
                filename = 'role_assignment_template.csv';
                break;
            case 'data_security':
                content = 'username,role_name,security_context,security_value\njohn.doe,HR_MANAGER,DEPARTMENT,IT\njane.smith,EMPLOYEE,LOCATION,NYC';
                filename = 'data_security_template.csv';
                break;
            case 'aor_assignment':
                content = 'username,aor_name,aor_type\njohn.doe,HR_DEPARTMENT,HR\njane.smith,IT_SUPPORT,IT';
                filename = 'aor_assignment_template.csv';
                break;
        }

        const blob = new Blob([content], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }

    // Search Functions
    async searchUsers() {
        const username = document.getElementById('searchUsername').value.trim();
        const email = document.getElementById('searchEmail').value.trim();
        const active = document.getElementById('searchActive').value;

        if (!username && !email && !active) {
            this.showNotification('Please enter at least one search criteria', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const searchCriteria = {};
            if (username) searchCriteria.username = username;
            if (email) searchCriteria.email = email;
            if (active) searchCriteria.active = active;

            const response = await fetch(`${this.apiBaseUrl}/users/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    search_criteria: searchCriteria,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.displaySearchResults(data, 'users');
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async searchAORs() {
        const aorName = document.getElementById('searchAORName').value.trim();
        const aorType = document.getElementById('searchAORType').value;

        if (!aorName && !aorType) {
            this.showNotification('Please enter at least one search criteria', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const searchCriteria = {};
            if (aorName) searchCriteria.name = aorName;
            if (aorType) searchCriteria.type = aorType;

            const response = await fetch(`${this.apiBaseUrl}/areas-of-responsibility/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    search_criteria: searchCriteria,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.displaySearchResults(data, 'aors');
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displaySearchResults(data, type) {
        const resultPanel = document.getElementById('searchResult');
        
        if (type === 'users') {
            const users = data.Resources || [];
            resultPanel.innerHTML = `
                <h3>Search Results (${users.length} users found)</h3>
                <div class="search-results">
                    ${users.length > 0 ? users.map(user => `
                        <div class="user-result">
                            <div class="user-info">
                                <span class="username">${user.userName}</span>
                                <span class="email">${user.emails?.[0]?.value || 'N/A'}</span>
                                <span class="status ${user.active ? 'active' : 'inactive'}">${user.active ? 'Active' : 'Inactive'}</span>
                            </div>
                        </div>
                    `).join('') : '<p>No users found</p>'}
                </div>
            `;
        } else if (type === 'aors') {
            const aors = data.items || [];
            resultPanel.innerHTML = `
                <h3>Search Results (${aors.length} AORs found)</h3>
                <div class="search-results">
                    ${aors.length > 0 ? aors.map(aor => `
                        <div class="aor-result">
                            <div class="aor-info">
                                <span class="aor-name">${aor.name}</span>
                                <span class="aor-type">${aor.type || 'General'}</span>
                            </div>
                        </div>
                    `).join('') : '<p>No AORs found</p>'}
                </div>
            `;
        }

        resultPanel.style.display = 'block';
    }

    // Password Management
    async resetPassword() {
        const username = document.getElementById('resetUsername').value.trim();
        const newPassword = document.getElementById('newPassword').value;

        if (!username || !newPassword) {
            this.showNotification('Please fill in all fields', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/password/reset`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    new_password: newPassword,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message, 'success');
                document.getElementById('resetPasswordForm').reset();
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async updatePassword() {
        const username = document.getElementById('updateUsername').value.trim();
        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('updateNewPassword').value;

        if (!username || !currentPassword || !newPassword) {
            this.showNotification('Please fill in all fields', 'warning');
            return;
        }

        if (!this.oracleConfig) {
            this.showNotification('Please connect to Oracle first', 'warning');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/password/update`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    current_password: currentPassword,
                    new_password: newPassword,
                    oracle_config: this.oracleConfig
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification(result.message, 'success');
                document.getElementById('updatePasswordForm').reset();
            } else {
                const error = await response.text();
                this.showNotification('Error: ' + error, 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    // Logs
    async loadLogs() {
        // This would load activity logs from your backend
        const logsContent = document.getElementById('logsContent');
        logsContent.innerHTML = '<p>No logs available</p>';
    }

    clearLogs() {
        const logsContent = document.getElementById('logsContent');
        logsContent.innerHTML = '<p>Logs cleared</p>';
    }

    // Settings Management
    loadSettings() {
        const settings = localStorage.getItem('oracleFusionSettings');
        if (settings) {
            const parsed = JSON.parse(settings);
            
            // Apply theme
            if (parsed.theme) {
                document.documentElement.setAttribute('data-theme', parsed.theme);
                document.getElementById('appTheme').value = parsed.theme;
            }
            
            // Apply branding
            if (parsed.branding) {
                this.applyBranding(parsed.branding);
            }
            
            // Apply auto refresh
            if (parsed.autoRefresh) {
                document.getElementById('autoRefresh').value = parsed.autoRefresh;
                this.setupAutoRefresh(parsed.autoRefresh);
            }
        }

        // Load connection config
        const connectionConfig = localStorage.getItem('oracleConnectionConfig');
        if (connectionConfig) {
            const config = JSON.parse(connectionConfig);
            document.getElementById('instanceUrl').value = config.instance_url || '';
            document.getElementById('username').value = config.username || '';
            // Don't auto-fill password for security
        }
    }

    saveSettings() {
        const settings = {
            theme: document.getElementById('appTheme').value,
            autoRefresh: parseInt(document.getElementById('autoRefresh').value) || 0,
            branding: {
                companyName: document.getElementById('companyName').value,
                primaryColor: document.getElementById('primaryColor').value,
                secondaryColor: document.getElementById('secondaryColor').value,
                logoUrl: document.getElementById('logoUrl').value
            }
        };

        localStorage.setItem('oracleFusionSettings', JSON.stringify(settings));
        
        // Apply settings
        document.documentElement.setAttribute('data-theme', settings.theme);
        this.applyBranding(settings.branding);
        this.setupAutoRefresh(settings.autoRefresh);
        
        this.showNotification('Settings saved successfully', 'success');
        this.closeModal('settingsModal');
    }

    applyBranding(branding) {
        if (branding.primaryColor) {
            document.documentElement.style.setProperty('--primary-color', branding.primaryColor);
        }
        if (branding.secondaryColor) {
            document.documentElement.style.setProperty('--secondary-color', branding.secondaryColor);
        }
        if (branding.companyName) {
            document.querySelector('.app-subtitle').textContent = branding.companyName;
        }
        if (branding.logoUrl) {
            // Apply logo if needed
        }
    }

    setupAutoRefresh(seconds) {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
        
        if (seconds > 0) {
            this.autoRefreshInterval = setInterval(() => {
                if (this.currentSection === 'dashboard') {
                    this.loadDashboard();
                }
            }, seconds * 1000);
        }
    }

    saveConnectionConfig(config) {
        localStorage.setItem('oracleConnectionConfig', JSON.stringify(config));
    }

    checkConnection() {
        const connectionConfig = localStorage.getItem('oracleConnectionConfig');
        if (connectionConfig) {
            const config = JSON.parse(connectionConfig);
            if (config.instance_url && config.username) {
                // Auto-connect if we have saved credentials
                this.oracleConfig = config;
                this.showMainApp();
                this.loadDashboard();
            }
        }
    }
}

// Global functions for HTML onclick handlers
function showSection(sectionId) {
    app.showSection(sectionId);
}

function getUserDetails() {
    app.getUserDetails();
}

function bulkAssignRoles() {
    app.bulkAssignRoles();
}

function bulkAssignSecurity() {
    app.bulkAssignSecurity();
}

function bulkAssignAORs() {
    app.bulkAssignAORs();
}

function uploadExcelFile() {
    app.uploadExcelFile();
}

function downloadTemplate(type) {
    app.downloadTemplate(type);
}

function loadUserCount() {
    app.loadUserCount();
}

function loadRoleCount() {
    app.loadRoleCount();
}

function loadAORCount() {
    app.loadAORCount();
}

function loadRecentActivities() {
    app.loadRecentActivities();
}

function loadLogs() {
    app.loadLogs();
}

function clearLogs() {
    app.clearLogs();
}

function saveSettings() {
    app.saveSettings();
}

function closeModal(modalId) {
    app.closeModal(modalId);
}

// Initialize the application
const app = new OracleFusionApp();
