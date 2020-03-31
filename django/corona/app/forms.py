from django import forms
from .models import cases, volunteers
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Email must be unique"}),
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "8 or more characters"}),
    )
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter first name"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter last name"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class volunteersForm(forms.ModelForm):
    mobile = forms.CharField(
        label="Mobile No. (add Country Code)",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "+120XXXXXXXX"}),
    )
    landline = forms.CharField(
        label="Landline No.",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "+120XXXXXXXX"}),
    )

    address = forms.CharField(
        label="Full Address",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "14, MG ROAD, Nashik"}),
    )
    postal_code = forms.IntegerField(
        label="Postal Code",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "422008"}),
    )

    class Meta:
        model = volunteers
        fields = ("mobile", "landline", "address",
                  "postal_code", "x", "y", "servicescanprovide", "country")


class casesForm(forms.ModelForm):
    condition = (
        ("Severe", "Severe"),
        ("Isolated", "Isolated"),
        ("Negative", "Negative"),
        ("Curious", "Curious"),
    )
    sexop = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    name = forms.CharField(
        label="Name",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Name Please "}
        ),
    )
    telephone = forms.CharField(
        label="Phone No. (add Country Code)",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "+120XXXXXXXX"}),
    )
    condition = forms.ChoiceField(choices=condition)
    age = forms.IntegerField()
    sex = forms.ChoiceField(choices=sexop)

    class Meta:
        model = cases
        fields = "__all__"
