from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
import hashlib
from .models import TabSynonym, TabGrammar, TabSentence, TabClassType, TabWords, TabClassTypeFamilyWord
from .forms import FormWords, FormClassType, FormGrammar, FormSentence, FormSynonym, FormClassTypeFamilyWord
from .forms import FormEditClass,FormEditFamilyWord,FormEditSentence,FormEditSynonym
from .forms import FormFindClassByWord,FormFindFamilyWordByWord,FormFindSentenceByClass,FormFindSentenceByWord,FormFindSynonymByWord
from .forms import FormDeleteClass,FormDeleteFamilyWord,FormDeleteSentence,FormDeleteSynonym,FormDeleteWord
from .forms import FormInputVocabulary
from .forms import FormTranslateText
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
def convertTuple(tup):
    str =  ''.join(tup)
    return str
# Create your views here.
def signup_function(request):
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['password'].encode())
        updated_password = hashed_password.hexdigest()
        user = User.objects.create_user(data['username'],'',updated_password)
        if user:
            return render(request,'520-templates/520-blog.html')
    return render(request,'520-templates/make-account.html')
def login_function(request):
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['password'].encode())
        updated_password = hashed_password.hexdigest()
        user = authenticate(username=data['username'],password=updated_password)
        if user is not None:
            login(request, user)
            return render(request,'520-templates/520-blog.html')
        else:
            return HttpResponse('login 0')
    return render(request,'520-templates/login.html')

def logout_session(request):
    logout(request)
    return redirect('blog')
# Create your views here.
def home(request):
    w_form = FormWords()
    ct_form = FormClassType()
    s_form = FormSentence()
    g_form = FormGrammar()
    sy_form = FormSynonym()
    g_c_form = FormClassTypeFamilyWord()
    print("---")
    print(w_form)
    print("---")
    print(ct_form)
    print("---")
    print(s_form)
    print("---")
    print(g_form)
    print("---")
    print(sy_form)
    print("---")
    print(g_c_form)
    return render(request,"main.html")
def search_word(request):
    if request.method == "GET":
        search_item = request.GET.get('keyword')
        word_result = TabWords.objects.filter(word=search_item)
        class_result = TabClassType.objects.filter(word=search_item)
        sentence_result = TabSentence.objects.filter(word=search_item)
        grammar_result = TabGrammar.objects.filter(word=search_item)
        synonym_result = TabSynonym.objects.filter(word=search_item)
        try:
            search_family_word = (TabGrammar.objects.values_list('family_word').filter(word=search_item))[1]
        except IndexError:
            pass
        temp = []
        try:
            queried_family_word = (TabGrammar.objects.values_list('family_word').filter(word=search_item))[0]
        except IndexError:
            pass
        try:
            queried_family_word = convertTuple(queried_family_word)
        except UnboundLocalError as error:
            queried_family_word = None
        try:
            queried_id_specific = str((TabGrammar.objects.values_list('id').get(family_word=queried_family_word,
                                                                                word=search_item))[0])
        except TabGrammar.DoesNotExist as error:
            queried_id_specific = None
        try:
            grammar_queried_id = str(
                (TabGrammar.objects.values_list('related_word').get(id=queried_id_specific, word=search_item))[0])
        except TabGrammar.DoesNotExist:
            grammar_queried_id = None
        n = TabGrammar.objects.filter(related_word=grammar_queried_id).count()
        for x in range(0,n):
            search_family_word_temped = (TabGrammar.objects.values_list('family_word').filter(word=search_item))[x]
            temp.append(search_family_word_temped)
        temp_data = []
        for x in range(0,n):
            string_chain = "".join(str(d) for d in temp[x])
            temp_data.append(string_chain)
        try:
            search_family_word = convertTuple(search_family_word)
        except UnboundLocalError as error:
            search_family_word = None
        class_family_word = TabClassTypeFamilyWord.objects.filter(family_word=search_family_word)
        array_item = []
        array_item.append(search_item)
        return render(request,"520-templates/520-search-result.html",{'word_result':word_result,
                                              'grammar_result':grammar_result,
                                              'class_result':class_result,
                                              'sentence_result':sentence_result,
                                              'synonym_result':synonym_result,
                                              'itemlist':array_item,
                                              'class_family_result':class_family_word,
                                              'temp_data':temp_data})
