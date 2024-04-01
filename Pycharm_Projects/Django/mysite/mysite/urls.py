"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstapp import views
from django.conf import settings
from django.conf.urls.static import static
from firstapp.views import MyModelListView,MyModelDetailView,MyModelDeleteView,MyModelCreateView,MyModelUpdateView
from firstapp.views import BookListCreateView, BookRetrieveUpdateDestroyView

app_name = 'firstapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.base),
    path('home/',views.home),
    path('one/',views.one),
    path('book/',views.book),
    path('not_found_view/',views.not_found_view),
    path('detail/<int:pk>/', views.detail_view),
    path('home1/',views.home1, name='home1'),
    path('about/',views.about, name='about'),
    path('list/',MyModelListView.as_view(),name='list'),
    path('details/<int:pk>',MyModelDetailView.as_view(),name='details'),
    path('delete/<int:pk>',MyModelDeleteView.as_view()),
    path('create/',MyModelCreateView.as_view()),
    path('update/<int:pk>',MyModelUpdateView.as_view()),
    path('books/',views.books),
    path('bookcreate/', BookListCreateView.as_view(), name='book-list-create'),
    path('bookretrieve/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-destroy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

