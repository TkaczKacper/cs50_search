from django import forms


class CreateListingForm(forms.Form):
    title = forms.CharField(label='Title', max_length=64)
    description = forms.CharField(label='Description', max_length=500)
    auction_image = forms.URLField(label='Image url (if you dont want to add image just skip this input)', required=False)
    choices = (('Sport', 'Sport'), ('Jewlery', 'Jewelry'), ('Decorations', 'Decorations'), ('Books', 'Books'), ('Automotive', 'Automotive'), ('Electronics', 'Electronics'), ('Toys', 'Toys'))
    category = forms.ChoiceField(choices=choices)
    starting_bid = forms.DecimalField(max_digits=8, decimal_places=2)
    duration = forms.IntegerField(label='Duration (hours)')

class MakeBid(forms.Form):
    bid = forms.DecimalField(label='Your offer', max_digits=10, decimal_places=2)

class AddComment(forms.Form):
    comment = forms.CharField(label=False, max_length=255)