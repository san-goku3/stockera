# admin_app/views.py
# admin_app/views.py
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user_model
import re
from django.db import connection
from django.conf import settings
from django.core.paginator import Paginator
from .models import IPOInfo
from django.core.files.storage import default_storage
from django.core.files.images import get_image_dimensions
from django.http import JsonResponse
from django.db.models import F
import os
from datetime import datetime



User = get_user_model()

def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Validation
        errors = {}
        
        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Enter a valid email address.'
        
        # Password validation
        if len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'
        if not re.search(r'[A-Z]', password):
            errors['password'] = 'Password must contain at least one uppercase letter.'
        if not re.search(r'[a-z]', password):
            errors['password'] = 'Password must contain at least one lowercase letter.'
        if not re.search(r'[0-9]', password):
            errors['password'] = 'Password must contain at least one number.'
        if not re.search(r'[\W_]', password):
            errors['password'] = 'Password must contain at least one special character.'
        
        if errors:
            return render(request, 'sign_in.html', {'errors': errors})
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            errors['auth'] = 'Invalid email or password'
            return render(request, 'sign_in.html', {'errors': errors})
    
    return render(request, 'sign_in.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        # Validation
        errors = {}
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Enter a valid email address.'
        
        if email:
            if not User.objects.filter(email=email).exists():
                errors['email'] = 'Email address not found.'
        else:
            errors['email'] = 'Please enter your email address'

        if errors:
            return render(request, 'forgot_password.html', {'errors': errors})
        
        # Handle password reset logic here
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        password_reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uid, token]))

        # Send email
        subject = "Password Reset Requested"
        email_template_name = "password_reset_email.html"
        context = {
            "email": user.email,
            "domain": request.META['HTTP_HOST'],
            "site_name": "Bluestock Fintech",
            "uid": uid,
            "user": user,
            "token": token,
            "protocol": "http",
        }
        email_message = render_to_string(email_template_name, context)
        send_mail(subject, email_message, 'akash.naren1997@gmail.com', [user.email], fail_silently=False)

        # Redirect to sign in page with success message
        return render(request, 'sign_in.html', {'message': 'A password reset link has been sent to your email address.'})
    
    return render(request, 'forgot_password.html')

def create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Validation
        errors = {}
        
        # Username validation
        if username: 
            if User.objects.filter(username=username).exists():
                errors['username'] = 'Username already exists.'
        else:
            errors['username'] = 'Please enter username.'
        
        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Enter a valid email address.'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists.'
        
        # Password validation
        if password:
            if len(password) < 8:
                errors['password'] = 'Password must be at least 8 characters long.'
            if not re.search(r'[A-Z]', password):
                errors['password'] = 'Password must contain at least one uppercase letter.'
            if not re.search(r'[a-z]', password):
                errors['password'] = 'Password must contain at least one lowercase letter.'
            if not re.search(r'[0-9]', password):
                errors['password'] = 'Password must contain at least one number.'
            if not re.search(r'[\W_]', password):
                errors['password'] = 'Password must contain at least one special character.'
        else:
            errors['password'] = 'Please enter the Password'

        
        if errors:
            return render(request, 'create_account.html', {
                'errors': errors,
                'username': username,
                'email': email,
                'password': password
            })
        
        # Handle account creation logic here
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'create_account.html')

