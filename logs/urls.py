'''defines url patterns for logs'''
from django.urls import path
from . import views

app_name='logs'
urlpatterns=[
    #home page
    path('',views.index,name='index'),
    #page showing all topics
    path('topics',views.topics,name='topics'),
    #page showing detail for single topic
    path('topics/<int:topic_id>/',views.topic,name='topic'),
    #page for adding a new topic
    path('new_topic/',views.new_topic, name='new_topic'),
    #page for adding new entries
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    #page for editing an entry
    path('edit_entry/<int:entry_id>/', views.edit_entry,name='edit_entry'),
    #page to delete topic
    path('delete_topic/<int:topic_id>/',views.delete_topic, name='delete_topic'),
    #page to delete entry to a topic
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),

]