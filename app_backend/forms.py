from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
from django import forms as Fform
from .models import  TabWords
class FormWords(Fform.ModelForm):
    class Meta:
        model=TabWords
        fields=[
            'word','word_in_vietnamese'
        ]


from .models import TabClassType
class FormClassType(Fform.ModelForm):
    class Meta:
        model = TabClassType
        fields = [
            'word','class_type','class_in_vietnamese'
        ]
from .models import TabSentence
class FormSentence(Fform.ModelForm):
    class Meta:
        model = TabSentence
        fields = [
            'word','class_type','sentence','sentence_in_vietnamese'
        ]
from .models import TabGrammar
class FormGrammar(Fform.ModelForm):
    class Meta:
        model = TabGrammar
        fields = [
            'word','family_word'
        ]
from .models import TabSynonym
class FormSynonym(Fform.ModelForm):
    class Meta:
        model = TabSynonym
        fields = [
            'word','synonym'
        ]
from .models import TabClassTypeFamilyWord
class FormClassTypeFamilyWord(Fform.ModelForm):
    class Meta:
        model = TabClassTypeFamilyWord
        fields = [
            'family_word',
            'family_word_class_type',
            'family_word_class_type_in_vietnamese'
        ]
from .models import EditClass,EditFamilyWord,EditSentence,EditSynonym,FindClassByWord,FindFamilyWordByWord,FindSentenceByClass,FindSentenceByWord,FindSynonymByWord,DeleteClass,DeleteFamilyWord,DeleteSentence,DeleteSynonym,DeleteWord
class FormEditClass(Fform.ModelForm):
    class Meta:
        model = EditClass
        fields = [
            'enter_old_class_to_be_edited',
            'enter_new_class',
            'enter_new_class_in_Vietnamese'
        ]
class FormEditSentence(Fform.ModelForm):
    class Meta:
        model = EditSentence
        fields = [
            'enter_old_sentence_to_be_edited',
            'enter_new_sentence',
            'enter_new_sentence_in_Vietnamese'
        ]
class FormEditFamilyWord(Fform.ModelForm):
    class Meta:
        model = EditFamilyWord
        fields = [
            'enter_old_family_word_to_be_edited',
            'enter_new_family_word'
        ]
class FormEditSynonym(Fform.ModelForm):
    class Meta:
        model = EditSynonym
        fields = [
            'enter_old_synonym_to_be_edited',
            'enter_new_synonym'
        ]
class FormDeleteWord(Fform.ModelForm):
    class Meta:
        model = DeleteWord
        fields = [
            'enter_word_you_want_to_delete'
        ]
class FormDeleteClass(Fform.ModelForm):
    class Meta:
        model = DeleteClass
        fields = [
            'enter_class_you_want_to_delete'
        ]
class FormDeleteSentence(Fform.ModelForm):
    class Meta:
        model = DeleteSentence
        fields = [
            'enter_sentence_you_want_to_delete'
        ]
class FormDeleteFamilyWord(Fform.ModelForm):
    class Meta:
        model = DeleteFamilyWord
        fields = [
            'enter_family_word_you_want_to_delete'
        ]
class FormDeleteSynonym(Fform.ModelForm):
    class Meta:
        model = DeleteSynonym
        fields = [
            'enter_synonym_you_want_to_delete'
        ]
class FormFindClassByWord(Fform.ModelForm):
    class Meta:
        model = FindClassByWord
        fields = [
            'enter_word_to_find_class'
        ]
class FormFindSentenceByWord(Fform.ModelForm):
    class Meta:
        model = FindSentenceByWord
        fields = [
            'enter_word_to_find_sentence'
        ]
class FormFindFamilyWordByWord(Fform.ModelForm):
    class Meta:
        model = FindFamilyWordByWord
        fields = [
            'enter_word_to_find_family_word'
        ]
class FormFindSynonymByWord(Fform.ModelForm):
    class Meta:
        model = FindSynonymByWord
        fields = [
            'enter_word_to_find_synonym'
        ]
class FormFindSentenceByClass(Fform.ModelForm):
    class Meta:
        model = FindSentenceByClass
        fields = [
            'enter_class_to_find_sentence'
        ]
from .models import InputVocabulary
class FormInputVocabulary(Fform.ModelForm):
    class Meta:
        model = InputVocabulary
        fields = [
            'add_new_word',
            'word_in_Vietnamese',
            'enter_a_sentence',
            'sentence_in_Vietnamese',
            'add_family_word',
            'add_synonym',
            'add_class',
            'class_in_Vietnamese'
        ]
from .models import TranslateText
class FormTranslateText(Fform.ModelForm):
    input_text_to_translate = Fform.CharField(label='Input text to translate:', max_length=5000,
                           widget=Fform.Textarea(attrs={'rows': '10', 'cols': '10'}))
    class Meta:
        model = TranslateText
        fields = ('input_text_to_translate',)