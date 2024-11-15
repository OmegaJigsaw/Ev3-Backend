from django import forms
from app.models import User, Categoria, Producto

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    
    password = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'})
        )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'rol': forms.HiddenInput(),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'disponible': forms.HiddenInput(),
            }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control','min': '1','step': '1'}),
            'fecha_ingreso': forms.DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'disponible': forms.HiddenInput(),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept':'image/*'})
        }
        