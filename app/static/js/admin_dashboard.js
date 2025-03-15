document.addEventListener('DOMContentLoaded', function() {
    initTabs();
    
    loadDashboardStats();
    initCharts();
    loadRecentActivity();
    
    initUserManagement();
    
    
    //initOrderManagement();
    
    

    loadAdminProfile();
    initPasswordForm();
    
    initModals();
    initNotifications();
});

function initTabs() {
    const menuItems = document.querySelectorAll('.admin-menu li');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            menuItems.forEach(i => i.classList.remove('active'));
            
            this.classList.add('active');
            
            const tabs = document.querySelectorAll('.admin-tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            const tabToShow = document.getElementById(`${this.dataset.tab}-tab`);
            if (tabToShow) {
                tabToShow.classList.add('active');
            }
        });
    });
}

function loadDashboardStats() {
    fetch('/api/admin/users/count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-users').textContent = data.count || 0;
        })
        .catch(error => {
            console.error('Error fetching user count:', error);
            document.getElementById('total-users').textContent = 'Error';
        });
    
    fetch('/api/admin/orders/count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-orders').textContent = data.count || 0;
        })
        .catch(error => {
            console.error('Error fetching order count:', error);
            document.getElementById('total-orders').textContent = 'Error';
        });
    

}

function loadAdminProfile() {
    fetch('/api/admin/profile')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('admin-username').value = data.admin.username || '';
                document.getElementById('admin-email').value = data.admin.email || '';
                document.getElementById('admin-name').value = data.admin.name || '';
                document.getElementById('admin-surname').value = data.admin.surname || '';
            } else {
                console.error('Error loading admin profile:', data.error);
            }
        })
        .catch(error => {
            console.error('Error fetching admin profile:', error);
        });
}

function initPasswordForm() {
    document.getElementById('change-password-form').addEventListener('submit', function (e) {
        e.preventDefault();

        const currentPassword = document.getElementById('current-password').value;
        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (newPassword !== confirmPassword) {
            alert('New passwords do not match!');
            return;
        }

        fetch('/api/admin/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Password changed successfully!');
                    document.getElementById('change-password-form').reset();
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error changing password:', error);
            });
    });
}

function initCharts() {
    fetch('/api/admin/orders/stats')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('ordersChartCanvas').getContext('2d');
            
            const chartData = data.chartData || {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                values: [12, 19, 3, 5, 2, 3]
            };
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: 'Orders',
                        data: chartData.values,
                        borderColor: '#2f1c0e',
                        backgroundColor: 'rgba(47, 28, 14, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading orders chart:', error);
            document.getElementById('orders-chart').innerHTML = '<p class="loading">Error loading chart data</p>';
        });
    
    
}

function initModals() {
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.close-modal');

    // Open modal when clicking on a trigger element
    document.querySelectorAll('[data-modal]').forEach(trigger => {
        trigger.addEventListener('click', function () {
            const modalId = this.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('show');
            }
        });
    });

    // Close modal when clicking on the close button
    closeButtons.forEach(button => {
        button.addEventListener('click', function () {
            this.closest('.modal').classList.remove('show');
        });
    });

    // Close modal when clicking outside the modal content
    modals.forEach(modal => {
        modal.addEventListener('click', function (event) {
            if (event.target === modal) {
                modal.classList.remove('show');
            }
        });
    });
}

function initNotifications() {
    const notification = document.getElementById('notification');
    const closeBtn = notification ? notification.querySelector('.notification-close') : null;

    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            notification.classList.remove('show');
        });
    }
}

// Function to show notifications dynamically
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (!notification) return;

    notification.classList.remove('error', 'success', 'info');
    notification.classList.add(type);
    
    const messageElement = notification.querySelector('#notification-message');
    if (messageElement) {
        messageElement.textContent = message;
    }

    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
}

