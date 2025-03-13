from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_required, current_user
from app.models import User
from bson import ObjectId
from functools import wraps
from app.database import db, users_collection, orders_collection
from datetime import datetime
import json
import csv
import io

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('routes.login'))
        
        if current_user.role != 'admin':
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for('routes.home'))
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    return render_template('admin_dashboard.html')


@admin_bp.route('/api/admin/users/count')
@login_required
@admin_required
def get_users_count():
    count = users_collection.count_documents({})
    return jsonify({'count': count})

@admin_bp.route('/api/admin/orders/count')
@login_required
@admin_required
def get_orders_count():
    count = orders_collection.count_documents({})
    return jsonify({'count': count})

@admin_bp.route('/api/admin/orders/stats')
@login_required
@admin_required
def get_orders_stats():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    values = [12, 19, 3, 5, 2, 3]
    
    return jsonify({
        'chartData': {
            'labels': months,
            'values': values
        }
    })


@admin_bp.route('/api/admin/activity')
@login_required
@admin_required
def get_activity():
    
    activities = [
        {
            'type': 'user',
            'message': 'New user John Doe registered',
            'time': datetime.now().isoformat()
        },
        {
            'type': 'order',
            'message': 'New order #123456 received',
            'time': datetime.now().isoformat()
        },
        {
            'type': 'product',
            'message': 'Product Crystal Ring updated',
            'time': datetime.now().isoformat()
        },
        {
            'type': 'order',
            'message': 'Order #123455 status changed to Shipped',
            'time': datetime.now().isoformat()
        },
        {
            'type': 'user',
            'message': 'User Jane Doe updated their profile',
            'time': datetime.now().isoformat()
        }
    ]
    
    return jsonify(activities)

