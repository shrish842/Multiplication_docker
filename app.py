from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.template import Template, Context
import os

# Django settings configuration
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='your-secret-key-here-multiplication-app-2025',
        ROOT_URLCONF=__name__,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                ],
            },
        }],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        STATIC_URL='/static/',
        ALLOWED_HOSTS=['*'],
    )

# HTML Template as string
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Multiplication Calculator</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 600px; 
            margin: 50px auto; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { 
            text-align: center; 
            color: #333; 
            margin-bottom: 30px;
            font-size: 2.2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: bold; 
            color: #555;
        }
        input { 
            width: 100%; 
            padding: 15px; 
            font-size: 16px; 
            border: 2px solid #ddd; 
            border-radius: 8px;
            box-sizing: border-box;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button { 
            width: 100%;
            padding: 15px 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 18px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover { 
            transform: translateY(-2px);
        }
        .result { 
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 25px; 
            border-radius: 10px; 
            margin-top: 25px;
            text-align: center;
        }
        .result h3 {
            margin: 0 0 15px 0;
            color: #333;
        }
        .calculation {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
        .error { 
            background: #ffebee; 
            color: #c62828; 
            padding: 15px; 
            border-radius: 8px; 
            margin-top: 20px;
            border-left: 4px solid #c62828;
        }
        .multiplication-symbol {
            font-size: 2em;
            color: #667eea;
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔢 Multiplication Calculator</h1>
        
        <form method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
            
            <div class="form-group">
                <label for="num1">First Number:</label>
                <input type="number" step="any" name="num1" id="num1" 
                       placeholder="Enter first number" required 
                       value="{% if num1 %}{{ num1 }}{% endif %}">
            </div>
            
            <div class="multiplication-symbol">×</div>
            
            <div class="form-group">
                <label for="num2">Second Number:</label>
                <input type="number" step="any" name="num2" id="num2" 
                       placeholder="Enter second number" required
                       value="{% if num2 %}{{ num2 }}{% endif %}">
            </div>
            
            <button type="submit">Calculate Result</button>
        </form>
        
        {% if error %}
            <div class="error">
                <strong>Error:</strong> {{ error }}
            </div>
        {% endif %}
        
        {% if calculated %}
            <div class="result">
                <h3>🎯 Calculation Result</h3>
                <div class="calculation">{{ num1 }} × {{ num2 }} = {{ result }}</div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def home(request):
    """Home page with multiplication calculator"""
    context = {}
    
    if request.method == 'POST':
        try:
            # Get form data
            num1_str = request.POST.get('num1', '')
            num2_str = request.POST.get('num2', '')
            
            # Validate inputs
            if not num1_str or not num2_str:
                context['error'] = "Please enter both numbers"
            else:
                num1 = float(num1_str)
                num2 = float(num2_str)
                result = num1 * num2
                
                context.update({
                    'num1': num1,
                    'num2': num2,
                    'result': result,
                    'calculated': True
                })
                
        except (ValueError, TypeError):
            context['error'] = "Please enter valid numbers (decimals are allowed)"
    
    # Render template from string
    template = Template(HOME_TEMPLATE)
    
    # Add CSRF token to context
    from django.middleware.csrf import get_token
    context['csrf_token'] = get_token(request)
    
    rendered_html = template.render(Context(context))
    return HttpResponse(rendered_html)

def api_multiply(request):
    """Simple API endpoint for multiplication"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            num1 = float(data.get('num1', 0))
            num2 = float(data.get('num2', 0))
            result = num1 * num2
            
            response_data = {
                'num1': num1,
                'num2': num2,
                'result': result,
                'operation': 'multiplication'
            }
            return HttpResponse(
                json.dumps(response_data),
                content_type='application/json'
            )
        except Exception as e:
            return HttpResponse(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=400
            )
    
    return HttpResponse(
        json.dumps({'error': 'Only POST method allowed'}),
        content_type='application/json',
        status=405
    )

# URL patterns
urlpatterns = [
    path('', home, name='home'),
    path('api/multiply/', api_multiply, name='api_multiply'),
]

# WSGI application
application = get_wsgi_application()

if __name__ == '__main__':
    import django
    from django.core.management import execute_from_command_line
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
    django.setup()
    
    print("🚀 Starting Django Multiplication Calculator...")
    print("📱 Access at: http://127.0.0.1:8000/")
    print("🔗 API endpoint: http://127.0.0.1:8000/api/multiply/")
    print("⏹️  Press CTRL+C to stop the server")
    
    # Run development server
    import sys
    sys.argv = ['app.py', 'runserver', '0.0.0.0:8000']
    execute_from_command_line(sys.argv)