def add_word(request):
    rendered_inputvocabulary = FormInputVocabulary()
    if request.method == "POST":
        data = request.POST
        update_tabWords = TabWords.objects.create(word_origin=data['word_origin'],
                                                  word_translated=data['word_translated'])
        queried_id = str((TabWords.objects.values_list('id').get(word_origin=data['word_origin']))[0])
        update_tabClassType = TabClassType.objects.create(word_for_class=data['word_origin'],
                                                          class_type=data['class_type'],
                                                          class_translated=data['class_translated'],
                                                          word_class_id=queried_id)
        queried_class_id = str((TabClassType.objects.values_list('id').get(word_class_id=queried_id))[0])
        update_tabSentence = TabSentence.objects.create(class_for_sentence=data['class_type'],
                                                        sentence=data['sentence'],
                                                        sentence_translated=data['sentence_translated'],
                                                        class_sentence_id=queried_class_id,
                                                        word_for_sentence=data['word_origin'])
        update_tabGrammar = TabGrammar.objects.create(word_for_grammar=data['word_origin'],
                                                      family_word=data['family_word'],
                                                      word_grammar_id=queried_id)
        update_tabSynonym = TabSynonym.objects.create(word_for_synonym=data['word_origin'],
                                                      synonym=data['synonym'],
                                                      word_synonym_id=queried_id)
        if update_tabWords and update_tabClassType and update_tabSentence and update_tabGrammar and update_tabSynonym:
            return HttpResponse("200")
        else:
            return HttpResponse("404")
    return render(request,"add_vocabularies.html",
                  {"inputvocabulary":rendered_inputvocabulary})

def add_family_word(request):
    g_form = FormGrammar()
    if request.method == "POST":
        data = request.POST
        queried_id = str((TabWords.objects.values_list('id').get(word_origin=data['word_for_grammar']))[0])
        updateFamilyWord = TabGrammar.objects.create(word_for_grammar=data['word_for_grammar'],
                                                     family_word=data['family_word'],
                                                     word_grammar_id=queried_id)
        if updateFamilyWord:
            return HttpResponse("200")
        else:
            return HttpResponse("404")
    return render(request,"add_family_word.html",{"g_form":g_form})
def add_class_family_word(request):
    g_c_form = FormClassTypeFamilyWord()
    if request.method == "POST":
        data = request.POST
        queried_id = str((TabGrammar.objects.values_list('id').get(family_word=data['family_word_for_class']))[0])
        updateClassFamilyWord = TabClassTypeFamilyWord.objects.create(
            family_word_for_class=data['family_word_for_class'],
            family_word_class_type=data['family_word_class_type'],
            family_word_class_type_translated=data['family_word_class_type_translated'],
            family_word_class_id = queried_id
        )
        if updateClassFamilyWord:
            return HttpResponse("200")
        else:
            return HttpResponse("404")
    return render(request,"add_class_family_word.html",{"g_c_form":g_c_form})
def add_synonym(request):
    sy_form = FormSynonym()
    if request.method == "POST":
        data = request.POST
        queried_id = str((TabWords.objects.values_list('id').get(word_origin=data['word_for_synonym']))[0])
        updateSynonym = TabSynonym.objects.create(
            word_for_synonym = data['word_for_synonym'],
            synonym = data['synonym'],
            word_synonym_id = queried_id
        )
        if updateSynonym:
            return HttpResponse("200")
        else:
            return HttpResponse("404")
    return render(request, "add_synonym.html", {"sy_form": sy_form})
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
def create_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    return response
class rendered_soup:
    def __init__(self,mySoup,myDriver,myURL):
        self.mySoup = mySoup
        self.myDriver = myDriver
        self.myURL = myURL
    def fetching(self):
        try:
            myList = self.mySoup.find('span', jsname='W297wb').text
        except AttributeError:
            print("!! Error detected !!")
            print("Rolling back to previous execution...")
            self.myDriver.quit()
            self.myDriver = webdriver.Chrome(ChromeDriverManager().install())
            self.myDriver.get(self.myURL)
            self.mySoup = BeautifulSoup(self.myDriver.page_source,'html.parser')
            initialized_mySoup = rendered_soup(self.mySoup, self.myDriver, self.myURL)
            myList = initialized_mySoup.fetching()
            print("result = ",myList)
        return myList
class Translate:
    def __init__(self,translate_text):
        self.translate_text = translate_text
    def translate_item(self):
        print("- Entering translate state -")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = "https://translate.google.com/#view=home&op=translate&sl=en&tl=vi&text=" + self.translate_text
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        temp = []
        initialized_mySoup = rendered_soup(soup,driver,url)
        list_result = initialized_mySoup.fetching()
        temp.append(list_result)
        driver.quit()
        for x in range(0,1):
            temp_string = "".join(str(d) for d in temp[x])
            return temp_string
