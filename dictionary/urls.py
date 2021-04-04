from django.urls import path
from . import views_html

urlpatterns = [
    path('adicionar_palavra/', views_html.addWord, name='add_translate'),
    path('lista_de_palavras/', views_html.listWords, name= 'list_translation'),
    path('lista_de_palavras/<int:id>/', views_html.viewWord, name="view-word"),
    path('lista_de_palavras/<int:id>/editar/<field>', views_html.editWord, name="edit-word"),
]  