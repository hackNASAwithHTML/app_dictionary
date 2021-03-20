from django.db import models

# Create your models here.
class InputVocabulary(models.Model):
    add_new_word = models.CharField(max_length=254,null=True)
    word_in_Vietnamese = models.CharField(max_length=254,null=True)
    enter_a_sentence = models.CharField(max_length=254,null=True)
    sentence_in_Vietnamese = models.CharField(max_length=254,null=True)
    add_family_word = models.CharField(max_length=254,null=True)
    add_synonym = models.CharField(max_length=254,null=True)
    add_class_choice = (
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns", "Pronouns"),
        ("Verbs", "Verbs"),
    )
    add_class = models.CharField(max_length=254, null=True,
                                 choices=add_class_choice,
                                 default='Verbs')
    class_in_Vietnamese_choice = (
        ("Tính từ", "Tính từ"),
        ("Trạng từ", "Trạng từ"),
        ("Giới từ", "Giới từ"),
        ("Danh từ", "Danh từ"),
        ("Đại từ", "Đại từ"),
        ("Động từ", "Động từ"),
    )
    class_in_Vietnamese = models.CharField(max_length=254, null=True,
                                           choices=class_in_Vietnamese_choice,
                                           default='Động từ')
class TabWords(models.Model):
    word = models.CharField(max_length=254, null=True) # word
    word_in_vietnamese = models.CharField(max_length=254, null=True)
    def __str__(self):
        return self.word

class TabClassType(models.Model):
    word = models.CharField(max_length=254,null=True)
    related_word = models.ForeignKey(TabWords, on_delete=models.CASCADE)
    class_type_choice = (
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns","Pronouns"),
        ("Verbs","Verbs"),
    )
    class_type_translated_choice = (
        ("Tính từ", "Tính từ"),
        ("Trạng từ", "Trạng từ"),
        ("Giới từ", "Giới từ"),
        ("Danh từ", "Danh từ"),
        ("Đại từ","Đại từ"),
        ("Động từ","Động từ"),
    )
    class_type = models.CharField(max_length=20, choices=class_type_choice, default='Verbs')
    class_in_vietnamese = models.CharField(max_length=20, choices=class_type_translated_choice, default='Động từ')
    def __str__(self):
        return self.class_type
class TabSentence(models.Model):
    class_for_sentence_choice = (
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns", "Pronouns"),
        ("Verbs", "Verbs"),
    )
    word = models.CharField(max_length=254,null=True)
    class_type = models.CharField(max_length=20,null=True, choices=class_for_sentence_choice, default='Verbs')
    related_class = models.ForeignKey(TabClassType, on_delete=models.CASCADE)
    sentence = models.CharField(max_length=254, null=True)
    sentence_in_vietnamese = models.CharField(max_length=254, null = True)
    def __str__(self):
        return self.sentence
class TabGrammar(models.Model):
    word = models.CharField(max_length=254, null=True)
    related_word = models.ForeignKey(TabWords, on_delete=models.CASCADE)
    family_word = models.CharField(max_length=254,null=True)
    def __str__(self):
        return self.family_word
class TabClassTypeFamilyWord(models.Model):
    family_word = models.CharField(max_length=254, null=True)
    related_family_word = models.ForeignKey(TabGrammar, on_delete=models.CASCADE)
    family_word_class_type_choice =(
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns","Pronouns"),
        ("Verbs","Verbs"),
    )
    family_word_class_type = models.CharField(max_length=20,null=True, choices=family_word_class_type_choice, default='Verbs')
    family_word_class_type_translated_choice = (
        ("Tính từ", "Tính từ"),
        ("Trạng từ", "Trạng từ"),
        ("Giới từ", "Giới từ"),
        ("Danh từ", "Danh từ"),
        ("Đại từ","Đại từ"),
        ("Động từ","Động từ"),
    )
    family_word_class_type_in_vietnamese = models.CharField(max_length=20, choices=family_word_class_type_translated_choice, default='Động từ')
    def __str__(self):
        return self.family_word_class_type
