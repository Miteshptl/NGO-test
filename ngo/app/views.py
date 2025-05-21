from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, Contact, Media, Blog, Project, Donation, OurWork, Admin_profile, Task,Emp_Profile,Vol_Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from .models import User  





import random
import razorpay
# Create your views here.

# index views
def index(request):
    blogs=Blog.objects.filter(published=True).order_by('-id')[:3]
    projects=Project.objects.filter(is_active=True).order_by('-id')[:3]
    media=Media.objects.all().order_by('-id')[:3]
    our_work=OurWork.objects.all().order_by('-id')[:3]
    context = {
        'blogs': blogs,
        'projects': projects,
        'media': media,
        'our_work': our_work,
    }
    return render(request, 'index.html',context)

# about views
def about(request):
    return render(request, 'about.html')

# our_work views
def our_work(request):
    ourwork=OurWork.objects.all().order_by('-id')
    context = {
        'ourwork': ourwork,
    }
    return render(request, 'our_work.html',context)

# projects views
def projects(request):
    projects=Project.objects.filter(is_active=True).order_by('-id')
    context = {
        'projects': projects,
    }
    return render(request, 'projects.html',context)

# media views
def media(request):
    media=Media.objects.all().order_by('-id')
    context = {
        'media': media,
    }
    return render(request, 'media.html',context)

# volunteer views
def volunteer(request):
    return render(request, 'volunteer.html')

# blogs views
def blogs(request):
    blogs=Blog.objects.filter(published=True).order_by('-id')
    context = {
        'blogs': blogs,
    }
    return render(request, 'blogs.html',context)

# contact views
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect('contact')
    return render(request, 'contact.html')

# donate views
def donate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        message = request.POST.get('message', '')
        is_anonymous = request.POST.get('anonymous', False)
        Donation.objects.create(amount=amount, message=message, is_anonymous=is_anonymous)
        return redirect('donate')
    return render(request, 'donate.html')


# Validation 
def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if len(password) > 128:
        raise ValidationError("Password cannot exceed 128 characters.")


    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "@$!%*?&"

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not has_digit:
        raise ValidationError("Password must contain at least one digit.")
    if not has_special:
        raise ValidationError(
            "Password must contain at least one special character (e.g., @$!%*?&)."
        )
    common_passwords = [
        "password",
        "123456",
        "qwerty",
        "abc123",
    ] 
    if password in common_passwords:
        raise ValidationError("This password is too common. Please choose another one.")


@login_required
def task(request):
    return render(request, 'task.html')



# role dashboard views

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('access_denied')
    return render(request, 'admin_dashboard.html')

@login_required
def employee_dashboard(request):
    if request.user.role != 'employee':
        return redirect('access_denied')
    return render(request, 'employee_dashboard.html')

@login_required
def volunteer_dashboard(request):
    if request.user.role != 'volunteer':
        return redirect('access_denied')
    
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'volunteer_dashboard.html', {'tasks': tasks})

def access_denied(request):
    return render(request, 'access_denied.html')


# signup views
def signup(request):
    context = {}
    if request.method == "GET":
        return render(request, "signup.html")
    
    uname = request.POST.get("uname", "").strip()
    uemail = request.POST.get("uemail", "").strip()
    upass = request.POST.get("upass", "")
    ucpass = request.POST.get("ucpass", "")

    if not uname or not uemail or not upass or not ucpass:
        context["errmsg"] = "All fields are required."
        return render(request, "signup.html", context)

    if upass != ucpass:
        context["errmsg"] = "Passwords do not match."
        return render(request, "signup.html", context)

    if uname.isdigit():
        context["errmsg"] = "Username cannot be all numbers."
        return render(request, "signup.html", context)

    if upass == uname:
        context["errmsg"] = "Password cannot be the same as username."
        return render(request, "signup.html", context)

    try:
        validate_password(upass)
    except ValidationError as e:
        context["errmsg"] = e.messages[0]
        return render(request, "signup.html", context)

    if User.objects.filter(username=uname).exists():
        context["errmsg"] = "Username already taken."
        return render(request, "signup.html", context)

    if User.objects.filter(email=uemail).exists():
        context["errmsg"] = "Email already registered."
        return render(request, "signup.html", context)

    user = User(username=uname, email=uemail)
    user.set_password(upass)  
    user.save()

    return redirect("signin")


# Signin views
def signin(request):
    context = {}
    if request.method == "POST":
        uname = request.POST.get("uname", "").strip()
        upass = request.POST.get("upass", "").strip()
        role = request.POST.get("role", "").strip()

        if not uname or not upass or not role:
            context["errmsg"] = "All fields are required."
            return render(request, "signin.html", context)

        user = authenticate(request, username=uname, password=upass)
        if user is not None:
            if user.role == role:
                login(request, user)
                return redirect(f'{role}_dashboard')
            else:
                context["errmsg"] = f"You are not authorized as {role.title()}."
        else:
            context["errmsg"] = "Invalid username or password."

    return render(request, "signin.html", context)


