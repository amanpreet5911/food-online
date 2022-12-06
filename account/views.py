from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from vendor.forms import *
from .models import *
from django.contrib import messages,auth
from .utils import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
# Create your views here.

def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied               


def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in")
        return redirect('myaccount')
    form = UserForms()
    if request.method == "POST":
        form = UserForms(request.POST)
        if form.is_valid():
            # user=form.save(commit=False)
            # user.role=User.CUSTOMER
            # user.save()
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.role = User.CUSTOMER
            user.save() 
            send_verification_email(request,user)
            messages.success(request,"Your form has been submitted successfully")
            return redirect("register")
     
        else:
            print(form.errors)
            context = {"forms": form}
            return render(request, "accounts/register.html", context)

    else:
        context = {"forms": form}

        return render(request, "accounts/register.html", context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in")
        return redirect('myaccount')
    if request.method=='POST':
        form=UserForms(request.POST)
        v_form=VendorForms(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                
            )
            user.role=User.VENDOR
            # send_verification_email(request,user)
            user.save()
            send_verification_email(request,user)
            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,"Your account has been registered successfully!!!")
            return redirect('vendor')

        else:
            print('invalid form')
            print(form.errors)
            context={
            'form':form,
            'v_form':v_form,
        }
            return render(request,'accounts/vendor.html',context)
    else:
        form=UserForms()
        v_form=VendorForms()
        context={
            'form':form,
            'v_form':v_form,
        }
        return render(request,'accounts/vendor.html',context)             

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in")
        return redirect('myaccount')
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"you heve logged in successfully")
            return redirect('myaccount')
        else:
            messages.error(request,"Invalid") 
    return render(request,"accounts/login.html")

         
        
def logout(request):
    auth.logout(request)
    messages.info(request,"Succesfully logged out")
    return redirect('login')   


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,"accounts/custDashboard.html")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,"accounts/vendorDashboard.html")    

@login_required(login_url='login')
def myaccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)



def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=user._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Yor account has been activated!!!!") 
        return redirect("myaccount") 

    else:
        messages.error(request,"invalid link")
        return redirect('myaccount')          


def forgot_password(request):
    return render(request,'accounts/forgot_password.html')   

def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=user._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,"Please reset Your password")
        return redirect("reset_password")
    else:
        messages.error(request,'The link has expired')      
        return redirect('myaccount')    


def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confrm_password=request.POST['confirm_password']
        if password==confrm_password:
            pk=request.seesion.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'password reset successful')
            return redirect('login')
        else:
            messages.error(request,"Password do not match")
            return redirect('login')    
    return render(request,'accounts/reset-password.html')   


    

        
        
