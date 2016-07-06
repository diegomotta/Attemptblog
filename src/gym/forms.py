from django import forms
from django.core.urlresolvers import reverse_lazy 
from .models import Post
import datetime
from django.forms.extras.widgets import SelectDateWidget
class PostForm(forms.ModelForm):
	publish = forms.DateField(widget=SelectDateWidget)
	class Meta:
		model = Post
		fields =["title","content","image"]