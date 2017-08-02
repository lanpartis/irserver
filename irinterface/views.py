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
    Selected_model = forms.CharField()
    Image = forms.FileField()

class ModelForm(forms.Form):
    Model = forms.FileField()

def homepage(request):
    return render_to_response("irinterface/homepage.html")

def upload(request):
    return render_to_response("irinterface/upload.html")

def upload_model(request):
    if request.method == "POST":
        uf = ModelForm(request.POST,request.FILES)
        if uf.is_valid():
            model_src = uf.cleaned_data['Model']
            pm = PdModel()
            pm.model_src = model_src
            pm.save()
            return HttpResponse(model_src.name+' upload succeed.')
    else:
        uf = ModelForm()
        return render(request,'irinterface/upload_model.html',{'uf':uf})

def upload_image(request):
    if request.method == "POST":
        uf = ImageForm(request.POST,request.FILES)
        if uf.is_valid():
            model_name = uf.cleaned_data['Selected_model']
            headImg = uf.cleaned_data['Image']
            pd = PdImage()
            pd.model_name = model_name
            pd.image_src = headImg
            pd.save()
            src = model_name
            print('using media.upload_networks.'+model_name)
            try:
                pkg = importlib.import_module('media.upload_networks.'+src)
            except ImportError:
                print(ImportError)
                return HttpResponse('Import error.')
            c1 = pkg.DLMOD()
            path = settings.MEDIA_ROOT
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
