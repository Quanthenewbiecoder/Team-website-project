import os

# Directory where your template files are located
template_dir = './app/templates'

# List of required template files
required_templates = [
    'login.html', 'register.html', 'forgot_password.html', 'Password_change.html',
    'index.html', 'about_us.html', 'Contact.html', 'Product.html', 'product_detail.html',
    'care_instructions.html', 'bundles.html', 'bundle_detail.html', 'Basket.html',
    'wishlist.html', 'checkout.html', 'apply_discount.html', 'order_summary.html',
    'order_confirmation.html', 'track_order.html', 'History.html', 'product_reviews.html',
    'add_review.html', 'feedback.html', 'profile.html', 'edit_profile.html',
    'admin_dashboard.html', 'suppliers.html', 'manage_users.html', 'manage_orders.html',
    'add_product.html', 'inventory_dashboard.html', 'manage_discounts.html',
    'manage_tags.html', 'manage_bundles.html', 'reports.html', 'Payment.html',
    'customize_product.html'
]

# Template structure to write into each new file
template_content = """{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}

{% endblock %}
"""

# Loop through each required template
for template_name in required_templates:
    # Full path of the template file
    template_path = os.path.join(template_dir, template_name)
    
    # Check if the template file already exists
    if not os.path.exists(template_path):
        # Extract the title from the file name (e.g., "Basket" for "Basket.html")
        title = os.path.splitext(template_name)[0]
        
        # Write the template content to the new file
        with open(template_path, 'w') as f:
            # Fill in the title in the content and write to the file
            f.write(template_content.replace("{{ title }}", title.capitalize()))
        
        print(f"Created: {template_name}")
    else:
        print(f"Already exists: {template_name}")
