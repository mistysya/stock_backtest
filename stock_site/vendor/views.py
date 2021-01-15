from django.shortcuts import render
from .models import Vendor

# Create your views here.
def vendor_index(request):
    vendor_list = Vendor.objects.all()
    context = {'vendor_list': vendor_list}
    return render(request, 'test.html', context)
