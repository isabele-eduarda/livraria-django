from django.shortcuts import render, get_object_or_404
from .models import Livro
from django.core.paginator import Paginator

from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import LivroForm

def home(request):
    """Página inicial — exibe os 6 livros mais recentes."""
    livros = Livro.objects.filter(disponivel=True).order_by('-criado_em')[:6]
    contexto = {'livros': livros}
    return render(request, 'livraria/home.html', contexto)


def lista_livros(request):
    """Lista todos os livros disponíveis com busca."""
    busca = request.GET.get('q', '')
    livros = Livro.objects.filter(disponivel=True)

    if busca:
        livros = livros.filter(titulo__icontains=busca)

    paginator = Paginator(livros, 6)  # 6 livros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'page_obj': page_obj,
        'busca': busca,
    }
    return render(request, 'livraria/lista.html', contexto)

def detalhe_livro(request, pk):
    """Exibe os detalhes de um livro específico."""
    livro = get_object_or_404(Livro, pk=pk, disponivel=True)
    contexto = {'livro': livro}
    return render(request, 'livraria/detalhe.html', contexto)

def criar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save()
            messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso!')
            return redirect('livros:detalhe', pk=livro.pk)
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = LivroForm()

    return render(request, 'livraria/form.html', {
        'form': form,
        'titulo': 'Cadastrar Livro',
    })