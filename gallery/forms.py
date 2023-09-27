from django import forms
from .models import *
from betterforms.multiform import MultiModelForm
from bootstrap_modal_forms.forms import BSModalModelForm

class PhotoForm(forms.ModelForm):
    photoset = forms.ModelChoiceField(queryset = None, widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    image_r = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'type':'file', 'multiple':''}), required=True, label='Carpeta de imagenes derechas')
    image_l = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'type':'file', 'multiple':''}), required=True, label='Carpeta de imagenes izquierdas')
    class Meta:
        model = Photo_pair
        fields = ['photoset', 'image_r', 'image_l']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['photoset'].queryset = PhotoSet.objects.filter(owner=user)

class SetForm(forms.ModelForm):
    class Meta:
        model = PhotoSet
        fields = '__all__'

        widgets = {
            'title':forms.TextInput(attrs={'class' : 'form-control'}),
            'owner':forms.TextInput(attrs={'class' : 'form-control','value':'','id':'owner', 'type':'hidden'}),
        }

class DeleteForm(forms.ModelForm):
    class Meta:
        model = PhotoSet
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DeleteForm, self).__init__(*args, **kwargs)
        self.fields['title'].queryset = PhotoSet.objects.filter(owner=user)

    title = forms.ModelChoiceField(queryset = None, widget=forms.Select(attrs={'class': 'form-control'}), required=True)

class ObjectForm(forms.ModelForm):
    class Meta:
        model = StreetObject
        fields = ['name','description','objtype']
    
        widgets = {
            'name':forms.TextInput(attrs={'class' :'form-control me-2'}),
            'description':forms.TextInput(attrs={'class' :'form-control'}),
            'objtype':forms.Select(attrs={'class' :'form-control me-2'}),
        }

class ROIForm(forms.ModelForm):
    class Meta: 
        model = Roi
        fields = '__all__'
        
        widgets = {
            'center_x':forms.NumberInput(attrs={'class' : 'form-control','value':'','id':'form_center_x', 'type':'hidden'}),
            'center_y':forms.NumberInput(attrs={'class' : 'form-control','value':'','id':'form_center_y', 'type':'hidden'}),
            'width':forms.NumberInput(attrs={'class' : 'form-control','value':'','id':'form_width', 'type':'hidden'}),
            'height':forms.NumberInput(attrs={'class' : 'form-control','value':'','id':'form_height', 'type':'hidden'})
        }

class LocationForm(forms.ModelForm):
    class Meta: 
        model = Location
        fields = '__all__'
        
        widgets = {
            'latitude':forms.NumberInput(attrs={'class' : 'form-control','value':'','id':'form_latitude', 'type':'hidden'}),
            'longitude':forms.NumberInput(attrs={'class' : 'form-control','value':'','id':'form_longitude', 'type':'hidden'})
        }

class ObjectAttributeForm(BSModalModelForm):
    class Meta:
        model = ObjectAttributes
        fields = ['attribute_key','attribute_value']
        labels = {
            "attribute_key": "",
            "attribute_value": ""
        }

        widgets = {
            'attribute_key':forms.TextInput(attrs={'class' :'form-control me-2', 'placeholder':'atributo'}),
            'attribute_value':forms.TextInput(attrs={'class' :'form-control', 'placeholder':'valor'}),
        }

class AddObjectForm(MultiModelForm):
    form_classes = {
        'object': ObjectForm,
        'roi': ROIForm,
        'loc': LocationForm,
    }

class DownloadDXFForm(forms.ModelForm):
    class Meta:
        model = PhotoSet
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DeleteForm, self).__init__(*args, **kwargs)
        self.fields['title'].queryset = PhotoSet.objects.filter(owner=user)

    title = forms.ModelChoiceField(queryset = None, widget=forms.Select(attrs={'class': 'form-control'}), required=True)