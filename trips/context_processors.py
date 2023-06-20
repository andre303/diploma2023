from .forms import RegisterForm
from .models import Guide
def register_processor(request):
 form = RegisterForm()
 return {'RegisterForm': form}

def isGuide_processor(request):
    if request.user.is_authenticated:
     guide = Guide.objects.filter(user = request.user).first()
     if guide:
         return {'isGuide':True,"Guide_pk":guide.pk,"Guide_new_bookings":guide.waiting_bookings()}
    return {'isGuide':False}
