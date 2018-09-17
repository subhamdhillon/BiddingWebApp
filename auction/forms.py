from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item,Bid

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.CharField(max_length=30)

	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password1','password2')

class BidForm(forms.ModelForm):

	class Meta:
		model = Bid
		fields = ('bid_amount',)

class ItemForm(forms.ModelForm):

	class Meta:
		model = Item
		fields = ('item_name','base_price','item_description','item_category','item_close','item_image')

