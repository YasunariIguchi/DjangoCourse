from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.base import (
    View, TemplateView, RedirectView 
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from . import forms
from datetime import datetime
from .models import Book
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        book_form = forms.BookForm()
        return render(request, "index.html", context={"book_form": book_form})
    
    def post(self, request, *args, **kwargs):
        book_form = forms.BookForm(request.POST or None)
        if book_form.is_valid():
            book_form.save()
        return render(request, "index.html", context={"book_form": book_form})
    
class HomeView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = kwargs.get("name")
        context["time"] = datetime.now()
        return context
    

class BookDetailView(DetailView):
    model = Book
    template_name = "book.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["osaka"] = "sakuranomiya"
        return context


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    
    def get_queryset(self) -> QuerySet[Any]:
        qs = super(BookListView, self).get_queryset().order_by("-price")
        return qs
    
class BookCreateView(CreateView):
    model = Book
    fields = ["name", "description", "price"]
    template_name = "add_book.html"
    success_url = reverse_lazy("store:list_books")
    
    def form_valid(self,form):
        form.instance.create_at = datetime.now()
        form.instance.update_at = datetime.now()
        return super().form_valid(form)
    
    def get_initial(self, **kwargs) -> dict[str, Any]:
        initial = super().get_initial(**kwargs)
        initial["name"] = "sample"
        return initial

class BookUpdateView(SuccessMessageMixin, UpdateView):
    model = Book
    template_name = "update_book.html"
    form_class = forms.BookUpdateForm
    success_message = "更新に成功したお"
    
    def get_success_url(self) -> str:
        # print(self.get_object)
        return reverse_lazy("store:update_book", kwargs ={"pk": self.object.id })
    
    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return cleaned_data.get("name") + "を更新したお"

class BookDeleteView(DeleteView):
    model = Book
    template_name = "delete_book.html"
    success_url = reverse_lazy("store:list_books")
    

class BookFormView(FormView):
    template_name = "form_book.html"
    form_class = forms.BookForm
    success_url = reverse_lazy("store:list_books")
    
    def form_valid(self,form):
        if form.is_valid():
            form.instance.create_at = datetime.now()
            form.instance.update_at = datetime.now()
            form.save()
        return super().form_valid(form)

class BookRedirectView(RedirectView):
    url = "https://google.com"