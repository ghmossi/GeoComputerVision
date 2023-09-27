from django import forms
from gallery.models import PhotoSet

class CreateMap(forms.ModelForm):
    class Meta:
        model = PhotoSet
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreateMap, self).__init__(*args, **kwargs)
        self.fields['title'].queryset = PhotoSet.objects.filter(owner=user).order_by('id').reverse()

    title = forms.ModelChoiceField(queryset = None, widget=forms.Select(attrs={'class': 'form-control'}), required=True)