from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Tweet
from users.models import User
from .forms import TweetForm   # ✅ use corrected class name
from django.contrib import messages
import traceback
from django.http import JsonResponse



def home(request):
    tweets = Tweet.objects.select_related("user").order_by("-created_at")
    uname = request.session.get("uname", "Guest")
    uid = request.session.get("user_id")  
    return render(request, "tweets/tweet_home.html", {
        "uname": uname,
        "uid": uid,
        "tweets": tweets
    })

def tweet_create(request):
    uid = request.session.get("user_id")
    uname = request.session.get("uname", "guest")
    
    if request.method == "POST":
        print(f"POST - UID: {uid}, Content: {request.POST.get('content')}")
        
        if not uid:
            messages.error(request, "⚠️ Guests cannot post. Please login first.")
        else:
            form = TweetForm(request.POST, request.FILES)
            
            if form.is_valid():
                print("Form valid - attempting save")
                try:
                    user = User.objects.get(id=uid)
                    tweet = form.save(commit=False)
                    tweet.user = user
                    tweet.save()
                    
                    print(f"✅ Saved tweet ID: {tweet.id}")
                    messages.success(request, "✅ Tweet posted successfully!")
                    return redirect('tweet_create')
                    
                except Exception as e:
                    print(f"❌ Save error: {e}")
                    messages.error(request, f"Error: {e}")
            else:
                print(f"❌ Form invalid: {form.errors}")
        
        form = TweetForm(request.POST, request.FILES)
    else:
        form = TweetForm()
    
    return render(request, "tweets/tweet_create.html", {
        "form": form, 'uname': uname, 'uid': uid
    })
def tweet_edit(request, tweet_id):
    uid = request.session.get("user_id")   
    user = get_object_or_404(User, id=uid)
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=user)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TweetForm(instance=tweet)

    return render(request, "tweets/tweet_edit.html", {'form': form})


def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    uname = request.session.get("uname")

    if uname and tweet.user.uname == uname:   # ✅ check with session uname
        tweet.delete()

    return redirect("home")


def tweet_detail_ajax(request, tweet_id):
    try:
        print(f"=== TWEET DETAIL DEBUG ===")
        print(f"Tweet ID requested: {tweet_id}")
        
        tweet = get_object_or_404(Tweet.objects.select_related("user"), id=tweet_id)
        print(f"Tweet found: {tweet}")
        print(f"Tweet user: {tweet.user}")
        print(f"Tweet content: {tweet.content}")
        print(f"Tweet image: {tweet.image}")
        print(f"User pic: {tweet.user.pic.url}")
        
        data = {
            'id': tweet.id,
            'content': tweet.content,
            'user_name': tweet.user.uname,
            'user_email': tweet.user.email,
            'created_at': tweet.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'updated_at': tweet.updated_at.strftime('%B %d, %Y at %I:%M %p') if tweet.updated_at != tweet.created_at else None,
            'image_url': tweet.image.url if tweet.image else None,
            'user_pic': tweet.user.pic.url if tweet.user.pic else None,
        }
        
        print(f"Data to return: {data}")
        return JsonResponse(data)
        
    except Exception as e:
        print(f"❌ Error in tweet_detail_ajax: {str(e)}")
        print(f"Error type: {type(e)}")
        traceback.print_exc()
        
        # Return error as JSON instead of 500
        return JsonResponse({
            'error': str(e),
            'tweet_id': tweet_id
        }, status=500)