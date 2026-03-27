from django.http import JsonResponse
from .models import Employee
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import UserProfile
import requests


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_employee(request):


    if request.method == "POST":

        data = request.data 

        Employee.objects.create(
           dept=data.get('dept'),
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            joining_date=data.get('joiningDate'),
            profile=data.get('profile'),
            country=data.get('country'),
            state=data.get('state'),
            city=data.get('city'),
            pincode=data.get('pincode'),
            contact_no=data.get('contact'),
            email=data.get('email')
        )

        return JsonResponse({"message": "Employee Added"}, status=201)
    return JsonResponse({"error": "Invalid request"}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])   # 🔒 ONLY LOGGED-IN AUTHORITY
def register_user(request):

    if not request.user.is_staff:
        return Response({"error": "Not authorized"}, status=403)

    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    contact = request.data.get("contact")

    if User.objects.filter(username=username).exists():
        return Response({"error": "User exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        is_staff=True   # authority
    )

    UserProfile.objects.create(user=user, contact_no=contact)

    return Response({"message": "Authority created"})


@csrf_exempt
@api_view(['POST'])
def login_user(request):

    username = (request.data.get("username") or "").strip()
    password = request.data.get("password") or ""

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    if not user.is_staff:
        return Response({"error": "User is not authority"}, status=403)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_employee(request, emp_id):

    try:

        emp = Employee.objects.get(id=emp_id)

        data = {
            "id": emp.id,
            "dept": emp.dept,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "joining_date": str(emp.joining_date),
            "profile": emp.profile,
            "country": emp.country,
            "state": emp.state,
            "city": emp.city,
            "pincode": emp.pincode,
            "contact_no": emp.contact_no,
            "email": emp.email
        }

        return JsonResponse(data)

    except Employee.DoesNotExist:

        return JsonResponse({"error": "Employee not found"})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_employee(request, emp_id):

    if request.method == "DELETE":

        try:

            emp = Employee.objects.get(id=emp_id)

            emp.delete()

            return JsonResponse({"message": "Employee deleted"})

        except Employee.DoesNotExist:

            return JsonResponse({"error": "Employee not found"}, status=404)    
        
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_employee(request, emp_id):

    try:
        emp = Employee.objects.get(id=emp_id)

        data = request.data

        emp.dept = data.get('dept')
        emp.first_name = data.get('firstName')
        emp.last_name = data.get('lastName')
        emp.joining_date = data.get('joiningDate')
        emp.profile = data.get('profile')
        emp.country = data.get('country')
        emp.state = data.get('state')
        emp.city = data.get('city')
        emp.pincode = data.get('pincode')
        emp.contact_no = data.get('contact')
        emp.email = data.get('email')

        emp.save()

        return Response({"message": "Employee updated successfully"})

    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)
    
def employee_home(request):
    return HttpResponse("Employee API is running")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employees(request):

    dept = request.GET.get('dept')
    profile = request.GET.get('profile')
    country = request.GET.get('country')
    state = request.GET.get('state')
    city = request.GET.get('city')

    employees = Employee.objects.all()

    if dept:
        employees = employees.filter(dept=dept)

    if profile:
        employees = employees.filter(profile=profile)

    if country:
        employees = employees.filter(country=country)

    if state:
        employees = employees.filter(state=state)

    if city:
        employees = employees.filter(city=city)

    data = list(employees.values())

    return JsonResponse(data, safe=False)

from django.http import JsonResponse

# ✅ COUNTRIES
def get_countries(request):
    countries = Employee.objects.values_list('country', flat=True).distinct()
    return JsonResponse(list(countries), safe=False)


# ✅ STATES
def get_states(request, country):
    states = Employee.objects.filter(country=country).values_list('state', flat=True).distinct()
    return JsonResponse(list(states), safe=False)


# ✅ CITIES
def get_cities(request, state):
    cities = Employee.objects.filter(state=state).values_list('city', flat=True).distinct()
    return JsonResponse(list(cities), safe=False)


# 🔐 OAUTH HANDLERS
@api_view(['POST'])
@permission_classes([AllowAny])
def oauth_google_callback(request):
    """
    Handle Google OAuth callback with access token.
    Frontend sends: { "accessToken": "..." }
    """
    access_token = request.data.get('accessToken')
    
    if not access_token:
        return Response({"error": "Access token required"}, status=400)
    
    try:
        # Get user info from Google
        response = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if response.status_code != 200:
            return Response({"error": "Invalid access token"}, status=401)
        
        user_info = response.json()
        email = user_info.get('email')
        
        if not email:
            return Response({"error": "Email not provided by Google"}, status=400)
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'is_staff': False  # Require admin to set as staff
            }
        )
        

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def oauth_linkedin_callback(request):
    """
    Handle LinkedIn OAuth callback with access token.
    Frontend sends: { "accessToken": "..." }
    """
    access_token = request.data.get('accessToken')
    
    if not access_token:
        return Response({"error": "Access token required"}, status=400)
    
    try:
        # Get user info from LinkedIn
        response = requests.get(
            'https://api.linkedin.com/v2/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if response.status_code != 200:
            return Response({"error": "Invalid access token"}, status=401)
        
        user_info = response.json()
        
        # Get email from LinkedIn
        email_response = requests.get(
            'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        email = None
        if email_response.status_code == 200:
            email_data = email_response.json()
            if 'elements' in email_data and len(email_data['elements']) > 0:
                email = email_data['elements'][0]['handle~']['emailAddress']
        
        if not email:
            return Response({"error": "Email not provided by LinkedIn"}, status=400)
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': user_info.get('localizedFirstName', ''),
                'last_name': user_info.get('localizedLastName', ''),
                'is_staff': False
            }
        )
        

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def oauth_success_redirect(request):
    """
    Called by LOGIN_REDIRECT_URL after successful django-allauth OAuth flow.
    Generates a JWT for the newly session-authenticated user and redirects to React.
    """
    user = request.user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    # CRITICAL SECURITY & LOGIC FIX:
    # Destroy the Django session immediately!
    # Otherwise, the browser holds a persistent sessionid on 127.0.0.1:8000,
    # causing subsequent "Continue with Google/LinkedIn" clicks to collide
    # and violently crash with "Third-Party Login Failure" (account linking constraints).
    logout(request)
    
    # Redirect back to the React app with the token in the URL query string
    return redirect(f"http://localhost:3001/?token={access_token}")