def csv_adding_word(request):
    path = "C:\\Users\HoangChuong\RatingAppProject\\venv\Scripts\\app_dictionary\\"
    with open(path+"update-word.csv","r",newline='') as my_item:
        reading_items = csv.reader(my_item)
        for item in reading_items:
            initialized_word = Translate(item[0])
            csv_word_translated = initialized_word.translate_item()
            initialized_class = Translate(item[1])
            csv_class_translated = initialized_class.translate_item()
            initialized_sentence = Translate(item[2])
            csv_sentences_translated = initialized_sentence.translate_item()
            updateWord = TabWords.objects.create(word=item[0],
                                                 word_in_vietnamese=csv_word_translated)
            word_queried_id = str((TabWords.objects.values_list('id').get(word=item[0]))[0])
            updateClass = TabClassType.objects.create(class_type=item[1],
                                                      class_in_vietnamese=csv_class_translated,
                                                      related_word_id=word_queried_id,
                                                      word=item[0])
            class_queried_id = str((TabClassType.objects.values_list('id').get(word=item[0]))[0])
            updateSentence = TabSentence.objects.create(class_type=item[1],
                                                        sentence=item[2],
                                                        sentence_in_vietnamese=csv_sentences_translated,
                                                        related_class_id=class_queried_id,
                                                        word=item[0])
        if updateWord and updateClass and updateSentence:
            return redirect('home')
    return HttpResponse('0')
def see_words_list(request):
    n = TabWords.objects.count()
    temp = []
    temp.append(n)
    total_words = TabWords.objects.all()
    return render(request,'see_words_list.html',{'temp':temp,'total_words':total_words})
import socket
def highway_blog(request):
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")
    return render(request,'520-templates/520-blog.html')
def add_items_selection(request):
    return render(request,"520-templates/520-add-items-selection.html")
def edit_items_selection(request):
    return render(request,"520-templates/520-edit-items-selection.html")
def delete_items_selection(request):
    return render(request,"520-templates/520-delete-items-selection.html")
def add_vocabulary(request):
    rendered_inputvocabulary = FormInputVocabulary()
    if request.method == "POST":
        data = request.POST
        update_tabWords = TabWords.objects.create(word=data['add_new_word'],
                                                  word_in_vietnamese=data['word_in_Vietnamese'])

        queried_id = str((TabWords.objects.values_list('id').get(word=data['add_new_word']))[0])
        print("id word: ",queried_id)
        update_tabClassType = TabClassType.objects.create(word=data['add_new_word'],
                                                          class_type=data['add_class'],
                                                          class_in_vietnamese=data['class_in_Vietnamese'],
                                                          related_word_id=queried_id)
        queried_class_id = str((TabClassType.objects.values_list('id').get(related_word_id=queried_id))[0])
        print("id class: ",queried_class_id)
        update_tabSentence = TabSentence.objects.create(class_type=data['add_class'],
                                                        sentence=data['enter_a_sentence'],
                                                        sentence_in_vietnamese=data['sentence_in_Vietnamese'],
                                                        related_class_id=queried_class_id,
                                                        word=data['add_new_word'])
        update_tabGrammar = TabGrammar.objects.create(word=data['add_new_word'],
                                                      family_word=data['add_family_word'],
                                                      related_word_id=queried_id)
        update_tabSynonym = TabSynonym.objects.create(word=data['add_new_word'],
                                                      synonym=data['add_synonym'],
                                                      related_word_id=queried_id)
        if update_tabWords and update_tabClassType and update_tabSentence and update_tabGrammar and update_tabSynonym:
            return HttpResponse("200")
        else:
            return HttpResponse("404")
    return render(request,'520-templates/520-add-vocabulary.html',
                  {"inputvocabulary":rendered_inputvocabulary})
def add_class(request):
    text = FormTranslateText()
    print(text)
    ct_form = FormClassType()
    if request.method == "POST":
        data = request.POST
        queried_id = str((TabWords.objects.values_list('id').get(word=data['word']))[0])
        update_tabClassType = TabClassType.objects.create(word=data['word'],
                                                          class_type=data['class_type'],
                                                          class_in_vietnamese=data['class_in_vietnamese'],
                                                          related_word_id=queried_id)
        if update_tabClassType:
            return HttpResponse("200")
        else:
            return HttpResponse("404")
    return render(request,'520-templates/520-add-class.html',{"ct_form":ct_form,
                                                              "text":text})
