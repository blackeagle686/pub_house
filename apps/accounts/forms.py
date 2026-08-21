from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="رقم الهاتف", max_length=11, widget=forms.TextInput(attrs={'placeholder': 'مثال: 01xxxxxxxxx'}))

class UserRegistrationForm(forms.ModelForm):
    phone = forms.CharField(max_length=11, label="رقم الهاتف", widget=forms.TextInput(attrs={'placeholder': 'مثال: 01xxxxxxxxx'}))
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="تأكيد كلمة المرور")
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 11 or not phone.startswith('01'):
            raise forms.ValidationError("يجب أن يكون رقم الهاتف مكوناً من 11 رقماً ويبدأ بـ 01")
        if User.objects.filter(username=phone).exists():
            raise forms.ValidationError("رقم الهاتف مستخدم بالفعل.")
        return phone

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password') != cd.get('password_confirm'):
            raise forms.ValidationError("كلمات المرور غير متطابقة")
        return cd.get('password_confirm')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['phone']
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    primary_phone = forms.CharField(label="رقم الهاتف الأساسي (غير قابل للتعديل)", disabled=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['primary_phone'] = self.instance.username

class ProfileEditForm(forms.ModelForm):
    phone = forms.CharField(label="رقم هاتف إضافي (اختياري)", max_length=20, required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'location'] # 'image' field removed for now
