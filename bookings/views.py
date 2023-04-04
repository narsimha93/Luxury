from django.shortcuts import render, redirect
from .models import Bookings,PAYMENT_STATUS
from listings.models import Listing
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from btre import settings
from django.contrib.sites.shortcuts import get_current_site
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.




def booking (request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        adhar_card = request.POST['adhar_card']
        pan_card  = request.POST['pan_card']
        family_members = request.POST['family_members']
        aggrement = request.POST['aggrement']
        realtor_email = request.POST['realtor_email']
        user_id = request.user

        # Check if user has made transportation already:
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Bookings.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already book the house request')
                return redirect('/listings/'+listing_id)

        contact = Bookings( listing_id_id=int(listing_id), name=name, email=email, phone_number=phone_number,
                           adhar_card=adhar_card, pan_card=pan_card,family_members=family_members ,
                           aggrement=aggrement,user_id_id=user_id )

        contact.save()

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
       
        return redirect('/listings/'+listing_id)
   # return render(request,"booking/bookings.html")
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))
#razorpay payment gateway.


def payment(request,list_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                list = Listing.objects.get(id=list_id)
                callback_url = 'http://' + str(get_current_site(request)) + "/bookings/callback/"

                if list.price==None:
                    return HttpResponse("Price is NUll")
                notes = {'order-type': "basic order from the website", 'key': 'value'}
                razorpay_order = razorpay_client.order.create(
                    dict(amount=list.price*100, currency="USD", notes=notes, payment_capture='0'))
                context = {
                    'order_id': razorpay_order['id'],
                    'final_price':int(list.price),
                    'razorpay_merchant_id':settings.razorpay_id,
                    'callback_url':callback_url
                }
                booking = Bookings.objects.get(listing_id=list.id, user_id=request.user.id)
                booking.razorpay_order_id = razorpay_order['id']
                booking.save()
                return render(request, 'payment/paymentsummaryrazorpay.html', context)
            except ObjectDoesNotExist:
                return HttpResponse("id doesnt exist")
        return render(request, 'payment/paymentsummaryrazorpay.html')
    return HttpResponse("user is not authenticated")

                     # { 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':final_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})



def allbookings(request):
    booking = Bookings.objects.filter(user_id=request.user)

    return render(request, "booking/bookings.html", {'booking':booking,'list_id':""})

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
            client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))
            status = client.utility.verify_payment_signature(response_data)
            return status
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        booking = Bookings.objects.get(razorpay_order_id=provider_order_id)
        booking.razorpay_signature = signature_id
        booking.razorpay_payment_id = payment_id
        booking.save()
        if verify_signature(request.POST):
            booking.status = "SUCCESS"
            booking.save()
            return HttpResponse("Success")
        else:
            booking.status = "FAILURE"
            booking.save()
            return HttpResponse("Failure")
    else:
        return HttpResponse("Failure")