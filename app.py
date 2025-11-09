from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'Paramjot2025!'

# Admin password (CHANGE THIS!)
ADMIN_PASSWORD = 'Japjot2025!'  # ← CHANGE THIS! Line 17

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Business Information
BUSINESS_INFO = {
    'name': 'Crown Stucco Ltd',
    'address': '46 Tivoli Lane',
    'city': 'West St. Paul, MB',
    'phone': '204-898-2832',
    'phone_toor': '204-962-8082',
    'email': 'crownstuccoltd@gmail.com',
    'hours': {
        'weekdays': '7:30 AM - 5:00 PM',
        'saturday': '7:30 AM - 5:00 PM',
        'sunday': 'Closed'
    },
    'service_area': 'Anywhere in Manitoba',
    'established': '2021',
    'specialties': [
        'On-time job completion',
        'Good management',
        'Experienced crew',
        'High-quality materials'
    ]
}

SERVICES = [
    {
        'id': 0,
        'name': 'Residential Stucco',
        'description': 'Professional stucco application for homes and residential properties. We provide durable, weather-resistant finishes that enhance your home\'s curb appeal.',
        'icon': '🏠'
    },
    {
        'id': 1,
        'name': 'Commercial Stucco',
        'description': 'Large-scale stucco solutions for commercial buildings, offices, and industrial properties. Reliable service for business owners.',
        'icon': '🏢'
    },
    {
        'id': 2,
        'name': 'EIFS Systems',
        'description': 'Exterior Insulation and Finish Systems (EIFS) installation for improved energy efficiency and modern aesthetics.',
        'icon': '🛡️'
    },
    {
        'id': 3,
        'name': 'House Wrap Installation',
        'description': 'Professional house wrap installation to protect your building structure from moisture and air infiltration.',
        'icon': '🏗️'
    },
    {
        'id': 4,
        'name': 'Paper Wire Systems',
        'description': 'Traditional paper wire application for stucco base preparation, ensuring proper adhesion and longevity.',
        'icon': '📋'
    },
    {
        'id': 5,
        'name': 'Custom Work',
        'description': 'We specialize in custom stucco work tailored to your specific requirements. No project is too unique for our experienced team.',
        'icon': '⭐'
    }
]

# Gallery data file
GALLERY_DATA_FILE = 'gallery_data.json'


def load_gallery_items():
    """Load gallery items from JSON file"""
    if os.path.exists(GALLERY_DATA_FILE):
        with open(GALLERY_DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_gallery_items(items):
    """Save gallery items to JSON file"""
    with open(GALLERY_DATA_FILE, 'w') as f:
        json.dump(items, f, indent=2)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================
# PUBLIC ROUTES
# ============================================

@app.route('/')
def home():
    return render_template('home.html', business=BUSINESS_INFO)


@app.route('/services')
def services():
    return render_template('services.html', services=SERVICES, business=BUSINESS_INFO)


@app.route('/services/<int:service_id>')
def service_detail(service_id):
    """Display individual service detail page"""
    # Check if service_id is valid
    if 0 <= service_id < len(SERVICES):
        service = SERVICES[service_id]
        return render_template('service_detail.html', service=service, business=BUSINESS_INFO)
    else:
        # If invalid ID, redirect to services page
        flash('Service not found', 'error')
        return redirect(url_for('services'))


@app.route('/gallery')
def gallery():
    # Load real gallery items from JSON file
    gallery_items = load_gallery_items()

    # If no items, show placeholders
    if not gallery_items:
        gallery_items = [
            {'title': 'Residential Exterior Project', 'description': 'Complete home exterior stucco application',
             'category': 'residential'},
            {'title': 'Commercial Building', 'description': 'Large-scale commercial stucco project',
             'category': 'commercial'},
            {'title': 'EIFS Installation', 'description': 'Energy-efficient EIFS system application',
             'category': 'eifs'},
            {'title': 'Custom Texture Work', 'description': 'Specialized custom texture stucco finish',
             'category': 'custom'},
            {'title': 'House Wrap Installation', 'description': 'Professional house wrap and preparation',
             'category': 'residential'},
            {'title': 'Repair and Restoration', 'description': 'Expert stucco repair and color matching',
             'category': 'repair'},
        ]

    return render_template('gallery.html', gallery_items=gallery_items, business=BUSINESS_INFO)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = request.args.get('success')
    if success:
        flash('Thank you for your message! We will get back to you within 24 hours.', 'success')

    return render_template('contact.html', business=BUSINESS_INFO)


# ============================================
# ADMIN ROUTES
# ============================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Simple admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Welcome! You can now upload photos.', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Incorrect password. Please try again.', 'error')

    return render_template('admin_login.html', business=BUSINESS_INFO)


@app.route('/admin')
def admin_panel():
    """Admin panel for photo management"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    gallery_items = load_gallery_items()
    return render_template('admin.html', business=BUSINESS_INFO, gallery_items=gallery_items)


@app.route('/admin/upload', methods=['POST'])
def admin_upload():
    """Handle photo upload"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Check if file was uploaded
    if 'photo' not in request.files:
        flash('No photo selected', 'error')
        return redirect(url_for('admin_panel'))

    file = request.files['photo']

    # Check if file is empty
    if file.filename == '':
        flash('No photo selected', 'error')
        return redirect(url_for('admin_panel'))

    # Check if file is allowed
    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)

        # Add timestamp to avoid overwriting
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"

        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get form data
        title = request.form.get('title', 'Untitled Project')
        description = request.form.get('description', '')
        category = request.form.get('category', 'residential')

        # Load current gallery items
        gallery_items = load_gallery_items()

        # Add new item
        new_item = {
            'id': len(gallery_items) + 1,
            'title': title,
            'description': description,
            'category': category,
            'filename': filename,
            'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        gallery_items.append(new_item)

        # Save updated gallery
        save_gallery_items(gallery_items)

        flash('Photo uploaded successfully!', 'success')
        return redirect(url_for('admin_panel'))

    flash('Invalid file type. Please upload an image (JPG, PNG, GIF, WEBP)', 'error')
    return redirect(url_for('admin_panel'))


@app.route('/admin/delete/<int:photo_id>', methods=['POST'])
def admin_delete(photo_id):
    """Delete a photo"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    gallery_items = load_gallery_items()

    # Find and remove the item
    item_to_delete = None
    for item in gallery_items:
        if item.get('id') == photo_id:
            item_to_delete = item
            break

    if item_to_delete:
        # Delete file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], item_to_delete['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)

        # Remove from list
        gallery_items.remove(item_to_delete)
        save_gallery_items(gallery_items)

        flash('Photo deleted successfully', 'success')
    else:
        flash('Photo not found', 'error')

    return redirect(url_for('admin_panel'))


@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))


# Serve uploaded files
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)