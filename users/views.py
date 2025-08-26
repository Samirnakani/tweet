from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def login(request):
    
    if request.session.get("uname") and request.session["uname"] != "Guest":
        return redirect("home")
    if "uname" not in request.session:
        request.session["uname"] = "Guest"

    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(uname=uname)
            if user.password == password:
                request.session['uname'] = user.uname
                request.session['user_id'] = user.id  
                return redirect("home")  
            else:
                return render(request, "users/login.html", {
                    "error": "Invalid password"
                })

        except User.DoesNotExist:
            return render(request, "users/login.html", {
                "error": "User not found"
            })

    # GET request
    return render(request, "users/login.html")



def register(request):
    if request.method == 'POST':
        
        uname = request.POST.get('uname')
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        pic = request.FILES.get("pic") 

        user = User(
            uname=uname,
            name=name,
            password=password,
            email=email,
            pic=pic
        )
        user.save()
        request.session['uname'] = user.uname
        request.session['user_id'] = user.id 
        return redirect("home") 

    return render(request, "users/register.html")


def logout(request):
    try:
        request.session['uname'] = "Guest"
        del request.session['user_id']   # ✅ match key name
    except KeyError:
        pass
    
    return redirect("home")   # ✅ use URL name instead of function
