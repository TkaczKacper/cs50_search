from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:name>', views.entry, name='entry'),
    path('add_page', views.add_page, name='add_page'),
    path('edit_page/<str:name>', views.edit_page, name='edit_page')
]
