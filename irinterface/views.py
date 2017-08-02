from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
import os
from irserver import settings
# Create your views here.
from irinterface.models import PdImage,PdModel
import importlib
# from deep_learning_models.se_classifier import DLMOD
def show_lib(request):
    imgs = PdImage.objects.all()
    return render_to_response("irinterface/lib_list.html",{"imgs":imgs})

class ImageForm(forms.Form):
    Select_model = forms.CharField()
    Image = forms.FileField()

class ModelForm(forms.Form):
    Model_manage_file = forms.FileField()
    Model_file = forms.FileField()

def homepage(request):
    return render_to_response("irinterface/homepage.html")

def upload(request):
    return render_to_response("irinterface/upload.html")

def upload_model(request):
    if request.method == "POST":
        uf = ModelForm(request.POST,request.FILES)
        if uf.is_valid():
            model_src = uf.cleaned_data['Model_manage_file']
            weights_src = uf.cleaned_data['Model_file']
            pm = PdModel()
            pm.model_src = model_src
            pm.weights_src = weights_src
            pm.save()
            return HttpResponse(model_src.name+' and '+ weights_src.name + ' upload succeed.')
    else:
        uf = ModelForm()
        return render(request,'irinterface/upload_model.html',{'uf':uf})

def upload_image(request):
    if request.method == "POST":
        uf = ImageForm(request.POST,request.FILES)
        if uf.is_valid():
            model_name = uf.cleaned_data['Select_model']
            headImg = uf.cleaned_data['Image']
            pd = PdImage()
            pd.model_name = model_name
            pd.image_src = headImg

            print('using media.upload_networks.'+model_name)
            try:
                pkg = importlib.import_module('media.upload_networks.'+model_name)
            except ImportError:
                print(ImportError)
                return HttpResponse('Import error. Model not found.')

            path = settings.MEDIA_ROOT
            try:
                model = PdModel.objects.get(model_src='upload_networks/'+model_name+'.py')
            except:
                return HttpResponse('Model missing!')
            pd.save()
            model_path = path+'/'+str(model.weights_src)
            c1 = pkg.DLMOD(model_path)
            result = c1.predict(path+'/img/'+headImg.name)
            result= result[0]
            pd.prediction = str(result)
            # pd.prediction1 = "Prediction1 :%s \twith %d%% confidence"%(result[0][1],int(result[0][2]*100))
            # pd.prediction2 = "Prediction2 :%s \twith %d%% confidence"%(result[1][1],int(result[1][2]*100))
            # pd.prediction3 = "Prediction3 :%s \twith %d%% confidence"%(result[2][1],int(result[2][2]*100))
            # pd.prediction4 = "Prediction4 :%s \twith %d%% confidence"%(result[3][1],int(result[3][2]*100))
            pd.save()
            del pkg
            return render_to_response("irinterface/result.html",{'img':pd})
            # return HttpResponse('upload ok! the image is %s result is%s' %(path+"/media/img/"+headImg.name,result))
    else:
        uf = ImageForm()
    return render(request,'irinterface/upload_image.html',{'uf':uf})
