from django import forms

class SampleChoiceForm(forms.Form):
	CHOICE = (
		('gairai', '外来'),
		('kyuugai', '救外'),
	)
	select = forms.fields.ChoiceField(required=True, widget = forms.widgets.Select, choices=CHOICE)
