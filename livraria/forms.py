from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Autor, Categoria, Editora, Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            'titulo',
            'isbn',
            'pagina',
            'preco',
            'ano_publicacao',
            'sinopse',
            'capa',
            'estoque',
            'disponivel',
            'categoria',
            'editora',
            'autor',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Dom Casmurro'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '978-XX-XXXXX-XX-X'}),
            'paginas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'sinopse': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'capa': forms.FileInput(attrs={'class': 'form-control'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'editora': forms.Select(attrs={'class': 'form-select'}),
            'autores': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        }
        labels = {
            'titulo': 'Título do livro',
            'isbn': 'ISBN',
            'preco': 'Preço (R$)',
            'ano_publicacao': 'Ano de publicação',
            'capa': 'Capa do livro',
        }
        help_texts = {
            'isbn': 'Informe o ISBN com ou sem hífens.',
            'autores': 'Segure Ctrl (ou Cmd) para selecionar múltiplos autores.',
        }

    # ----- Validações customizadas -----

    def clean_isbn(self):
        """Remove hífens e valida tamanho do ISBN."""
        isbn = self.cleaned_data['isbn'].replace('-', '').replace(' ', '')
        if len(isbn) not in (10, 13):
            raise ValidationError('ISBN deve ter 10 ou 13 dígitos.')
        if not isbn.isdigit():
            raise ValidationError('ISBN deve conter apenas números (e hífens).')
        return isbn

    def clean_ano_publicacao(self):
        ano = self.cleaned_data['ano_publicacao']
        ano_atual = datetime.now().year
        if ano < 1450:
            raise ValidationError('Ano inválido (antes da invenção da imprensa).')
        if ano > ano_atual + 1:
            raise ValidationError(f'Ano não pode ser maior que {ano_atual + 1}.')
        return ano

    def clean_preco(self):
        preco = self.cleaned_data['preco']
        if preco <= 0:
            raise ValidationError('O preço deve ser maior que zero.')
        return preco

    def clean(self):
        """Validação envolvendo múltiplos campos."""
        cleaned_data = super().clean()
        estoque = cleaned_data.get('estoque', 0)
        disponivel = cleaned_data.get('disponivel', False)

        if disponivel and estoque == 0:
            self.add_error(
                'estoque',
                'Para marcar como disponível, o estoque deve ser maior que zero.'
            )
        return cleaned_data