from rest_framework import serializers
from .models import WordKokama, WordPortuguese
from .models import PronunciationType, PhrasePortuguese, PhraseKokama


class PhraseKokamaSerializer(serializers.ModelSerializer):
    phrase_portuguese = serializers.SlugRelatedField(read_only=True, slug_field='phrase_portuguese')

    class Meta:
        model = PhraseKokama
        fields = ['phrase_kokama', 'phrase_portuguese']


class WordKokamaSerializer(serializers.ModelSerializer):
    pronunciation_type = serializers.SlugRelatedField(read_only=True, slug_field='pronunciation_type')
    translations = serializers.SlugRelatedField(many=True, read_only=True, slug_field='word_portuguese')
    phrases =  PhraseKokamaSerializer(many=True, read_only=True)

    class Meta:
        model = WordKokama
        fields = ['id', 'word_kokama', 'pronunciation_type', 'phrases', 'translations']


class WordListSerializer(serializers.ModelSerializer):
    translations = serializers.SlugRelatedField(many=True, read_only=True, slug_field='word_portuguese')

    class Meta:
        model = WordKokama
        fields = ['id', 'word_kokama', 'translations']
