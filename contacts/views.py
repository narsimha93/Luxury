from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact,transportation, reviews
from listings.models import Listing

def contact (request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already:
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id )

        contact.save()

        # SEND EMAIL
        # send_mail(
        #     'Property Listing Inquiry',
        #     'There has been an inquiry fro ' + listing + '. Sign in to the admin panel for more information.',
        #     'realestate@gmail.com',
        #     [realtor_email, ],
        #     fail_silently=False
        # )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/'+listing_id)
    


def trans (request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        owner_phone_number = request.POST['owner_phone_number']
        onwer_address = request.POST['onwer_address']
        no_of_boxes  = request.POST['no_of_boxes']
        truck_requirement = request.POST['truck_requirement']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made transportation already:
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = transportation.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an transportation request')
                return redirect('/listings/'+listing_id)

        contact = transportation(listing=listing, listing_id=listing_id, name=name, email=email, owner_phone_number=owner_phone_number,
                           onwer_address=onwer_address, no_of_boxes=no_of_boxes,truck_requirement=truck_requirement ,user_id=user_id )

        contact.save()

        # SEND EMAIL
        # send_mail(
        #     'Property Listing Inquiry',
        #     'There has been an inquiry fro ' + listing + '. Sign in to the admin panel for more information.',
        #     'realestate@gmail.com',
        #     [realtor_email, ],
        #     fail_silently=False
        # )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/'+listing_id)
    



def postComment(request):
    print('>>>>')
    if request.method == "POST":
        comment = request.POST['comment']
        user = request.user
        listing_id =request.POST.get('listing_id')
        post = Listing.objects.get(id=listing_id)
       # parentSno = request.POST.get("parentSno")
        print("comment","user")
        #parent = reviews.objects.get(sno=parentSno)
        print(post, '>?????')
        comment = reviews(comment=comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your replay has been posted successfully")
    return redirect("/")


