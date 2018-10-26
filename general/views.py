from django.shortcuts import render
from .models import Intranet_Ip
# Create your views here.

def ip_in_free(request):
    nets = Intranet_Ip.objects.all()
    context = {
        'nets': nets,
    }
    return render(request, 'general/ipinfree.html', context=context)


