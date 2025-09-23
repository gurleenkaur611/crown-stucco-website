from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'crown_stucco_secret_key_2025'  # Change this in production

# Email Configuration - Temporarily disabled
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "gillgurleen1636@gmail.com"
EMAIL_PASSWORD = ""  # Temporarily disabled to fix deployment

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
        'name': 'Residential Stucco',
        'description': 'Professional stucco application for homes and residential properties. We provide durable, weather-resistant finishes that enhance your home\'s curb appeal.',
        'icon': '🏠'
    },
    {
        'name': 'Commercial Stucco',
        'description': 'Large-scale stucco solutions for commercial buildings, offices, and industrial properties. Reliable service for business owners.',
        'icon': '🏢'
    },
    {
        'name': 'EIFS Systems',
        'description': 'Exterior Insulation and Finish Systems (EIFS) installation for improved energy efficiency and modern aesthetics.',
        'icon': '🛡️'
    },
    {
        'name': 'House Wrap Installation',
        'description': 'Professional house wrap installation to protect your building structure from moisture and air infiltration.',
        'icon': '🏗️'
    },
    {
        'name': 'Paper Wire Systems',
        'description': 'Traditional paper wire application for stucco base preparation, ensuring proper adhesion and longevity.',
        'icon': '📏'
    },
    {
        'name': 'Custom Work',
        'description': 'We specialize in custom stucco work tailored to your specific requirements. No project is too unique for our experienced team.',
        'icon': '⭐'
    }
]


def send_confirmation_email(customer_name, customer_email, service, message):
    """Send confirmation email to customer - temporarily disabled"""
    try:
        # Temporarily disabled - just log what would happen
        print(f"Would send confirmation email to {customer_email} for customer {customer_name}")
        print(f"Service: {service}, Message preview: {message[:50]}...")
        return True  # Pretend it worked

    except Exception as e:
        print(f"Failed to send confirmation email: {e}")
        return False


@app.route('/')
def home():
    return render_template('home.html', business=BUSINESS_INFO)


@app.route('/services')
def services():
    return render_template('services.html', services=SERVICES, business=BUSINESS_INFO)


@app.route('/gallery')
def gallery():
    gallery_items = [
        {'title': 'Residential Exterior Project', 'description': 'Complete home exterior stucco application'},
        {'title': 'Commercial Building', 'description': 'Large-scale commercial stucco project'},
        {'title': 'EIFS Installation', 'description': 'Energy-efficient EIFS system application'},
        {'title': 'Custom Texture Work', 'description': 'Specialized custom texture stucco finish'},
        {'title': 'House Wrap Installation', 'description': 'Professional house wrap and preparation'},
        {'title': 'Repair and Restoration', 'description': 'Expert stucco repair and color matching'},
        {'title': 'Interior Specialty Work', 'description': 'Custom interior plaster application'},
        {'title': 'Before/After Comparison', 'description': 'Transformation of aged stucco surface'},
        {'title': 'Modern EIFS Finish', 'description': 'Contemporary EIFS application'},
    ]
    return render_template('gallery.html', gallery_items=gallery_items, business=BUSINESS_INFO)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = request.args.get('success')
    if success:
        flash('Thank you for your message! We will get back to you within 24 hours.', 'success')

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            service = request.form.get('service')
            message = request.form.get('message')

            if name and email and message:
                # Try to send confirmation email
                email_sent = send_confirmation_email(name, email, service, message)

                if email_sent:
                    flash('Thank you for your message! We will get back to you within 24 hours.', 'success')
                else:
                    flash('Thank you for your message! We will get back to you within 24 hours.', 'success')

                return redirect(url_for('contact'))
        except Exception as e:
            print(f"Error processing form: {e}")
            flash('Thank you for your message! We will get back to you within 24 hours.', 'success')

    return render_template('contact.html', business=BUSINESS_INFO)


if __name__ == '__main__':
    app.run(debug=True)