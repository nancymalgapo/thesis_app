from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from os.path import dirname, exists, isdir, realpath, isfile, join

import glob
import pdb
#from .hcr import HCR
import os

from .plagscan import login_user, plagscan_upload
#from .forms import DocumentForm
#from .picam import capture_images
#from .ocr import read_typewritten_img, read_handwritten_from_dir
from .utils import SCANNED_FILES_DIR, create_dir, format_list, generate_pdf
from time import sleep


from django.core.files.storage import FileSystemStorage

from .Api import PlagScan
from .models import Document
from django.core.exceptions import ObjectDoesNotExist

login_validation = True
doc_type = ""
doc_title = ""
doc_pages = 0


def index(request):
    global login_validation
    login_validation = False
    print(login_validation)
    return render(request, 'index.html')

def login(request):
    global login_validation
    login_validation = False
    if request.method == 'GET':
        # testing
        login_validation = True
        return render(request, 'user_home.html')
        # login_validation = False
        # return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('pwd', '')
        if login_user(username, password):
            request.session['username'] = username
            request.session['password'] = password
            login_validation = True
            return render(request, 'user_home.html')
        else:
            messages.warning(
                request, 'Login failed! Please enter a valid username and password, or check your internet connection and try again!')
            return render(request, 'login.html')


def user_home(request):
    global login_validation
    login_validation = False
    if login_validation:
        return render(request, 'user_home.html')
    else:
        return render(request, 'error_page.html')

def user_home_scan(request):
    global login_validation
    print(login_validation)
    if login_validation:
        return render(request, 'user_home_scan.html')
    else:
        return render(request, 'error_page.html')

def doc_info_flatbed(request):
    print('doc_info_flatbed')
    print(login_validation)
    if login_validation:
        if request.method == 'GET':
            return render(request, 'doc_info_flatbed.html')
        elif request.method == 'POST':
            global doc_type
            global doc_title
            global doc_pages
            doc_type = request.POST.get('doc_type', '')
            doc_title = request.POST.get('doc_title', '')
            doc_pages = request.POST.get('doc_pages', '')

            if create_dir(doc_title):
                messages.success(
                    request, 'New folder created! Folder location: ' + SCANNED_FILES_DIR)
                return render(request, 'user_procedure_flatbed.html', {})
            else:
                messages.error(request, 'Folder already exists!')
                return render(request, 'doc_info_flatbed.html')
    else:
        return render(request, 'error_page.html')

def doc_info_feeder(request):
    print(login_validation)
    if login_validation:
        if request.method == 'GET':
            return render(request, 'doc_info_feeder.html', {})
        elif request.method == 'POST':
            global doc_type
            global doc_title
            global doc_pages
            doc_type = request.POST.get('doc_type', '')
            doc_title = request.POST.get('doc_title', '')
            doc_pages = request.POST.get('doc_pages', '')

            if not create_dir(doc_title):
                messages.error(request, 'Folder already exists!')
                return render(request, 'doc_info_feeder.html')
            else:
                messages.success(
                    request, 'New folder created! Folder location: ' + SCANNED_FILES_DIR)
                return render(request, 'user_procedure_feeder.html', {})
    else:
        return render(request, 'error_page.html')


def user_procedure_flatbed(request):
    print(login_validation)
    if login_validation:
        return render(request, 'user_procedure_flatbed.html')
    else:
        return render(request, 'error_page.html')


def user_procedure_feeder(request):
    print(login_validation)
    if login_validation:
        return render(request, 'user_procedure_feeder.html')
    else:
        return render(request, 'error_page.html')


def user_upload_scan_flatbed(request):
    print('user_upload_scan_flatbed')
    if login_validation:
        if request.method == 'GET':
            return render(request, 'user_upload_scan_flatbed.html')
        elif request.method == 'POST':
            if 'scan' in request.POST:
                print('scan')
                
                #TODO: capture 1 image
                capture_images((SCANNED_FILES_DIR + doc_title + '/'), 1, 'flatbed')
                print('Finish Capturing images')            
                return render(request, 'user_upload_scan_flatbed.html')
            elif 'submit' in request.POST:
                if doc_type == 'T_Written':
                    for f in glob.glob(SCANNED_FILES_DIR + doc_title + '/*.jpg'):
                        unformatted_list = read_typewritten_img(f)
                        recognized_text.append(format_list(unformatted_list))
                else:
                    recognized_text = read_handwritten_from_dir(
                        SCANNED_FILES_DIR + doc_title)
                for file in glob.glob(SCANNED_FILES_DIR + doc_title + '/*.jpg'):
                    if doc_type == 'T_Written':
                        unformatted_list = read_typewritten_img(file)
                        recognized_text.append(format_list(unformatted_list))
                    else:
                        pass
                unformatted_list = read_handwritten_img(file)
                recognized_text.append(
                format_list(unformatted_list))
                generate_pdf(recognized_text, doc_title)
                print("PDF generated")
                print('upload')
                content = dirname(realpath(__file__)) + "/Documents/" + \
                    doc_title + "/" + doc_title + ".pdf"
                if plagscan_upload(content):
                    messages.success(request, 'Files upload completed!')
                    return render(request, 'doc_result.html')
                else:
                    messages.error(request, 'Files failed to upload! Try again.')
                    return render(request, 'user_upload_scan_flatbed.html')
    else:
        return render(request, 'error_page.html')