def add_sentence(request):
    s_form = FormSentence()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabClassType.objects.values_list('id').get(word=data['word'], class_type=data['class_type']))[0])
        except TabClassType.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('The item you entered does not exist.')
        updateSentence = TabSentence.objects.create(class_type=data['class_type'],
                                                           sentence=data['sentence'],
                                                    sentence_in_vietnamese=data['sentence_in_vietnamese'],
                                                    related_class_id=queried_id,
                                                    word=data['word'])
        if updateSentence:
            return HttpResponse("200")
        else:
            return HttpResponse("404")
    return render(request,'520-templates/520-add-sentence.html',{"s_form":s_form})
def edit_class(request):
    rendered_editclass = FormEditClass()
    rendered_findclass = FormFindClassByWord
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabWords.objects.values_list('id').get(word=data['enter_word_to_find_class']))[0])
        except TabWords.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        related_class_properties = TabClassType.objects.get(related_word_id=queried_id,class_type=data['enter_old_class_to_be_edited'])
        related_class_properties.class_type = data['enter_new_class']
        related_class_properties.class_in_vietnamese = data['enter_new_class_in_Vietnamese']
        related_class_properties.save()
        return HttpResponse('200')
    return render(request,'520-templates/520-edit-class.html',{"editclass":rendered_editclass,
                                                               "findclass":rendered_findclass})
def edit_sentence(request):
    rendered_findsentence = FormFindSentenceByWord()
    rendered_editsentence = FormEditSentence()
    rendered_findsentence_additional = FormFindSentenceByClass()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabClassType.objects.values_list('id').get(class_type=data['enter_class_to_find_sentence'],
                                                                         word=data['enter_word_to_find_sentence']))[0])
        except TabClassType.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        related_sentence_properties = TabSentence.objects.get(related_class_id=queried_id,sentence=data['enter_old_sentence_to_be_edited'])
        related_sentence_properties.sentence = data['enter_new_sentence']
        related_sentence_properties.sentence_in_vietnamese = data['enter_new_sentence_in_Vietnamese']
        related_sentence_properties.save()
        return HttpResponse('200')
    return render(request, '520-templates/520-edit-sentence.html', {"findsentence": rendered_findsentence,
                                                                    "editsentence":rendered_editsentence,
                                                                    "findsentence_additional":rendered_findsentence_additional})
def edit_family_word(request):
    rendered_findfamilyword = FormFindFamilyWordByWord()
    rendered_editfamilyword = FormEditFamilyWord()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabWords.objects.values_list('id').get(word=data['enter_word_to_find_family_word']))[0])
        except TabWords.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        related_family_word_properties = TabGrammar.objects.get(related_word_id=queried_id,family_word=data['enter_old_family_word_to_be_edited'])
        related_family_word_properties.family_word = data['enter_new_family_word']
        related_family_word_properties.save()
        return HttpResponse('200')
    return render(request,'520-templates/520-edit-family-word.html',{"findfamilyword":rendered_findfamilyword,
                                                                     "editfamilyword":rendered_editfamilyword})
def edit_synonym(request):
    rendered_findsynonym = FormFindSynonymByWord()
    rendered_editsynonym = FormEditSynonym()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabWords.objects.values_list('id').get(word=data['enter_word_to_find_synonym']))[0])
        except TabWords.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        try:
            related_synonym_properties = TabSynonym.objects.get(related_word_id=queried_id,
                                                                synonym=data['enter_old_synonym_to_be_edited'])
        except TabSynonym.DoesNotExist as error:
            related_synonym_properties = None
        if related_synonym_properties == None:
            return HttpResponse('Double 404')
        related_synonym_properties.synonym = data['enter_new_synonym']
        related_synonym_properties.save()
        return HttpResponse('200')
    return render(request,"520-templates/520-edit-synonym.html",{"findsynonym":rendered_findsynonym,
                                                                 "editsynonym":rendered_editsynonym})
def delete_items(request):
    return render(request,'520-templates/520-delete-items.html')
def delete_vocabulary(request):
    rendered_deleteword = FormDeleteWord()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabWords.objects.values_list('id').get(word=data['enter_word_you_want_to_delete']))[0])
        except TabWords.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        del_word = TabWords.objects.get(pk=queried_id)
        del_word.delete()
        return HttpResponse("word has been deleted.")
    return render(request,'520-templates/520-delete-vocabulary.html',{"deleteword":rendered_deleteword})
