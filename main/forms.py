from django import forms



class SearchForm(forms.Form):
	keyword = forms.CharField(required=False, max_length=200)