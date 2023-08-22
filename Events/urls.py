from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('<int:year>/<str:month>/',views.home,name="home"), 
    path('list_event',views.list_event,name="list_event"), 
    path('add_venue',views.add_venue,name='add_venue'),
    path('list_venue',views.list_venue,name='list_venue'),
    path('show_venue/<venue_id>',views.show_venue,name='show_venue'),
    path('search_venue',views.search_venue,name='search_venue'),
    path('update_venue/<venue_id>',views.update_venue,name='update_venue'),
    path('add_event',views.add_event,name='add_event'),
    path('update_event/<event_id>',views.update_event,name='update_event'),
    path('delete_event/<event_id>',views.delete_event,name='delete_event'),
    path('delete_venue/<venue_id>',views.delete_venue,name='delete_venue'),
    path('venue_text',views.venue_text,name='venue_text'),
    path('venue_csv',views.venue_csv,name='venue_csv'),
    path('venue_pdf',views.venue_pdf,name='venue_pdf'),
    path('event_text',views.event_text,name='event_text'),
    path('event_csv',views.event_csv,name='event_csv'),
    path('event_pdf',views.event_pdf,name='event_pdf'),
    path('my_event',views.my_event,name='my_event'),
    path('search_event',views.search_event,name='search_event'),
    path('admin_approval',views.admin_approval,name='admin_approval'),
    path('venue_event/<venue_id>',views.venue_event,name='venue_event'),
    path('show_event/<event_id>',views.show_event,name='show_event'),
]
