from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Configure static and template folders
app.static_folder = 'static'
app.template_folder = 'templates'

# Store form submissions (in production, use a database)
SUBMISSIONS_FILE = 'submissions.json'

def save_submission(data):
    """Save form submission to JSON file"""
    try:
        # Read existing submissions
        if os.path.exists(SUBMISSIONS_FILE):
            with open(SUBMISSIONS_FILE, 'r') as f:
                submissions = json.load(f)
        else:
            submissions = []
        
        # Add new submission
        submissions.append(data)
        
        # Save back to file
        with open(SUBMISSIONS_FILE, 'w') as f:
            json.dump(submissions, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving submission: {e}")
        return False

# ============= MAIN ROUTES =============

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/home')
def home():
    """Alternative home route"""
    return redirect(url_for('index'))

# ============= BLOG ROUTES =============

@app.route('/all-blogs')
def all_blogs():
    """All blogs listing page"""
    return render_template('all_blogs.html')

@app.route('/om')
def blog_om():
    """Om's blog post - AWS"""
    return render_template('blogs/om.html')

@app.route('/gurbani')
def blog_gurbani():
    """Gurbani's blog post - Cloud Computing"""
    return render_template('blogs/gurbani.html')

@app.route('/sharv')
def blog_sharv():
    """Sharv's blog post - AI in Cybersecurity"""
    return render_template('blogs/sharv.html')

@app.route('/siddhi')
def blog_siddhi():
    """Siddhi's blog post - AI in Digital Marketing"""
    return render_template('blogs/siddhi.html')

@app.route('/ajinka')
def blog_ajinka():
    """Ajinka's blog post - Data-Driven Decision Making"""
    return render_template('blogs/ajinka.html')

@app.route('/anurag')
def blog_anurag():
    """Anurag's blog post - Website & App Design"""
    return render_template('blogs/anurag.html')

@app.route('/dhanashri')
def blog_dhanashri():
    """Dhanashri's blog post - Data Analysis"""
    return render_template('blogs/dhanashri.html')

@app.route('/nuper')
def blog_nuper():
    """Nuper's blog post - Digital Marketing"""
    return render_template('blogs/nuper.html')

@app.route('/om_gws')
def blog_om_gws():
    """Om's blog post - Visual Storytelling"""
    return render_template('blogs/om_gws.html')

# ============= OTHER PAGES =============

@app.route('/join_us')
def join_us():
    """Join Us / Careers page"""
    return render_template('join_us.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/services')
def services():
    """Services page"""
    return render_template('services.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/portfolio')
def portfolio():
    """Portfolio page"""
    return render_template('portfolio.html')

# ============= FORM SUBMISSION =============

@app.route('/submit_form', methods=['POST'])
def submit_form():
    """Handle contact form submission"""
    try:
        # Get form data
        form_data = {
            'name': request.form.get('entry.2005620554', ''),
            'email': request.form.get('entry.1045781291', ''),
            'phone': request.form.get('entry.1166974658', ''),
            'service': request.form.get('entry.839337160', ''),
            'project_goals': request.form.get('entry.1409986791', ''),
            'budget': request.form.get('entry.176533422', ''),
            'message': request.form.get('entry.920840346', ''),
            'timestamp': request.form.get('timestamp', datetime.now().isoformat()),
            'submission_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Validate required fields
        if not form_data['name'] or not form_data['email'] or not form_data['message']:
            return jsonify({
                'error': 'Please fill in all required fields (Name, Email, and Message)'
            }), 400
        
        # Save submission
        if save_submission(form_data):
            return jsonify({
                'message': 'Thank you! Your message has been sent successfully. We will get back to you soon.',
                'success': True
            }), 200
        else:
            return jsonify({
                'error': 'There was an error saving your submission. Please try again.'
            }), 500
            
    except Exception as e:
        print(f"Form submission error: {e}")
        return jsonify({
            'error': 'An unexpected error occurred. Please try again later.'
        }), 500

# ============= API ENDPOINTS (Optional) =============

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Get all form submissions (admin only - add authentication in production)"""
    try:
        if os.path.exists(SUBMISSIONS_FILE):
            with open(SUBMISSIONS_FILE, 'r') as f:
                submissions = json.load(f)
            return jsonify({
                'success': True,
                'count': len(submissions),
                'submissions': submissions
            }), 200
        else:
            return jsonify({
                'success': True,
                'count': 0,
                'submissions': []
            }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# ============= UTILITY ROUTES =============

@app.route('/sitemap.xml')
def sitemap():
    """Generate sitemap"""
    pages = []
    ten_days_ago = (datetime.now() - timedelta(days=10)).date().isoformat()
    
    # Add all your routes here
    routes = [
        ('index', 1.0, 'daily'),
        ('all_blogs', 0.8, 'weekly'),
        ('join_us', 0.7, 'monthly'),
        ('about', 0.9, 'monthly'),
        ('services', 0.9, 'monthly'),
        ('contact', 0.8, 'monthly'),
        ('portfolio', 0.9, 'weekly'),
    ]
    
    for route, priority, changefreq in routes:
        pages.append({
            'loc': url_for(route, _external=True),
            'lastmod': ten_days_ago,
            'priority': priority,
            'changefreq': changefreq
        })
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{page["loc"]}</loc>\n'
        sitemap_xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        sitemap_xml += f'    <priority>{page["priority"]}</priority>\n'
        sitemap_xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        sitemap_xml += '  </url>\n'
    
    sitemap_xml += '</urlset>'
    
    from flask import Response
    return Response(sitemap_xml, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Robots.txt file"""
    robots_txt = """User-agent: *
Allow: /
Sitemap: {}/sitemap.xml
""".format(request.url_root.rstrip('/'))
    
    from flask import Response
    return Response(robots_txt, mimetype='text/plain')

# ============= RUN APPLICATION =============

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('templates/blogs', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run the application
    # Set debug=False in production
    app.run(debug=True, host='0.0.0.0', port=5000)