def delete_class(request):
    rendered_findclass = FormFindClassByWord
    rendered_deleteclass = FormDeleteClass()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabClassType.objects.values_list('id').get(word=data['enter_word_to_find_class'],class_type=data['enter_class_you_want_to_delete']))[0])
        except TabClassType.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        del_class = TabClassType.objects.get(pk=queried_id)
        del_class.delete()
        return HttpResponse("200")
    return render(request,'520-templates/520-delete-class.html',
                  {"findclass":rendered_findclass,
                   "deleteclass":rendered_deleteclass})
def delete_sentence(request):
    rendered_findsentence = FormFindSentenceByWord()
    rendered_deletesentence = FormDeleteSentence()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabSentence.objects.values_list('id').get(word=data['enter_word_to_find_sentence'],sentence=data['enter_sentence_you_want_to_delete']))[0])
        except TabSentence.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        del_sentence = TabSentence.objects.get(pk=queried_id)
        del_sentence.delete()
        return HttpResponse("200")
    return render(request,'520-templates/520-delete-sentence.html',{"findsentence":rendered_findsentence,
                                                                    "deletesentence":rendered_deletesentence})
def delete_family_word(request):
    rendered_findfamilyword = FormFindFamilyWordByWord()
    rendered_deletefamilyword = FormDeleteFamilyWord()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabGrammar.objects.values_list('id').get(word=data['enter_word_to_find_family_word'],
                                                                       family_word=data['enter_family_word_you_want_to_delete']))[0])
        except TabGrammar.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        del_family_word = TabGrammar.objects.get(pk = queried_id)
        del_family_word.delete()
        return HttpResponse("200")
    return render(request,'520-templates/520-delete-family-word.html',
                  {"findfamilyword":rendered_findfamilyword,
                   "deletefamilyword":rendered_deletefamilyword})
def delete_synonym(request):
    rendered_findsynonym = FormFindSynonymByWord()
    rendered_deletesynonym = FormDeleteSynonym()
    if request.method == "POST":
        data = request.POST
        try:
            queried_id = str((TabSynonym.objects.values_list('id').get(word=data['enter_word_to_find_synonym'],
                                                                       synonym=data['enter_synonym_you_want_to_delete']))[0])
        except TabSynonym.DoesNotExist as error:
            queried_id = None
        if queried_id == None:
            return HttpResponse('404')
        del_synonym = TabSynonym.objects.get(pk=queried_id)
        del_synonym.delete()
        return HttpResponse("200")
    return render(request,'520-templates/520-delete-synonym.html',
                  {"findsynonym":rendered_findsynonym,
                   "deletesynonym":rendered_deletesynonym})
def text_translating(request):
    if request.method == "POST":
        data = request.POST
        search_text = data['keyword']
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = "https://translate.google.com/#view=home&op=translate&sl=en&tl=vi&text="+search_text
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print("soup is ")
        print(soup)
        temp = []
        list = soup.find('span', class_='tlid-translation translation').text
        temp.append(list)
        for x in range(0,1):
            temp_string = "".join(str(d) for d in temp[x])
        driver.quit()
        list_search_text = []
        list_search_text.append(search_text)
        return render(request,"text_translating_result.html",{'list_search_text':list_search_text,'temp':temp})
    return render(request,"text_translating.html")
def translate_text(request):
    rendered_text = FormTranslateText()
    print(rendered_text)
    if request.method == "POST":
        data = request.POST
        search_text = data['input_text_to_translate']
        initialized_text = Translate(search_text)
        translated_result = initialized_text.translate_item()
        return render(request, "520-templates/520-translate-text.html",
                          {"rendered_text": rendered_text, "translated_text": translated_result,
                           "entered_text": search_text})
    return render(request,"520-templates/520-translate-text.html",{"rendered_text":rendered_text})
def see_word_list(request):
    queried_words = TabWords.objects.all().filter()
    print("1-")
    print(queried_words)
    queried_words = list(queried_words)
    print("2-")
    print(queried_words)
    queried_words = str(queried_words)
    print("3-")
    print(queried_words)
    n = TabWords.objects.count()
    print("n = ",n)
    print("type is ",type(n))
    temp = []
    temp.append(n)
    total_words = TabWords.objects.all()
    print("total words are ",total_words)
    print("type is ",type(total_words))
    return render(request,"520-templates/520-see-word-list.html",{"total_words":total_words,"count":temp})
def feedback(request):
    return render(request,'520-templates/520-feedback.html')
def feedback_received(request):
    if request.method == "POST":
        data = request.POST
        print("first name = ",data['firstname'])
        print("last name = ",data['lastname'])
        return HttpResponse('sent successfully')
    return render(request,'520-templates/520-feedback-receive.html')