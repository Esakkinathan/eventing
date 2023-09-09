from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Events,Venue
from django.contrib.auth.models import User
from .forms import VenueForm,EventsForm,EventsFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
import csv
from django.http import FileResponse
import io
import pytz
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import pytz
from django.core.paginator import Paginator

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "eventer"
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    cal = HTMLCalendar().formatmonth(
        year, 
        month_number)
    now = datetime.now()
    current_year = now.year
    event_list = Events.objects.filter(
        event_date__year = year,
        event_date__month = month_number
        )
    day=now.day
    tz_kolkata = pytz.timezone('Asia/Kolkata')
    datetime_Mumbai = datetime.now(tz_kolkata)
    time= datetime_Mumbai.strftime('%H:%M:%S')


    return render(request,"home.html", {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time":time,
        "event_list": event_list,
        'day':day
    })

def list_event(request):
    event_list=Events.objects.all().order_by('name')
    return render(request,'list_event.html',{
        'event_list':event_list
    })

def add_venue(request):
     submitted=False
     if request.method=="POST": 
        form=VenueForm(request.POST,request.FILES)
        if form.is_valid():
            venue =form.save(commit=False)
            venue.owner = request.user.id #logged in user id
            venue.save()
            #form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
     else:
         form=VenueForm
         if 'submitted' in request.GET:
             submitted=True  
        
     return render(request,'add_venue.html',{
         "form":form,
         "submitted":submitted
     })

def list_venue(request):
    venue_list=Venue.objects.all()
    p=Paginator(Venue.objects.all(),3)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums='a'*venues.paginator.num_pages
    return render(request,'list_venues.html',{
        'venue_list':venue_list,
        'venues':venues,
        'nums':nums
    })

def show_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    events = venue.events_set.all()
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request,'show_venue.html',{
        'venue':venue,
        'venue_owner':venue_owner,
        'events':events
    })

def search_venue(request):
    if request.method == "POST" :
        searched = request.POST['searched']
        venues=Venue.objects.filter(name__contains=searched)
        return render(request,'search_venue.html',{
            'searched':searched,
            'venues':venues
            })
    else:
        return render(request,'search_venue.html',{})

def update_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    form=VenueForm(request.POST or None,request.FILES or None,instance=venue )
    if form.is_valid():
        form.save()
        return redirect('list_venue')

    return render(request,'update_venue.html',{
        'venue':venue,
        'form':form
    })

def venue_event(request,venue_id):
    venue = Venue.objects.get(id=venue_id)
    events = venue.events_set.all()
    if events:
        return render(request,'venue_event.html',{
        'events' : events
        }) 
    else:
        messages.success(request,"That venue has no events")
        return redirect('admin_Approval')

def show_event(request,event_id):
    event = Events.objects.get(pk=event_id)
    return render(request,"show_event.html",{
        'event':event
    })

def add_event(request):
    submitted=False     
    if request.method=="POST":
        if request.user.is_superuser: 
            form=EventsFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventsForm(request.POST)
            
            if form.is_valid():
                event =form.save(commit=False)
                event.manager = request.user #logged in user id
                event.save()
                #form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
         #not submmiting page
        if request.user.is_superuser:
            form = EventsFormAdmin
        else:           
            form=EventsForm
        if 'sbumitted' in request.GET:
             submitted=True  
        
    return render(request,'add_event.html',{
         "form":form,
         "submitted":submitted
     })

def update_event(request,event_id):
    event=Events.objects.get(pk=event_id)
    if request.user.is_superuser :
        form = EventsFormAdmin(request.POST or None,instance=event)
    else:   
        form=EventsForm(request.POST or None,instance=event )
    if form.is_valid():
        form.save()
        return redirect('list_event')

    return render(request,'update_event.html',{
        'event':event,
        'form':form
    })

def my_event(request):
    if request.user.is_authenticated: 
        me = request.user.id
        events = Events.objects.filter(attendees=me)
        return render(request,'my_event.html',{
            'events':events
        })
    else:
        messages.success(request,"You are'nt authorized to view this page")
        return redirect('list_event')

def search_event(request):
    if request.method == "POST" :
        searched = request.POST['searched']
        events=Events.objects.filter(name__contains=searched)
        return render(request,'search_event.html',{
            'searched':searched,
            'events':events
            })
    else:
        return render(request,'search_event.html',{})

def admin_approval(request):
    venue_list = Venue.objects.all()
   	# Get Counts
    event_count = Events.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Events.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            # Get list of checked box id's
            id_list = request.POST.getlist('boxes')

            # Uncheck all events
            event_list.update(approved=False)

            # Update the database
            for x in id_list:
                Events.objects.filter(pk=int(x)).update(approved=True)
            
            # Show Success Message and Redirect
            messages.success(request, ("Event List Approval Has Been Updated!"))
            return redirect('list-events')



        else:
            return render(request, 'events/admin_approval.html',
                {"event_list": event_list,
                "event_count":event_count,
                "venue_count":venue_count,
                "user_count":user_count,
                "venue_list":venue_list})
    else:
        messages.success(request, ("You aren't authorized to view this page!"))
        return redirect('home')



def delete_event(request,event_id):
    event=Events.objects.get(pk=event_id)
    if request.user == event.manager :
        event.delete()
        messages.success(request,"Event deleted successfully")
        return redirect('list_event')
    else:
        messages.success(request,"You are'nt authorized to delete this event")
        return redirect('list_event')

def delete_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venue')

def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    """lines=['This is line 1\n',
           'This is line 2\n',
           'This is line 3\n']
    """
    venues=Venue.objects.all()
    lines=[]
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phonenumber}\n{venue.web}\n{venue.email_address}\n\n\n')

    response.writelines(lines)
    return response

def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    writer = csv.writer(response)
    venues=Venue.objects.all()
    writer.writerow(['Venue name','Address','Zip_Code','Phonenumber','Web address','Email Address'])
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phonenumber,venue.web,venue.email_address])
    return response

def venue_pdf(request):
    buf = io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob= c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont('Helvetica',14)
    venues=Venue.objects.all()
    lines=[]
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phonenumber)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("=====================")
    
    for l in lines:
        textob.textLine(l)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf,as_attachment=True,filename='venue.pdf')

def event_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=events.txt'
    """lines=['This is line 1\n',
           'This is line 2\n',
           'This is line 3\n']
    """
    event=Events.objects.all()
    lines=[]
    for e in event:
        lines.append(f'{e.name}\n{e.event_date}\n{e.venue}\n{e.manager}\n{e.attendees}\n{e.description}\n\n\n')
    response.writelines(lines)
    return response


def event_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=events.csv'
    writer = csv.writer(response)
    events=Events.objects.all()
    writer.writerow(['Event Name','Event Date','Event Venue','Event Manager','Event Attendees','Event Description'])
    for e in events:
        writer.writerow([e.name,e.event_date,e.venue,e.manager,e.attendees,e.description])
    return response

def event_pdf(request):
    buf = io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob= c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont('Helvetica',14)
    events=Events.objects.all()
    lines=[]
    for event in events:
        lines.append(event.name)
        lines.append(event.event_date)
        lines.append(event.venue)
        lines.append(event.manager)
        lines.append(event.attendees)
        lines.append(event.description)
        lines.append("=====================")
    
    for l in lines:
        textob.textLine(l)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True,filename='events.pdf')   