# Logout views
def userlogout(req):
    logout(req)
    return redirect("/")

# request Reset password views
def request_password_reset(req):
    if req.method == "GET":
        return render(req, "request_password_reset.html")
    else:
        uname = req.POST.get("uname")
        context = {}
        try:
            userdata = User.objects.get(username=uname)

            # Generate OTP and store in session
            userotp = random.randint(100000, 999999)
            req.session["otp"] = userotp
            req.session["uemail"] = userdata.email  
            # Send OTP via email
            subject = " NGO - OTP for Reset Password"
            message = f"""
            Hello {userdata.username},

            Your OTP to reset your password is: {userotp}

            If you didn’t request this, please ignore this email.

            Thank you,
            NGO.
            """
            emailfrom = settings.EMAIL_HOST_USER
            receiver = [userdata.email]
            send_mail(subject, message, emailfrom, receiver)    



            return redirect("reset_password", uname=userdata.username)

        except User.DoesNotExist:
            context["errmsg"] = "No account found with this username"
            return render(req, "request_password_reset.html", context)

# reset password Views
def reset_password(req, uname):
    userdata = User.objects.get(username=uname)
    if req.method == "GET":
        return render(req, "reset_password.html", {"user": userdata.username})
    else:
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        userdata = User.objects.get(username=uname)
        try:
            if upass == "" or ucpass == "":
                context["errmsg"] = "Field can't be empty"
                return render(req, "reset_password.html", context)
            elif upass != ucpass:
                context["errmsg"] = "Password and confirm password need to match"
                return render(req, "reset_password.html", context)
            else:
                validate_password(upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("signin")

        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "reset_password.html", context)


@login_required
def add_task(request):
    if request.user.role not in ['admin', 'employee']:
        return redirect('access_denied')
    
    if request.method == 'POST':
        assigned_to_id = request.POST['assigned_to']
        task = Task.objects.create(
            assigned_to=User.objects.get(id=assigned_to_id),
            title=request.POST['title'],
            description=request.POST['description'],
            due_date=request.POST['due_date']
        )
        return redirect('task')
    
    users = User.objects.filter(role__in=['employee', 'volunteer'])
    return render(request, 'add_task.html', {'users': users})


@login_required
def add_blog(request):
    if request.user.role not in ['admin', 'employee']:
        return redirect('access_denied')
    
    if request.method == 'POST':
        blog = Blog(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.user,
            published='published' in request.POST
        )
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        blog.save()
        return redirect('task')
    
    return render(request, 'add_blog.html')


@login_required
def add_project(request):
    if request.user.role not in ['admin', 'employee']:
        return redirect('access_denied')

    if request.method == 'POST':
        Project.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            start_date=request.POST['start_date'],
            end_date=request.POST.get('end_date') or None,
            is_active='is_active' in request.POST
        )
        return redirect('task')
    
    return render(request, 'add_project.html')


@login_required
def add_media(request):
    if request.user.role not in ['admin', 'employee']:
        return redirect('access_denied')

    if request.method == 'POST':
        Media.objects.create(
            title=request.POST['title'],
            media_type=request.POST['media_type'],
            file=request.FILES['file']
        )
        return redirect('task')
    
    return render(request, 'add_media.html')


@login_required
def add_ourwork(request):
    if request.user.role not in ['admin', 'employee']:
        return redirect('access_denied')

    if request.method == 'POST':
        OurWork.objects.create(
            title=request.POST['title'],
            summary=request.POST['summary'],
            image=request.FILES['image']
        )
        return redirect('task')
    
    return render(request, 'add_ourwork.html')

def payment_success(request):
    return render(request, 'payment_success.html')


from django.http import JsonResponse
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
@csrf_exempt
def donate(request):
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        import json
        body = json.loads(request.body)
        amount = int(body.get("amount", 0)) * 100  # Razorpay uses paise
        message = body.get("message", "")
        is_anonymous = body.get("anonymous", False)

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        # Optionally store in DB now or after success
        Donation.objects.create(
            user=request.user if not is_anonymous else None,
            amount=amount / 100,
            message=message,
            is_anonymous=is_anonymous
        )

        return JsonResponse({
            "order_id": order['id'],
            "amount": order['amount']
        })

    return render(request, "donate.html", {
        "RAZORPAY_API_KEY": settings.RAZORPAY_KEY_ID
    })