def user_upload_scan_feeder(request):
    global doc_title
    global doc_pages
    global doc_type
    if login_validation:
        if request.method == 'GET':
            print('GET')
            capture_images(SCANNED_FILES_DIR + doc_title + '/', doc_pages, 'feeder')
            print('Finish Capturing images')
            messages.success(request, 'null')
            return render(request, 'user_upload_scan_feeder.html')
        elif request.method == 'POST':
            if 'scan' in request.POST:
                print('scan')
                doc_pages = request.POST.get('doc_pages', '')
                print(doc_pages)
                capture_images(SCANNED_FILES_DIR + doc_title + '/', doc_pages)
                messages.success(request, 'null')
                return render(request, 'user_upload_scan_feeder.html')
            elif 'submit' in request.POST:
                print('submit')
                recognized_text = []
                doc_title = 'HW_TEST'
                if doc_type == 'T_Written':
                    for f in glob.glob(SCANNED_FILES_DIR + doc_title + '/*.jpg'):
                        unformatted_list = read_typewritten_img(f)
                        recognized_text.append(format_list(unformatted_list))
                else:
                    recognized_text = read_handwritten_from_dir(
                        SCANNED_FILES_DIR + doc_title)
                for file in glob.glob(SCANNED_FILES_DIR + doc_title + '/*.jpg'):
                    if doc_type == 'T_Written':
                        unformatted_list = read_typewritten_img(file)
                        recognized_text.append(format_list(unformatted_list))
                    else:
                        unformatted_list = read_handwritten_img(file)
                        pass
                unformatted_list = read_handwritten_img(file)
                recognized_text.append(
                format_list(unformatted_list))
                generate_pdf(recognized_text, doc_title)
                print("PDF generated")
                content = dirname(realpath(__file__)) + "/Documents/" + \
                    doc_title + "/" + doc_title + ".pdf"
                if plagscan_upload(content):
                    messages.success(request, 'Files upload completed!')
                    return render(request, 'doc_result.html')
                else:
                    messages.error(request, 'Files failed to upload! Try again.')
                    return render(request, 'user_upload_scan_feeder.html')
    else:
        return render(request, 'error_page.html')

def user_upload_direct(request):
    if login_validation:
        if request.method == 'GET':
            with open('media/documents/questions.docx', 'rb') as f: #open the file
                contents = f.readlines() #put the lines to a variable (list).
                print (f.readlines())
            return render(request, 'user_upload_direct.html')
        elif request.method == 'POST':
            plagscan = PlagScan()
           
            newdoc = Document(document=request.FILES['myfile'])
            newdoc.save()
            docID = plagscan.document_submit(newdoc.document, newdoc)
            
            print ('Validating form ...')
            #form = DocumentForm(request.POST, request.FILES)
            '''

            fs = FileSystemStorage()
            uploaded_file = request.FILES['myfile']
            temp_name = str(uploaded_file).replace(' ', '_')
            fs.save(temp_name, uploaded_file)

            upload_path = fs.location + '/' + temp_name
            # TODO: Check document if pdf (doc is saved on media dir)
            content = fs.location + '/' + temp_name
            print(content)
            if plagscan_upload(content):
                messages.success(request, 'Files upload completed!')
                return render(request, 'doc_result.html')
            else:
                messages.error(request, 'Files failed to upload! Try again.')
                return render(request, 'user_upload_scan_flatbed.html')

            os.system('rm %s ' % (fs.location + '/' + temp_name))
            '''
            return redirect("/home/document/?id="+str(docID))
            return render(request, 'user_upload_direct.html')
        else:
            print('INVALID FORM')
            return render(request, 'user_upload_direct.html')

            form = DocumentForm()
        # return render(request, 'user_upload_direct.html', {'form': form})
    else:
        return render(request, 'error_page.html')

def document_list(request):
    if request.method == 'GET':
        documents = Document.objects.all()
        context = {}
        context['documents'] = documents
        return render(request, 'document_list.html', context)

def document(request):
    if request.method == 'GET':
        doc_id = request.GET.get("id")
        try:
            document = Document.objects.get(docID= doc_id) or None
        except ObjectDoesNotExist:
            document = None
        
        context = {}
        context['document'] = document
        if document is None:
             return HttpResponse("DOCUMENT ID DOES NOT EXIST")
        plagscan = PlagScan()
        status = plagscan.document_analyzed_status(doc_id)
        if status == "not":
            return render(request, 'document_not.html', context)
        elif status == "checking":
            return render(request, 'document_checking.html', context)
        elif status == "converting":
            return render(request, 'document_converting.html', context)
        elif status == "done":
            context['report'] = plagscan.document_report(doc_id)
            return render(request, 'document_done.html', context)
            pass

def document_check(request):
    if request.method == 'GET':
        doc_id = request.GET.get("id")
        try:
            document = Document.objects.get(docID= doc_id)
        except ObjectDoesNotExist:
            document = None
        context = {}
        context['document'] = document
        if document is None:
             return HttpResponse("DOCUMENT ID DOES NOT EXIST")
        plagscan = PlagScan()
        status = plagscan.document_check_plagiarism(doc_id)
        return HttpResponse(status)

def doc_result(request):
    global login_validation
    if login_validation:
        return render(request, 'doc_result.html')
        login_validation = False
    else:
        return render(request, 'error_page.html')

def error_page(request):
    global login_validation
    login_validation = False
    return render(request, 'error_page.html')
