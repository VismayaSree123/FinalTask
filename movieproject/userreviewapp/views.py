from django.shortcuts import render, redirect
from .models import Reviews
# Create your views here.
def dispReview(request):
    review = Reviews.objects.all()
    return render(request, 'review.html', {'review': review})

def addReview(request):
        if request.method == 'POST':
            desc = request.POST.get('desc')
            review = Reviews(desc=desc,uname=request.user)
            review.save()
            return redirect('/userreviewapp/dispReview')
        else:
            return render(request, 'review.html')