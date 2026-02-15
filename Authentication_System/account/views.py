from django.shortcuts import render, redirect
from account.forms import RegistrationForm,PasswordResetForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email,send_reset_password_email
from account.models import User
from django .contrib.auth import authenticate,login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from core.utils import assing_permission



# ================= Home =================
def home(request):
    return render(request, "account/home.html")


# ================= Login =================

def login_view(request):
    
    # if request.user.is_authenticated:
    #     if request.user.is_seller:
    #         return redirect("seller_dash_board")
    #     elif request.user.is_customer:
    #         return redirect("customer_dashboard")
    #     return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Both fields are required.")
            return redirect("login")

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "Please activate your account first.")
                return redirect("login")

            login(request, user)

            if user.is_seller:
                return redirect("seller_dash_board")
            elif user.is_customer:
                return redirect("customer_dashboard")
            else:
                messages.error(request, "You do not have permission.")
                return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "account/login.html")



# ================= Registration =================
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False

            role = request.POST.get("role")
            if role == "seller":
                user.is_seller = True
                user.is_customer = False
            else:
                user.is_customer = True
                user.is_seller = False

            user.save()
            assing_permission(user,role)

            # ===== UID & token generate =====
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # ===== Activation link generate =====
            activation_link = request.build_absolute_uri(
                reverse("activate", kwargs={"uidb64": uidb64, "token": token})
            )

            # ===== Send activation email =====
            send_activation_email(user.email, activation_link)

            # ===== Success message & redirect =====
            messages.success(
                request,
                "Registration successful! Please check your email to activate your account."
            )
            return redirect("login")

    else:
        form = RegistrationForm()

    return render(request, "account/register.html", {"form": form})


# ================= Password Reset =================

def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()

            if not user:
                form.add_error("email", "No account found with this email address.")
                return render(request, "account/password_reset.html", {"form": form})

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = reverse(
                "password_reset_confirm_view",
                kwargs={"uidb64": uidb64, "token": token}
            )
            absolute_reset_url = request.build_absolute_uri(reset_url)
            
            send_reset_password_email(user.email, absolute_reset_url)

            messages.success(
                request,
                "We have sent a password reset link. Please check your email."
            )
            return redirect("login")

        return render(request, "account/password_reset.html", {"form": form})
    else:
        form = PasswordResetForm()
    return render(request, "account/password_reset.html", {"form": form})




def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user,token):
            messages.error(request,("This link has expired or is invalid."))
            return redirect("password_reset")
        

        if request.method == "POST":
            form = SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,("Your password has been successfully reset."))
                return redirect("login")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request,error)
        else:
            form = SetPasswordForm(user)

        return render(request,"account/password_reset_confirm.html",{"form":form,"uidb64":uidb64,"token":token})    


    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        messages.error(request,("An error occured.Place try again later"))

        return redirect("password_reset")


    



# ================= Activate Account =================
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user_obj = User.objects.get(pk=uid)

        if user_obj.is_active:
            messages.warning(request, "This account has already been activated")
            return redirect("login")

        if default_token_generator.check_token(user_obj, token):
            user_obj.is_active = True
            user_obj.save()
            messages.success(request, "Your email activation is successful.")
            return redirect("login")
        else:
            messages.error(request, "The activation link is invalid or has expired.")
            return redirect("login")

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print("Activation error:", e)
        messages.error(request, "Invalid activation link")
        return redirect("login")



