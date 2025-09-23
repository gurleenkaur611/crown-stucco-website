from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'crown_stucco_secret_key_2025'

# Force production mode - disable debug
app.config['DEBUG'] = False
app.config['TESTING'] = False

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
        'description': 'Professional stucco application for homes and residential properties.',
        'icon': 'house'
    },
    {
        'name': 'Commercial Stucco',
        'description': 'Large-scale stucco solutions for commercial buildings and offices.',
        'icon': 'building'
    },
    {
        'name': 'EIFS Systems',
        'description': 'Exterior Insulation and Finish Systems installation.',
        'icon': 'shield'
    },
    {
        'name': 'House Wrap Installation',
        'description': 'Professional house wrap installation services.',
        'icon': 'tools'
    },
    {
        'name': 'Paper Wire Systems',
        'description': 'Traditional paper wire application for stucco preparation.',
        'icon': 'ruler'
    },
    {
        'name': 'Custom Work',
        'description': 'Custom stucco work tailored to your requirements.',
        'icon': 'star'
    }
]

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
        {'title': 'Repair and Restoration', 'description': 'Expert stucco repair and color matching'}
    ]
    return render_template('gallery.html', gallery_items=gallery_items, business=BUSINESS_INFO)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = request.args.get('success')
    if success:
        flash('Thank you for your message! We will get back to you within 24 hours.', 'success')
    return render_template('contact.html', business=BUSINESS_INFO)

# Remove the debug mode completely for production
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)