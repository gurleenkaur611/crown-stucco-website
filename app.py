from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'Parmjot2025!'

# ============================================
# SESSION CONFIG - stays logged in 7 days
# ============================================
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

# ============================================
# MULTI-USER ADMIN ACCOUNTS
# ============================================
ADMIN_USERS = {
    'Harminder Gill': {
        'password': 'Japjotparamjot!',
        'display_name': 'Harminder Gill',
        'role': 'Owner'
    },
    'Harjinder Toor': {
        'password': 'Namneetnavraj!',
        'display_name': 'Harjinder Toor',
        'role': 'Owner'
    },
    'Gurleen Gill': {
        'password': 'Gurleengill!',
        'display_name': 'Gurleen Gill',
        'role': 'Admin'
    }
}

# ============================================
# EMAIL CONFIG - Gmail SMTP
# Change these to your Gmail credentials
# ============================================
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'crownstuccoltd@gmail.com',
    'sender_password': os.environ.get('GMAIL_APP_PASSWORD', ''),  # Set in Render environment
    'recipient_email': 'crownstuccoltd@gmail.com'
}

# ============================================
# FILE UPLOAD CONFIG
# ============================================
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ============================================
# BUSINESS INFO
# ============================================
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

# ============================================
# SERVICES DATA
# ============================================
SERVICES = [
    {
        'id': 0,
        'name': 'Residential Stucco',
        'description': 'Professional stucco application for homes and residential properties. We provide durable, weather-resistant finishes that enhance your home\'s curb appeal.',
        'icon': 'house',
        'details': {
            'overview': 'Transform your home with our expert residential stucco services. We provide durable, weather-resistant finishes that enhance your home\'s curb appeal and protect against Manitoba\'s harsh weather conditions.',
            'features': [
                'Durable, weather-resistant finishes',
                'Energy-efficient exterior solutions',
                'Wide range of colors and textures',
                'Improved home value and curb appeal',
                'Protection against harsh weather',
                'Long-lasting quality materials'
            ],
            'process': [
                'Initial consultation and site assessment',
                'Detailed 3D drawings and project plan',
                'Surface preparation and base installation',
                'Professional stucco application',
                'Finishing touches and texture work',
                'Final inspection and cleanup'
            ]
        }
    },
    {
        'id': 1,
        'name': 'Commercial Stucco',
        'description': 'Large-scale stucco solutions for commercial buildings, offices, and industrial properties. Reliable service for business owners.',
        'icon': 'building',
        'details': {
            'overview': 'Professional commercial stucco services for businesses throughout Manitoba. We deliver large-scale projects on time with minimal disruption to your operations.',
            'features': [
                'Large-scale project expertise',
                'Minimal business disruption',
                'Durable commercial-grade materials',
                'Professional project management',
                'Compliance with building codes',
                'Warranty-backed workmanship'
            ],
            'process': [
                'Commercial property assessment',
                'Detailed project planning and scheduling',
                'Coordination with building management',
                'Professional installation by experienced crew',
                'Quality control and inspection',
                'Final walkthrough and documentation'
            ]
        }
    },
    {
        'id': 2,
        'name': 'EIFS Systems',
        'description': 'Exterior Insulation and Finish Systems (EIFS) installation for improved energy efficiency and modern aesthetics.',
        'icon': 'shield',
        'details': {
            'overview': 'Energy-efficient EIFS (Exterior Insulation and Finish Systems) installation that provides superior insulation, moisture management, and modern aesthetics for your property.',
            'features': [
                'Superior energy efficiency',
                'Excellent moisture management',
                'Lightweight and versatile',
                'Wide range of design options',
                'Crack-resistant technology',
                'Reduced heating and cooling costs'
            ],
            'process': [
                'Energy assessment and consultation',
                'Custom EIFS system design',
                'Surface preparation and base installation',
                'Insulation board application',
                'Base coat and reinforcement',
                'Finish coat application and texturing'
            ]
        }
    },
    {
        'id': 3,
        'name': 'House Wrap Installation',
        'description': 'Professional house wrap installation to protect your building structure from moisture and air infiltration.',
        'icon': 'tools',
        'details': {
            'overview': 'Professional house wrap installation provides essential protection against moisture and air infiltration, creating a strong foundation for your stucco application.',
            'features': [
                'Superior moisture protection',
                'Air infiltration prevention',
                'Breathable membrane technology',
                'Mold and mildew resistance',
                'Energy efficiency improvement',
                'Building code compliance'
            ],
            'process': [
                'Building assessment and planning',
                'Surface preparation and cleaning',
                'House wrap installation with proper overlap',
                'Sealing all joints and penetrations',
                'Quality inspection',
                'Ready for stucco application'
            ]
        }
    },
    {
        'id': 4,
        'name': 'Paper Wire Systems',
        'description': 'Traditional paper wire application for stucco base preparation, ensuring proper adhesion and longevity.',
        'icon': 'ruler',
        'details': {
            'overview': 'Traditional paper wire system installation provides the essential base for quality stucco application, ensuring proper adhesion and long-lasting results.',
            'features': [
                'Traditional proven method',
                'Excellent stucco adhesion',
                'Structural reinforcement',
                'Crack prevention',
                'Weather-resistant backing',
                'Long-lasting durability'
            ],
            'process': [
                'Wall surface preparation',
                'Moisture barrier installation',
                'Wire lath attachment and securing',
                'Corner and edge reinforcement',
                'Quality inspection',
                'Ready for stucco application'
            ]
        }
    },
    {
        'id': 5,
        'name': 'Custom Work',
        'description': 'We specialize in custom stucco work tailored to your specific requirements. No project is too unique for our experienced team.',
        'icon': 'star',
        'details': {
            'overview': 'Bring your unique vision to life with our custom stucco services. From decorative features to specialty textures, our experienced team can handle any custom requirement.',
            'features': [
                'Unlimited design possibilities',
                'Custom textures and finishes',
                'Decorative elements and features',
                'Color matching expertise',
                'Architectural detail work',
                'One-of-a-kind solutions'
            ],
            'process': [
                'Design consultation and vision planning',
                'Custom 3D mockups and renderings',
                'Material selection and approval',
                'Skilled craftsman application',
                'Detailed finishing work',
                'Final inspection and client approval'
            ]
        }
    }
]

