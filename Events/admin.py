from django.contrib import admin
from .models import Venue
from .models import NewappUser
from .models import Events
from django.contrib.auth.models import Group

#admin.site.register(Venue)
admin.site.register(NewappUser)

#admin.site.register(Events)
@admin.register(Venue)

class VenueAdmin(admin.ModelAdmin):
    list_display=('name','address','phonenumber')
    ordering = ('name',) 
    search_fields=('name','address')

#admin.site.register(Venue,VenueAdmin)
@admin.register(Events)

class EventAdmin(admin.ModelAdmin):
    fields = (('name','venue'),'event_date','description','manager','attendees','approved')
    list_display = ('name','event_date','venue')
    list_filter = ('event_date','venue')
    ordering = ('-event_date',)

#remove groups
admin.site.unregister(Group)