@admin_bp.route('/api/admin/users')
@login_required
@admin_required
def get_users():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    per_page = 10
    
    filter_query = {}
    if search:
        filter_query = {
            "$or": [
                {"username": {"$regex": search, "$options": "i"}},
                {"name": {"$regex": search, "$options": "i"}},
                {"surname": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}}
            ]
        }
    
    total_records = users_collection.count_documents(filter_query)
    total_pages = (total_records // per_page) + (1 if total_records % per_page > 0 else 0)
    
    skip = (page - 1) * per_page
    users_cursor = users_collection.find(filter_query).skip(skip).limit(per_page).sort("created_at", -1)
    
    users = []
    for user in users_cursor:
        user['_id'] = str(user['_id'])  
        users.append(user)
    
    return jsonify({
        'users': users,
        'totalPages': total_pages,
        'currentPage': page,
        'totalRecords': total_records
    })

@admin_bp.route('/api/admin/users/<user_id>')
@login_required
@admin_required
def get_user(user_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user['_id'] = str(user['_id'])
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/users', methods=['POST'])
@login_required
@admin_required
def add_user():
    try:
        data = request.json
        
        if users_collection.find_one({"username": data['username']}):
            return jsonify({'error': 'Username already exists'}), 400
        
        if users_collection.find_one({"email": data['email']}):
            return jsonify({'error': 'Email already exists'}), 400
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            name=data['name'],
            surname=data['surname'],
            role=data['role'],
            password=data['password'] 
        )
        
        user_dict = new_user.__dict__
        
        result = users_collection.insert_one(user_dict)
        
        return jsonify({
            'message': 'User created successfully',
            'id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/users/<user_id>', methods=['PUT'])
@login_required
@admin_required
def update_user(user_id):
    try:
        data = request.json
        
        username_check = users_collection.find_one({"username": data['username'], "_id": {"$ne": ObjectId(user_id)}})
        if username_check:
            return jsonify({'error': 'Username already exists'}), 400
        
        email_check = users_collection.find_one({"email": data['email'], "_id": {"$ne": ObjectId(user_id)}})
        if email_check:
            return jsonify({'error': 'Email already exists'}), 400
        
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "username": data['username'],
                "email": data['email'],
                "name": data['name'],
                "surname": data['surname'],
                "role": data['role']
            }}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/users/<user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    try:
        if str(current_user._id) == user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/users/<user_id>/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_user_password(user_id):
    try:
        default_password = 'DefaultPassword123'
        
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        user = User(**user_data)
        user.set_password(default_password)
        
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password_hash": user.password_hash}}
        )
        
        return jsonify({
            'message': 'Password reset successfully',
            'password': default_password
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@admin_bp.route('/api/admin/orders')
@login_required
@admin_required
def get_orders():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    per_page = 10
    
    filter_query = {}
    if search:
        try:
            if ObjectId.is_valid(search):
                filter_query["_id"] = ObjectId(search)
            else:
                filter_query = {
                    "$or": [
                        {"user_id": {"$regex": search, "$options": "i"}},
                        {"user_name": {"$regex": search, "$options": "i"}},
                        {"user_email": {"$regex": search, "$options": "i"}},
                        {"status": {"$regex": search, "$options": "i"}}
                    ]
                }
        except:
            filter_query = {
                "$or": [
                    {"user_id": {"$regex": search, "$options": "i"}},
                    {"user_name": {"$regex": search, "$options": "i"}},
                    {"user_email": {"$regex": search, "$options": "i"}},
                    {"status": {"$regex": search, "$options": "i"}}
                ]
            }
    
    total_records = orders_collection.count_documents(filter_query)
    total_pages = (total_records // per_page) + (1 if total_records % per_page > 0 else 0)
    
    skip = (page - 1) * per_page
    orders_cursor = orders_collection.find(filter_query).skip(skip).limit(per_page).sort("created_at", -1)
    
    orders = []
    for order in orders_cursor:
        order['_id'] = str(order['_id'])
        
        if 'user_id' in order and order['user_id'] != 'guest':
            try:
                user = users_collection.find_one({"_id": ObjectId(order['user_id'])})
                if user:
                    order['user_name'] = f"{user['name']} {user['surname']}"
                    order['user_email'] = user['email']
            except:
                pass
        
        orders.append(order)
    
    return jsonify({
        'orders': orders,
        'totalPages': total_pages,
        'currentPage': page,
        'totalRecords': total_records
    })

@admin_bp.route('/api/admin/orders/<order_id>')
@login_required
@admin_required
def get_order(order_id):
    try:
        order = None
        if order_id.startswith('GUEST-'):
            order = orders_collection.find_one({"guest_order_id": order_id})
        else:
            order = orders_collection.find_one({"_id": ObjectId(order_id)})
            
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if '_id' in order:
            order['_id'] = str(order['_id'])
        
        if 'user_id' in order and order['user_id'] != 'guest':
            try:
                user = users_collection.find_one({"_id": ObjectId(order['user_id'])})
                if user:
                    order['user_name'] = f"{user['name']} {user['surname']}"
                    order['user_email'] = user['email']
            except:
                pass
        
        return jsonify(order)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/orders/<order_id>/status', methods=['PUT'])
@login_required
@admin_required
def update_order_status(order_id):
    try:
        data = request.json
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        if order_id.startswith('GUEST-'):
            result = orders_collection.update_one(
                {"guest_order_id": order_id},
                {"$set": {"status": new_status}}
            )
        else:
            result = orders_collection.update_one(
                {"_id": ObjectId(order_id)},
                {"$set": {"status": new_status}}
            )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'message': 'Order status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/orders/<order_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_order(order_id):
    try:
        
        if order_id.startswith('GUEST-'):
            result = orders_collection.delete_one({"guest_order_id": order_id})
        else:
            result = orders_collection.delete_one({"_id": ObjectId(order_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/profile')
@login_required
@admin_required
def get_profile():
    try:
        profile = {
            'username': current_user.username,
            'email': current_user.email,
            'name': current_user.name,
            'surname': current_user.surname,
            'role': current_user.role
        }
        
        return jsonify(profile)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/profile', methods=['PUT'])
@login_required
@admin_required
def update_profile():
    try:
        data = request.json
        
        if data['username'] != current_user.username:
            username_check = users_collection.find_one({"username": data['username'], "_id": {"$ne": current_user._id}})
            if username_check:
                return jsonify({'error': 'Username already exists'}), 400
        
        if data['email'] != current_user.email:
            email_check = users_collection.find_one({"email": data['email'], "_id": {"$ne": current_user._id}})
            if email_check:
                return jsonify({'error': 'Email already exists'}), 400
        
        result = users_collection.update_one(
            {"_id": current_user._id},
            {"$set": {
                "username": data['username'],
                "email": data['email'],
                "name": data['name'],
                "surname": data['surname']
            }}
        )
        
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/change-password', methods=['POST'])
@login_required
@admin_required
def change_password():
    try:
        data = request.json
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new passwords are required'}), 400
        
        if not current_user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        current_user.set_password(new_password)
        
        result = users_collection.update_one(
            {"_id": current_user._id},
            {"$set": {"password_hash": current_user.password_hash}}
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500