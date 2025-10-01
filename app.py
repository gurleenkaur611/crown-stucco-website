from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'crown_stucco_secret_key_2025'

# Force production mode
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
        'id': 'residential-stucco',
        'name': 'Residential Stucco',
        'description': 'Professional stucco application for homes and residential properties.',
        'icon': 'house',
        'details': {
            'overview': 'Transform your home with our expert residential stucco services. We provide durable, weather-resistant finishes that enhance your home\'s curb appeal and protect against Manitoba\'s harsh weather conditions.',
            'features': [
                'Weather-resistant exterior finishes',
                'Energy-efficient insulation properties',
                'Custom texture and color options',
                'Long-lasting durability',
                'Professional surface preparation',
                'Quality material application'
            ],
            'process': [
                'Initial consultation and site assessment',
                'Surface preparation and cleaning',
                'Base coat application',
                'Mesh installation for reinforcement',
                'Finish coat application',
                'Final inspection and cleanup'
            ]
        }
    },
    {
        'id': 'commercial-stucco',
        'name': 'Commercial Stucco',
        'description': 'Large-scale stucco solutions for commercial buildings and offices.',
        'icon': 'building',
        'details': {
            'overview': 'Professional commercial stucco services for offices, retail spaces, and industrial facilities. We handle large-scale projects with efficient project management and quality results.',
            'features': [
                'Large-scale project management',
                'Commercial-grade materials',
                'Fire-resistant applications',
                'Weather-resistant systems',
                'Professional scheduling',
                'Minimal business disruption'
            ],
            'process': [
                'Project planning and timeline development',
                'Site preparation and safety setup',
                'Systematic application by sections',
                'Quality control inspections',
                'Final walkthrough and documentation',
                'Warranty and maintenance guidance'
            ]
        }
    },
    {
        'id': 'eifs-systems',
        'name': 'EIFS Systems',
        'description': 'Exterior Insulation and Finish Systems installation.',
        'icon': 'shield',
        'details': {
            'overview': 'EIFS (Exterior Insulation and Finish Systems) provide superior energy efficiency and modern aesthetics. These systems offer excellent insulation properties while maintaining design flexibility.',
            'features': [
                'Superior energy efficiency',
                'Moisture barrier protection',
                'Design flexibility',
                'Lightweight construction',
                'Crack-resistant finish',
                'Modern aesthetic appeal'
            ],
            'process': [
                'Substrate preparation',
                'Insulation board installation',
                'Base coat application',
                'Mesh embedding',
                'Finish coat application',
                'Final detailing and sealing'
            ]
        }
    },
    {
        'id': 'house-wrap',
        'name': 'House Wrap Installation',
        'description': 'Professional house wrap installation services.',
        'icon': 'tools',
        'details': {
            'overview': 'House wrap installation protects your building structure from moisture and air infiltration while allowing vapor to escape. Essential preparation for stucco application.',
            'features': [
                'Moisture barrier protection',
                'Air infiltration prevention',
                'Vapor permeable design',
                'Weather-resistant materials',
                'Professional installation',
                'Building code compliance'
            ],
            'process': [
                'Wall surface inspection',
                'Proper overlap installation',
                'Seam sealing',
                'Window and door integration',
                'Quality inspection',
                'Documentation for warranty'
            ]
        }
    },
    {
        'id': 'paper-wire',
        'name': 'Paper Wire Systems',
        'description': 'Traditional paper wire application for stucco preparation.',
        'icon': 'ruler',
        'details': {
            'overview': 'Traditional paper wire systems provide the foundation for quality stucco application. This time-tested method ensures proper adhesion and long-lasting results.',
            'features': [
                'Traditional proven method',
                'Excellent adhesion base',
                'Long-lasting foundation',
                'Weather-resistant backing',
                'Professional installation',
                'Code-compliant application'
            ],
            'process': [
                'Surface preparation',
                'Paper backing installation',
                'Wire mesh attachment',
                'Corner and edge detailing',
                'Inspection and approval',
                'Ready for stucco application'
            ]
        }
    },
    {
        'id': 'custom-work',
        'name': 'Custom Work',
        'description': 'Custom stucco work tailored to your requirements.',
        'icon': 'star',
        'details': {
            'overview': 'We specialize in custom stucco work tailored to your specific requirements. No project is too unique for our experienced team.',
            'features': [
                'Unique design solutions',
                'Custom texture creation',
                'Architectural details',
                'Color matching services',
                'Decorative elements',
                'Specialty applications'
            ],
            'process': [
                'Design consultation',
                'Custom solution development',
                'Sample creation and approval',
                'Specialized installation',
                'Quality assurance',
                'Final artistic touches'
            ]
        }
    }
]

@app.route('/')
def home():
    return render_template('home.html', business=BUSINESS_INFO)

@app.route('/services')
def services():
    return render_template('services.html', services=SERVICES, business=BUSINESS_INFO)

@app.route('/service/<service_id>')
def service_detail(service_id):
    service = next((s for s in SERVICES if s['id'] == service_id), None)
    if not service:
        return redirect(url_for('services'))
    return render_template('service_detail.html', service=service, business=BUSINESS_INFO)

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

    return render_template('contact.html', business=BUSINESS_INFO)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)