from rest_framework import viewsets, mixins
from .serializers import WordKokamaSerializer, PhraseKokamaSerializer, WordListSerializer
from .models import WordKokama, WordPortuguese, PhraseKokama, PhrasePortuguese, Translate, PronunciationType
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)

def delete_word_kokama(word_kokama):
    translates = Translate.objects.filter(word_kokama=word_kokama)

    for translate in translates:
        translate.word_portuguese.delete()
    
    pharses_kokama = PhraseKokama.objects.filter(word_kokama=word_kokama)

    for pharse_kokama in pharses_kokama:
        pharse_kokama.phrase_portuguese.delete()

    word_kokama.delete()



class KokamaViewSet(viewsets.ModelViewSet):
    queryset = WordKokama.objects.all()
    serializer_class = WordKokamaSerializer

class WordListViewSet(viewsets.ModelViewSet):
    queryset = WordKokama.objects.all().order_by('-id')
    serializer_class = WordListSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            word_kokama = self.get_object()
            delete_word_kokama(word_kokama)
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=HTTP_204_NO_CONTENT)


class PhrasesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PhraseKokama.objects.all()
    serializer_class = PhraseKokamaSerializer

@api_view(["POST"])
def add_translate(request, id):
    if id:
        word_kokama = WordKokama.objects.get(id=id) # Conferir se existe (try)
        if word_kokama.word_kokama != request.POST.get('word_kokama') and WordKokama.objects.filter(word_kokama=request.POST.get('word_kokama')).first():
            return Response(
                {'error': 'Palavra Kokama já cadastrada.'},
                status=HTTP_400_BAD_REQUEST,
            )

        delete_word_kokama(word_kokama)
    
    word_kokama, created = WordKokama.objects.get_or_create(
        word_kokama=request.POST.get('word_kokama'),
        pronunciation_type=PronunciationType.objects.get(
            id=request.POST.get('pronunciation_choises')
        ),
    )
    if not created:
        return Response(
            {'error': 'Palavra Kokama já cadastrada.'},
            status=HTTP_400_BAD_REQUEST,
        )

    word_kokama.save()

    word_portuguese_total_forms = request.POST.get('word-portuguese-TOTAL_FORMS')
    for i in range(0, int(word_portuguese_total_forms)):
        word_portuguese = WordPortuguese.objects.create(
            word_portuguese=request.POST.get('word-portuguese-{}-word_portuguese'.format(i))
        )
        word_portuguese.save()
        translation = Translate.objects.create(
            word_kokama=word_kokama,
            word_portuguese=word_portuguese
        )
        translation.save()


    phrase_total_forms = request.POST.get('phrase-TOTAL_FORMS')
    for i in range(0, int(phrase_total_forms)):
        phrase_portuguese = PhrasePortuguese.objects.create(
            phrase_portuguese=request.POST.get('phrase-{}-phrase_portuguese'.format(i))
        )
        phrase_portuguese.save()

        phrase_kokama = PhraseKokama.objects.create(
            phrase_kokama=request.POST.get('phrase-{}-phrase_kokama'.format(i)),
            word_kokama=word_kokama,
            phrase_portuguese=phrase_portuguese,
        )
        phrase_kokama.save()

    return Response(status=HTTP_200_OK)

    