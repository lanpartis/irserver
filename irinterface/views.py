from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
import os
from irserver import settings
# Create your views here.
from irinterface.models import PdImage,PdModel
import importlib
from deep_learning_models.model_interface import DLMOD
def show_lib(request):
    imgs = PdImage.objects.all()
    return render_to_response("irinterface/lib_list.html",{"imgs":imgs})

class ImageForm(forms.Form):
    Select_model = forms.CharField()
    Image = forms.FileField()

class ModelForm(forms.Form):
    Model_file = forms.FileField()

def homepage(request):
    return render_to_response("irinterface/homepage.html")

def upload(request):
    return render_to_response("irinterface/upload.html")

def upload_model(request):
    if request.method == "POST":
        uf = ModelForm(request.POST,request.FILES)
        if uf.is_valid():
            model_src = uf.cleaned_data['Model_file']
            pm = PdModel()
            pm.model_src = model_src
            pm.save()
            return HttpResponse(model_src.name+ ' upload succeed.')
    else:
        uf = ModelForm()
        return render(request,'irinterface/upload_model.html',{'uf':uf})

def upload_image(request):
    if request.method == "POST":
        uf = ImageForm(request.POST,request.FILES)
        if uf.is_valid():
            model_name = uf.cleaned_data['Select_model']
            headImg = uf.cleaned_data['Image']
            path = 'upload_networks/'+model_name
            print(path)
            try:
                PdModel.objects.get(model_src=path)
            except:
                return HttpResponse("Model not found.")

            pd = PdImage()
            pd.model_name = model_name
            pd.image_src = headImg

            path = settings.MEDIA_ROOT
            pd.save()
            model_path = path+'/upload_networks/'+str(model_name)
            c1 = DLMOD(model_path)
            result = c1.predict(path+'/img/'+headImg.name)
            pd.prediction = str(result)
            pd.save()
            return render_to_response("irinterface/result.html",{'img':pd})
            # return HttpResponse('upload ok! the image is %s result is%s' %(path+"/media/img/"+headImg.name,result))
    else:
        uf = ImageForm()
    return render(request,'irinterface/upload_image.html',{'uf':uf})
