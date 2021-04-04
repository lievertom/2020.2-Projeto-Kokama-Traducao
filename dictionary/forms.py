from django import forms
from django.core.validators import RegexValidator
from .models import WordKokama, WordPortuguese, PhraseKokama, PhrasePortuguese

class AddNewPortugueseForm(forms.Form):
    portuguese_word = forms.CharField(
        label='portuguese_word',
        error_messages={'required': 'Preencha este campo.'}
    )

class AddNewPhraseForm(forms.Form):
    phrase_kokama = forms.RegexField(
        label='phrase_kokama', 
        regex='.*<.+>.*',
        error_messages={'invalid': ("A frase deve conter uma palavra destacada com <>. Ex: <panara>.")},
    )
    
    phrase_portuguese = forms.RegexField(
        label='phrase_portuguese', 
        regex='.*<.+>.*',
        error_messages={'invalid': ("A frase deve conter uma palavra destacada com <>. Ex: <banana>.")},
    
    )



PRONUNCIATION_CHOICES =(
    ("1", "Geral"),
    ("2", "Feminino"),
    ("3", "Masculino"),
)

class NewWordForm(forms.Form):

    kokama_word = forms.CharField(
        label='kokama_word',
        error_messages={'required': 'Preencha este campo.'}
    )

    portuguese_word = forms.CharField(
        label='portuguese_word',
        error_messages={'required': 'Preencha este campo.'}
    )
    
    type_pronunciation = forms.ChoiceField(
        choices = PRONUNCIATION_CHOICES,
        label='type_pronunciation',
    )

    phrase_kokama = forms.RegexField(
        label='phrase_kokama', 
        regex='.*<.+>.*',
        error_messages={'invalid': ("A frase deve conter uma palavra destacada com <>. Ex: <panara>.")},
    )
    
    phrase_portuguese = forms.RegexField(
        label='phrase_portuguese', 
        regex='.*<.+>.*',
        error_messages={'invalid': ("A frase deve conter uma palavra destacada com <>. Ex: <banana>.")},
    
    )

    
  