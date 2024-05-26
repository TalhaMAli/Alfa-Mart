from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=10)
    place = forms.CharField(max_length=100)
    payment_method = forms.ChoiceField(choices=[('stripe', 'Credit Card'), ('cod', 'Cash on Delivery')])
    stripe_token = forms.CharField(required=False)