class TabSynonym(models.Model):
    word = models.CharField(max_length=254, null=True)
    related_word = models.ForeignKey(TabWords, on_delete=models.CASCADE)
    synonym = models.CharField(max_length=254,null=True)
    def __str__(self):
        return self.synonym
class EditClass(models.Model):
    enter_old_class_to_be_edited_choice = (
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns", "Pronouns"),
        ("Verbs", "Verbs"),
    )
    enter_old_class_to_be_edited = models.CharField(max_length=20, null=True,
                                                    choices=enter_old_class_to_be_edited_choice,
                                                    default='Verbs')
    enter_new_class_choice = (
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns", "Pronouns"),
        ("Verbs", "Verbs"),
    )
    enter_new_class = models.CharField(max_length=20, null=True, choices=enter_new_class_choice,
                                              default='Verbs')
    enter_new_class_in_Vietnamese_choice = (
        ("Tính từ", "Tính từ"),
        ("Trạng từ", "Trạng từ"),
        ("Giới từ", "Giới từ"),
        ("Danh từ", "Danh từ"),
        ("Đại từ", "Đại từ"),
        ("Động từ", "Động từ"),
    )
    enter_new_class_in_Vietnamese = models.CharField(max_length=20,
                                                    choices=enter_new_class_in_Vietnamese_choice,
                                                default='Động từ')
class EditSentence(models.Model):
    enter_class_to_find_sentence_choice = (
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns", "Pronouns"),
        ("Verbs", "Verbs"),
    )
    enter_class_to_find_sentence = models.CharField(max_length=20,null=True, choices=enter_class_to_find_sentence_choice,default='Verbs')
    enter_old_sentence_to_be_edited = models.CharField(max_length=254,null=True)
    enter_new_sentence = models.CharField(max_length=254,null=True)
    enter_new_sentence_in_Vietnamese = models.CharField(max_length=254,null=True)
class EditFamilyWord(models.Model):
    enter_old_family_word_to_be_edited = models.CharField(max_length=254,null=True)
    enter_new_family_word = models.CharField(max_length=254,null=True)
class EditSynonym(models.Model):
    enter_old_synonym_to_be_edited = models.CharField(max_length=254,null=True)
    enter_new_synonym = models.CharField(max_length=254,null=True)
class DeleteWord(models.Model):
    enter_word_you_want_to_delete = models.CharField(max_length=254,null=True)
class DeleteClass(models.Model):
    enter_class_you_want_to_delete_choice=(
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns", "Pronouns"),
        ("Verbs", "Verbs"),
    )
    enter_class_you_want_to_delete = models.CharField(max_length=254,null=True,choices=enter_class_you_want_to_delete_choice,
                                                      default='Verbs')
class DeleteSentence(models.Model):
    enter_sentence_you_want_to_delete = models.CharField(max_length=254,null=True)
class DeleteFamilyWord(models.Model):
    enter_family_word_you_want_to_delete = models.CharField(max_length=254,null=True)
class DeleteSynonym(models.Model):
    enter_synonym_you_want_to_delete = models.CharField(max_length=254,null=True)
class FindClassByWord(models.Model):
    enter_word_to_find_class = models.CharField(max_length=254,null=True)
class FindSentenceByWord(models.Model):
    enter_word_to_find_sentence = models.CharField(max_length=254,null=True)
class FindFamilyWordByWord(models.Model):
    enter_word_to_find_family_word = models.CharField(max_length=254,null=True)
class FindSynonymByWord(models.Model):
    enter_word_to_find_synonym = models.CharField(max_length=254,null=True)
class FindSentenceByClass(models.Model):
    enter_class_to_find_sentence_choice =(
        ("Adjectives", "Adjectives"),
        ("Adverbs", "Adverbs"),
        ("Prepositions", "Prepositions"),
        ("Noun", "Noun"),
        ("Pronouns", "Pronouns"),
        ("Verbs", "Verbs"),
            )
    enter_class_to_find_sentence = models.CharField(max_length=254,null=True,choices=enter_class_to_find_sentence_choice,
                                                    default='Verbs')
class TranslateText(models.Model):
    input_text_to_translate = models.CharField(max_length=254,
                                               null=True)

