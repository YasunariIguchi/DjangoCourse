from django.urls import path
from .views import IndexView, HomeView, BookDetailView, BookListView, BookCreateView, BookUpdateView, BookDeleteView, BookFormView, BookRedirectView
from django.views.generic.base import RedirectView
#from django.views.generic.base import TemplateView

app_name = "store"

urlpatterns = [
    path("index/", IndexView.as_view(), name="index"),
    path("home/<str:name>", HomeView.as_view(), name="home"),
    path("detail_book/<int:pk>", BookDetailView.as_view(), name="detail_book"),
    path("list_books/", BookListView.as_view(), name="list_books"),
    path("add_book/", BookCreateView.as_view(), name="add_book"),
    path("update_book/<int:pk>", BookUpdateView.as_view(), name="update_book"),
    path("delete_book/<int:pk>", BookDeleteView.as_view(), name="delete_book"),
    path("book_form/", BookFormView.as_view(), name="book_form"),
    path("google/", RedirectView.as_view(url="https:/google.com"), name="google"),
    path("googl2/", BookRedirectView.as_view(), name="google2"),
    
]