# ============================================
# GALLERY HELPERS
# ============================================
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
# ADMIN HELPERS
# ============================================
def is_admin_logged_in():
    """Check if any admin user is logged in"""
    return session.get('admin_logged_in') and session.get('admin_username')


def get_current_admin():
    """Get the currently logged in admin user info"""
    username = session.get('admin_username')
    if username and username in ADMIN_USERS:
        user = ADMIN_USERS[username].copy()
        user['username'] = username
        return user
    return None


# ============================================
# EMAIL HELPER - Custom contact form
# ============================================
def send_contact_email(name, email, phone, service, message):
    """
    Send contact form email via Gmail SMTP.

    SETUP REQUIRED:
    1. Go to your Gmail account (crownstuccoltd@gmail.com)
    2. Enable 2-Factor Authentication
    3. Go to Google Account > Security > App Passwords
    4. Create an App Password for "Mail"
    5. Copy the 16-character password
    6. In Render.com dashboard, go to your service > Environment
    7. Add variable: GMAIL_APP_PASSWORD = (your 16-char app password)
    """
    sender_password = EMAIL_CONFIG['sender_password']

    if not sender_password:
        # Log the inquiry instead of failing silently
        print(f"[CONTACT FORM] New inquiry from {name} ({email}) - Gmail not configured yet")
        return True  # Return True so user still sees success message

    try:
        # Build the email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"New Stucco Inquiry from {name}"
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['recipient_email']
        msg['Reply-To'] = email  # So you can reply directly to the customer

        # Format service name nicely
        service_display = service.replace('-', ' ').title() if service else 'Not specified'
        phone_display = phone if phone else 'Not provided'
        submitted_at = datetime.now().strftime('%B %d, %Y at %I:%M %p')

        # Plain text version
        text_body = f"""
New inquiry from your Crown Stucco Ltd website!

--- CUSTOMER DETAILS ---
Name:    {name}
Email:   {email}
Phone:   {phone_display}
Service: {service_display}

--- MESSAGE ---
{message}

--- SUBMISSION INFO ---
Submitted: {submitted_at}
Website:   crownstucco.ltd

---
Reply directly to this email to respond to {name}.
        """.strip()

        # HTML version (nice formatting)
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #2d5a3d, #4a7c59); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 1.5rem; }}
        .header p {{ margin: 5px 0 0; color: #90ee90; font-size: 0.9rem; }}
        .body {{ padding: 30px; }}
        .field {{ background: #f8f9fa; border-left: 4px solid #2d5a3d; padding: 12px 15px; margin-bottom: 15px; border-radius: 0 5px 5px 0; }}
        .field label {{ font-size: 0.75rem; text-transform: uppercase; color: #666; font-weight: bold; display: block; margin-bottom: 3px; }}
        .field span {{ font-size: 1rem; color: #000; font-weight: 500; }}
        .message-box {{ background: #f0f7f0; border: 2px solid #c8e6c9; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .message-box label {{ font-weight: bold; color: #2d5a3d; display: block; margin-bottom: 8px; }}
        .message-box p {{ margin: 0; color: #000; line-height: 1.6; white-space: pre-wrap; }}
        .footer {{ background: #f0f7f0; padding: 20px; text-align: center; border-top: 2px solid #c8e6c9; }}
        .footer p {{ margin: 0; color: #666; font-size: 0.85rem; }}
        .reply-btn {{ display: inline-block; background: #2d5a3d; color: white; padding: 12px 25px; border-radius: 5px; text-decoration: none; font-weight: bold; margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📬 New Website Inquiry</h1>
            <p>Crown Stucco Ltd — crownstucco.ltd</p>
        </div>
        <div class="body">
            <p style="color:#000; margin-top:0;">You have a new inquiry from your website. Here are the details:</p>

            <div class="field">
                <label>Full Name</label>
                <span>{name}</span>
            </div>
            <div class="field">
                <label>Email Address</label>
                <span><a href="mailto:{email}" style="color:#2d5a3d;">{email}</a></span>
            </div>
            <div class="field">
                <label>Phone Number</label>
                <span>{phone_display}</span>
            </div>
            <div class="field">
                <label>Service Requested</label>
                <span>{service_display}</span>
            </div>

            <div class="message-box">
                <label>📝 Project Details</label>
                <p>{message}</p>
            </div>

            <div style="text-align:center;">
                <a href="mailto:{email}?subject=Re: Your Crown Stucco Inquiry" class="reply-btn">
                    ✉️ Reply to {name}
                </a>
            </div>
        </div>
        <div class="footer">
            <p>Submitted: {submitted_at}</p>
            <p style="margin-top:5px;">This email was sent automatically from crownstucco.ltd</p>
        </div>
    </div>
</body>
</html>
        """

        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))

        # Send via Gmail SMTP
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], sender_password)
            server.sendmail(
                EMAIL_CONFIG['sender_email'],
                EMAIL_CONFIG['recipient_email'],
                msg.as_string()
            )

        return True

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")
        return False


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
    if 0 <= service_id < len(SERVICES):
        service = SERVICES[service_id]
        return render_template('service_detail.html', service=service, business=BUSINESS_INFO)
    else:
        flash('Service not found', 'error')
        return redirect(url_for('services'))


@app.route('/gallery')
def gallery():
    gallery_items = load_gallery_items()

    if not gallery_items:
        gallery_items = [
            {'title': 'Residential Exterior Project', 'description': 'Complete home exterior stucco application', 'category': 'residential'},
            {'title': 'Commercial Building', 'description': 'Large-scale commercial stucco project', 'category': 'commercial'},
            {'title': 'EIFS Installation', 'description': 'Energy-efficient EIFS system application', 'category': 'eifs'},
            {'title': 'Custom Texture Work', 'description': 'Specialized custom texture stucco finish', 'category': 'custom'},
            {'title': 'House Wrap Installation', 'description': 'Professional house wrap and preparation', 'category': 'residential'},
            {'title': 'Repair and Restoration', 'description': 'Expert stucco repair and color matching', 'category': 'repair'},
        ]

    return render_template('gallery.html', gallery_items=gallery_items, business=BUSINESS_INFO)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form - handles both GET (show form) and POST (send email)"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        service = request.form.get('service', '').strip()
        message = request.form.get('message', '').strip()

        # Basic validation
        if not name or not email or not message:
            flash('Please fill in all required fields (Name, Email, Message).', 'error')
            return render_template('contact.html', business=BUSINESS_INFO)

        # Send the email
        email_sent = send_contact_email(name, email, phone, service, message)

        if email_sent:
            flash(f'Thank you {name}! Your message has been sent. We will get back to you within 24 hours.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Something went wrong sending your message. Please call us directly at 204-898-2832.', 'error')
            return render_template('contact.html', business=BUSINESS_INFO)

    # GET request - just show the form
    return render_template('contact.html', business=BUSINESS_INFO)


# ============================================
# ADMIN ROUTES - Multi-user
# ============================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Multi-user admin login page"""
    # If already logged in, go to panel
    if is_admin_logged_in():
        return redirect(url_for('admin_panel'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Check username exists
        if username not in ADMIN_USERS:
            flash('Invalid username or password.', 'error')
            return render_template('admin_login.html', business=BUSINESS_INFO)

        # Check password
        if ADMIN_USERS[username]['password'] != password:
            flash('Invalid username or password.', 'error')
            return render_template('admin_login.html', business=BUSINESS_INFO)

        # Success - set session
        session.permanent = True
        session['admin_logged_in'] = True
        session['admin_username'] = username

        display_name = ADMIN_USERS[username]['display_name']
        flash(f'Welcome, {display_name}! You are now logged in.', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('admin_login.html', business=BUSINESS_INFO)


@app.route('/admin')
def admin_panel():
    """Admin panel for photo management"""
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))

    current_admin = get_current_admin()
    gallery_items = load_gallery_items()
    return render_template('admin.html', business=BUSINESS_INFO, gallery_items=gallery_items, current_admin=current_admin)


@app.route('/admin/upload', methods=['POST'])
def admin_upload():
    """Handle photo upload"""
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))

    if 'photo' not in request.files:
        flash('No photo selected', 'error')
        return redirect(url_for('admin_panel'))

    file = request.files['photo']

    if file.filename == '':
        flash('No photo selected', 'error')
        return redirect(url_for('admin_panel'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        title = request.form.get('title', 'Untitled Project')
        description = request.form.get('description', '')
        category = request.form.get('category', 'residential')

        gallery_items = load_gallery_items()

        # Track who uploaded the photo
        current_admin = get_current_admin()
        uploaded_by = current_admin['display_name'] if current_admin else 'Unknown'

        new_item = {
            'id': len(gallery_items) + 1,
            'title': title,
            'description': description,
            'category': category,
            'filename': filename,
            'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'uploaded_by': uploaded_by
        }

        gallery_items.append(new_item)
        save_gallery_items(gallery_items)

        flash(f'Photo "{title}" uploaded successfully!', 'success')
        return redirect(url_for('admin_panel'))

    flash('Invalid file type. Please upload an image (JPG, PNG, GIF, WEBP)', 'error')
    return redirect(url_for('admin_panel'))


@app.route('/admin/delete/<int:photo_id>', methods=['POST'])
def admin_delete(photo_id):
    """Delete a photo"""
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))

    gallery_items = load_gallery_items()

    item_to_delete = None
    for item in gallery_items:
        if item.get('id') == photo_id:
            item_to_delete = item
            break

    if item_to_delete:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], item_to_delete.get('filename', ''))
        if os.path.exists(filepath):
            os.remove(filepath)

        gallery_items.remove(item_to_delete)
        save_gallery_items(gallery_items)

        flash(f'Photo deleted successfully.', 'success')
    else:
        flash('Photo not found.', 'error')

    return redirect(url_for('admin_panel'))


@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    current_admin = get_current_admin()
    name = current_admin['display_name'] if current_admin else 'Admin'

    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)

    flash(f'Goodbye, {name}! You have been logged out.', 'success')
    return redirect(url_for('home'))


# Serve uploaded files
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)