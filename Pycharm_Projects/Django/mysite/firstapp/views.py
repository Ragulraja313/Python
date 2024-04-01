import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from rest_framework import generics
from .serializers import BookSerializer

from .models import Books, MyModel
from .form import MyModelForm, BookForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView


class MyModelListView(ListView):
    model = MyModel
    template_name = 'list.html'
    context_object_name = 'my_model_list'


class MyModelDetailView(DetailView):
    model = MyModel
    template_name = 'detail.html'
    context_object_name = 'my_model'


class MyModelCreateView(CreateView):
    model = MyModel
    form_class = MyModelForm
    template_name = 'form.html'
    success_url = '/success/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create MyModel'
        return context


class MyModelDeleteView(DeleteView):
    model = MyModel
    template_name = 'delete.html'
    success_url = reverse_lazy('list')


class MyModelUpdateView(UpdateView):
    model = MyModel
    form_class = MyModelForm
    template_name = 'form.html'
    success_url = '/list/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update MyModel'
        return context


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


def home(request):
    tm = datetime.datetime.now()
    data = {"Date": tm}
    return render(request, 'abc.html', context=data)


def one(request):
    date = datetime.date.today()
    return HttpResponse('<h3><center> Current time: ' + str(date) + '</center></h3>')


def book(request):
    books = Books.objects.all()
    return render(request, 'abc.html', {'books': books})


def not_found_view():
    raise Http404("This page does not exist.")


def base(request):
    return render(request, 'base.html')


def home1(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def detail_view(request, pk):
    my_object = get_object_or_404(MyModel, pk=pk)
    return render(request, 'details.html', {'my_object': my_object})


def books(request):
    if request.method == 'POST': 
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')

    else:
        form = BookForm()

    return render(request, 'books.html', {'form': form})