function loadRecentActivity() {
    const activityList = document.getElementById('activity-list');
    
    fetch('/api/admin/activity')
        .then(response => response.json())
        .then(data => {
            activityList.innerHTML = '';
            
            if (data.length === 0) {
                activityList.innerHTML = '<li class="activity-item">No recent activity found</li>';
                return;
            }
            
            data.forEach(activity => {
                const li = document.createElement('li');
                li.className = 'activity-item';
                
                let iconClass = 'fas fa-info-circle';
                let iconClassType = '';
                
                if (activity.type === 'user') {
                    iconClass = 'fas fa-user';
                    iconClassType = 'activity-icon-user';
                } else if (activity.type === 'order') {
                    iconClass = 'fas fa-shopping-cart';
                    iconClassType = 'activity-icon-order';
                }
                
                const activityDate = new Date(activity.time);
                const formattedTime = formatRelativeTime(activityDate);
                
                li.innerHTML = `
                    <i class="${iconClass} ${iconClassType}"></i>
                    <span>${activity.message}</span>
                    <span class="activity-time">${formattedTime}</span>
                `;
                
                activityList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error loading activity:', error);
            activityList.innerHTML = '<li class="activity-item">Error loading activity data</li>';
        });
}

function initUserManagement() {
    loadUsers(1);
    
    const searchInput = document.getElementById('user-search');
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            loadUsers(1, this.value);
        }, 500);
    });
    
    document.getElementById('refresh-users').addEventListener('click', function() {
        searchInput.value = '';
        loadUsers(1);
    });
    
    document.getElementById('add-user').addEventListener('click', function() {
        document.getElementById('edit-user-form').reset();
        document.getElementById('user-modal-title').textContent = 'Add New User';
        
        const modal = document.getElementById('edit-user-modal');
        modal.classList.add('show');
    });

    document.getElementById('edit-user-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const userId = document.getElementById('edit-user-id').value;
        const formData = new FormData(this);
        const userData = {
            username: formData.get('username'),
            name: formData.get('name'),
            surname: formData.get('surname'),
            email: formData.get('email'),
            role: formData.get('role')
        };
        
        if (userId) {
            fetch(`/api/admin/users/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to update user');
                }
                return response.json();
            })
            .then(data => {
                showNotification('User updated successfully', 'success');
                document.getElementById('edit-user-modal').classList.remove('show');
                loadUsers(currentPage, searchInput.value);
            })
            .catch(error => {
                console.error('Error updating user:', error);
                showNotification('Error updating user', 'error');
            });
        } else {
            userData.password = 'DefaultPassword123';
            
            fetch('/api/admin/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to create user');
                }
                return response.json();
            })
            .then(data => {
                showNotification('User created successfully', 'success');
                document.getElementById('edit-user-modal').classList.remove('show');
                loadUsers(1, searchInput.value);
            })
            .catch(error => {
                console.error('Error creating user:', error);
                showNotification('Error creating user', 'error');
            });
        }
    });

    // Reset password to the default ("Password123")
    document.getElementById("reset-password-btn").addEventListener("click", function () {
        const userId = document.getElementById("edit-user-id").value;
        
        if (!userId) {
            alert("User ID is missing!");
            return;
        }
    
        // Show confirmation dialog before making the API call
        if (!confirm("Are you sure you want to reset this user's password to default? (Password123)")) {
            return; // Stop if the admin cancels
        }
    
        fetch(`/api/admin/users/${userId}/reset-password`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Password reset successfully! The user must log in again.");
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while resetting the password.");
        });
    });    
    
    document.getElementById('prev-page').addEventListener('click', function() {
        if (currentPage > 1) {
            loadUsers(currentPage - 1, searchInput.value);
        }
    });

    document.getElementById('next-page').addEventListener('click', function() {
        loadUsers(currentPage + 1, searchInput.value);
    });
}

let currentPage = 1;
let totalPages = 1;

function loadUsers(page, search = '') {
    const usersTable = document.getElementById('users-table').querySelector('tbody');
    usersTable.innerHTML = '<tr class="loading-row"><td colspan="7">Loading users...</td></tr>';
    
    currentPage = page;
    
    fetch(`/api/admin/users?page=${page}&search=${encodeURIComponent(search)}`)
        .then(response => response.json())
        .then(data => {
            usersTable.innerHTML = '';
            
            if (data.users.length === 0) {
                usersTable.innerHTML = '<tr><td colspan="7">No users found</td></tr>';
                return;
            }
            
            totalPages = data.totalPages || 1;
            document.getElementById('current-page').textContent = currentPage;
            document.getElementById('total-pages').textContent = totalPages;
            
            document.getElementById('prev-page').disabled = currentPage <= 1;
            document.getElementById('next-page').disabled = currentPage >= totalPages;
            
            data.users.forEach(user => {
                const tr = document.createElement('tr');
                
                const formattedDate = new Date(user.created_at).toLocaleDateString();
                
                tr.innerHTML = `
                    <td>${user._id}</td>
                    <td>${user.username}</td>
                    <td>${user.name} ${user.surname}</td>
                    <td>${user.email}</td>
                    <td>${user.role}</td>
                    <td>${formattedDate}</td>
                    <td class="table-actions">
                        <button class="action-btn edit-btn" data-id="${user._id}" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete-btn" data-id="${user._id}" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                
                usersTable.appendChild(tr);
                
                const editBtn = tr.querySelector('.edit-btn');
                const deleteBtn = tr.querySelector('.delete-btn');
                
                editBtn.addEventListener('click', function() {
                    editUser(user._id);
                });
                
                deleteBtn.addEventListener('click', function() {
                    deleteUser(user._id);
                });
            });
        })
        .catch(error => {
            console.error('Error loading users:', error);
            usersTable.innerHTML = '<tr><td colspan="7">Error loading users</td></tr>';
        });
}

function editUser(userId) {
    fetch(`/api/admin/users/${userId}`)
        .then(response => response.json())
        .then(user => {
            document.getElementById('edit-user-id').value = user._id;
            document.getElementById('edit-username').value = user.username;
            document.getElementById('edit-name').value = user.name;
            document.getElementById('edit-surname').value = user.surname;
            document.getElementById('edit-email').value = user.email;
            document.getElementById('edit-role').value = user.role;
            
            document.getElementById('user-modal-title').textContent = 'Edit User';
            document.getElementById('edit-user-modal').classList.add('show');
        })
        .catch(error => {
            console.error('Error fetching user details:', error);
            showNotification('Error fetching user details', 'error');
        });
}

function showConfirmation(message, onConfirm) {
    const confirmed = confirm(message); // Simple browser confirmation dialog
    if (confirmed) {
        onConfirm();
    }
}

function deleteUser(userId) {
    showConfirmation('Are you sure you want to delete this user?', () => {
        fetch(`/api/admin/users/${userId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to delete user');
            }
            return response.json();
        })
        .then(data => {
            showNotification('User deleted successfully', 'success');
            loadUsers(currentPage, document.getElementById('user-search').value);
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            showNotification('Error deleting user', 'error');
        });
    });
}

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (!notification) return;

    notification.classList.remove('error', 'success', 'info');
    notification.classList.add(type);

    const messageElement = notification.querySelector('#notification-message');
    if (messageElement) {
        messageElement.textContent = message;
    }

    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
}