def dashboard(request):
    username = request.user.username if request.user.is_authenticated else 'Guest'
    # Split the full name by spaces
    name_parts = username.split()
    
    # Take the first letter of each part and capitalize it
    usernameabbrevation = ''.join([name[0].upper() for name in name_parts])

    section = request.GET.get('section', 'dashboard-section')

    numeric_pattern = r'^-?\d+(\.\d+)?$'
    errors = []

    if request.method == 'POST':
        if 'register_ipo' in request.POST:
            # Validate company name
            section = 'manage-ipo-section'
            company_name = request.POST['company_name'].strip()
            if not company_name:
                errors.append("Company name is required.")
            elif IPOInfo.objects.filter(company_name=company_name).exists():
                errors.append("Company name already exists. Please choose a different name.")

            # Validate company logo
            company_logo = request.FILES.get('company_logo')
            """
            if not company_logo:
                errors.append("Company logo is required.")
            else:
                try:
                    width, height = get_image_dimensions(company_logo)
                    if width > 1024 or height > 1024:
                        errors.append("Company logo dimensions should not exceed 1024x1024 pixels.")
                    if company_logo.size > 5 * 1024 * 1024:
                        errors.append("Company logo file size should not exceed 5MB.")
                except ValidationError as e:
                    errors.append(f"Invalid image: {e}")
            """
            if not company_logo:
                errors.append("Company logo is required.")

            # Validate price_band
            price_band = request.POST.get('price_band', '').strip()
            if price_band:
                # Pattern to match a numeric range (e.g., -628.25 - 531.66)
                price_band_pattern = r'^-?\d+(\.\d+)?\s*-\s*-?\d+(\.\d+)?$'
    
                # Check if the input matches the pattern
                if not re.match(price_band_pattern, price_band):
                    errors.append("Price band should be in the format '159 - 164' or '-628.25 - 531.66'.")
                else:
                    # Further validation to ensure the lower value is less than or equal to the higher value
                    lower_value, higher_value = [float(value.strip()) for value in price_band.split('-')]
                    if lower_value > higher_value:
                        errors.append("In the price band, the first value should be less than or equal to the second value.")

            # Validate issue_size
            issue_size = request.POST.get('issue_size', '').strip()
            if issue_size and not re.match(numeric_pattern, issue_size):
                errors.append("Issue size should be a valid numeric value.")

            # Validate ipo_price
            ipo_price = request.POST.get('ipo_price', '').strip()
            if ipo_price and not re.match(numeric_pattern, ipo_price):
                errors.append("IPO price should be a valid numeric value.")

            # Validate listing_price
            listing_price = request.POST.get('listing_price', '').strip()
            if listing_price and not re.match(numeric_pattern, listing_price):
                errors.append("Listing price should be a valid numeric value.")

            # Validate listing_gain
            listing_gain = request.POST.get('listing_gain', '').strip()
            if listing_gain and not re.match(numeric_pattern, listing_gain):
                errors.append("Listing gain should be a valid numeric value and can be negative or positive.")

            # Validate cmp
            cmp = request.POST.get('cmp', '').strip()
            if cmp and not re.match(numeric_pattern, cmp):
                errors.append("CMP should be a valid numeric value and can be negative or positive.")

            # Validate current_return
            current_return = request.POST.get('current_return', '').strip()
            if current_return and not re.match(numeric_pattern, current_return):
                errors.append("Current return should be a valid numeric value.")

            # Validate RHP link
            rhp = request.POST.get('rhp_link', '').strip()
            if rhp and not (rhp.startswith('https://') or rhp.startswith('http://')):
                errors.append("RHP link should start with 'https://' or 'http://'.")

            # Validate DRHP link
            drhp = request.POST.get('drhp_link', '').strip()
            if drhp and not (drhp.startswith('https://') or drhp.startswith('http://')):
                errors.append("DRHP link should start with 'https://' or 'http://'.")

            # If no errors, proceed to save the IPO
            if not errors:
                company_logo_path = default_storage.save(f"company_logos/{company_logo.name}", company_logo) if company_logo else None

                IPOInfo.objects.create(
                    company_logo_path=company_logo_path,
                    company_name=company_name,
                    price_band=price_band,
                    open=request.POST['open'],
                    close=request.POST['close'],
                    issue_size=issue_size,
                    issue_type=request.POST['issue_type'],
                    listing_date=request.POST['listing_date'],
                    status=request.POST['status'],
                    ipo_price=ipo_price,
                    listing_price=listing_price,
                    listing_gain=listing_gain,
                    cmp=cmp,
                    current_return=current_return,
                    rhp=rhp,
                    drhp=drhp
                )

                return redirect(f"{reverse('dashboard')}?section=manage-ipo-section")

        elif 'update_ipo' in request.POST:
            # Update IPO logic
            print('Update IPO is working')
            section = 'manage-ipo-section'
            ipo_id = request.POST['ipo_id']
            ipo = IPOInfo.objects.get(id=ipo_id)

            # Delete the old photo if a new one is uploaded
            company_logo = request.FILES.get('company_logo')
            if company_logo:
                if ipo.company_logo_path:
                    old_logo_path = ipo.company_logo_path
                    if default_storage.exists(old_logo_path):
                        default_storage.delete(old_logo_path)
                ipo.company_logo_path = default_storage.save(f"company_logos/{company_logo.name}", company_logo)

            ipo.company_name = request.POST['company_name']
            ipo.price_band = request.POST['price_band']
            ipo.open = request.POST['open']
            ipo.close = request.POST['close']
            ipo.issue_size = request.POST['issue_size']
            ipo.issue_type = request.POST['issue_type']
            ipo.listing_date = request.POST['listing_date']
            ipo.status = request.POST['status']
            ipo.ipo_price = request.POST['ipo_price']
            ipo.listing_price = request.POST['listing_price']
            ipo.listing_gain = request.POST['listing_gain']
            ipo.cmp = request.POST['cmp']
            ipo.current_return = request.POST['current_return']
            ipo.rhp = request.POST.get('rhp_link')
            ipo.drhp = request.POST.get('drhp_link')

            ipo.save()

            return redirect(f"{reverse('dashboard')}?section=manage-ipo-section")

    ipo_list = IPOInfo.objects.all()

    for ipo in ipo_list:
        if ipo.open:
            try:
                ipo.open = datetime.strptime(ipo.open, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            except ValueError:
                ipo.open = datetime.strptime(ipo.open, '%Y-%m-%d').strftime('%Y-%m-%d')
    
        if ipo.close:
            try:
                ipo.close = datetime.strptime(ipo.close, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            except ValueError:
                ipo.close = datetime.strptime(ipo.close, '%Y-%m-%d').strftime('%Y-%m-%d')

        if ipo.listing_date:
            try:
                ipo.listing_date = datetime.strptime(ipo.listing_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            except ValueError:
                ipo.listing_date = datetime.strptime(ipo.listing_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    
    paginator = Paginator(ipo_list, 4)  # Show 4 IPOs per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object

    ipo_counts = {
        "total_ipo": IPOInfo.objects.count(),
        "total_ipo_gain": IPOInfo.objects.filter(listing_price__lt=F('current_return')).count(),
        "total_ipo_loss": IPOInfo.objects.filter(listing_price__gt=F('current_return')).count(),
        "total_ipo_ongoing": IPOInfo.objects.filter(status=3).count(),
        "total_ipo_upcomming": IPOInfo.objects.filter(status=2).count(),
        "total_ipo_new_listed": IPOInfo.objects.filter(status=1).count(),
    }

    context = {
        'username': username,
        'usernameabbrevation': usernameabbrevation,
        'page_obj': page_obj,
        'ipo_counts': ipo_counts,
        'section': section,
        'errors': errors,
    }

    print(context)

    return render(request, 'dashboard.html', context)
"""
def get_ipo_data(request, ipo_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM ipo_info WHERE id = %s", [ipo_id])
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchone()
        ipo_data = dict(zip(columns, data))
        print(ipo_data)
    return JsonResponse(ipo_data)

def delete_ipo(request, ipo_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ipo_info WHERE id=%s", [ipo_id])
        return redirect(f"{reverse('dashboard')}?section=manage-ipo-section")
"""
def get_ipo_data(request, ipo_id):
    ipo_data = IPOInfo.objects.filter(id=ipo_id).values().first()
    ipo_data['company_logo_path'] = settings.MEDIA_URL + ipo_data['company_logo_path']
    print(ipo_data)
    return JsonResponse(ipo_data)

def delete_ipo(request, ipo_id):
    if request.method == 'POST':
        ipo = IPOInfo.objects.get(id=ipo_id)

        # Delete the photo associated with the IPO
        if ipo.company_logo_path:
            if default_storage.exists(ipo.company_logo_path):
                default_storage.delete(ipo.company_logo_path)

        # Delete the IPO record from the database
        ipo.delete()

        return redirect(f"{reverse('dashboard')}?section=manage-ipo-section")
#######################################################################################################################################

