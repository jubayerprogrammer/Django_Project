from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden

error = """ 


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403 Forbidden</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .error-container {
            background: #ffffff;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            text-align: center;
        }

        .error-code {
            font-size: 100px;
            font-weight: bold;
            color: #dc3545;
        }

        .error-message {
            font-size: 24px;
            margin-bottom: 20px;
            color: #343a40;
        }

        .error-description {
            color: #6c757d;
            margin-bottom: 30px;
        }

        .btn-home {
            padding: 12px 30px;
            font-size: 16px;
        }
    </style>
</head>
<body>

    <div class="error-container">
        <div class="error-code">403</div>
        <div class="error-message">Access Forbidden</div>
        <div class="error-description">Sorry, you don't have permission to access this page.</div>
        <a href="/" class="btn btn-danger btn-home">Go Back Home</a>
    </div>

    <!-- Bootstrap JS (optional) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>




"""



def login_and_role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _warpped_view(request,*arg,**kwargs):
            user = request.user
            if required_role == "customer" and not user.is_customer:
                return HttpResponseForbidden(error)
            if required_role == "seller" and not user.is_seller:
                return HttpResponseForbidden(error)
            return view_func(request,*arg,**kwargs)
        return _warpped_view
    return decorator

    
        

