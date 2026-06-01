from django.urls import path
from . import views

app_name = 'livros'

urlpatterns = [
    path('', views.home, name='home'),
    path('livros/', views.lista_livros, name='lista'),
    path('livros/novo/', views.criar_livro, name='criar'),
    path('livros/<int:pk>/', views.detalhe_livro, name='detalhe'),
]