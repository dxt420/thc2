from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from . models import CustomUser,Department,Patient,Bed,Doctor,Employee,Message

from django.forms import ModelChoiceField,ModelForm,TextInput,Textarea

from . choices import GENDER_CHOICES,BLOOD_GROUPS,PAYMENT_STATUS,BED_TYPES,MONTHS,YEAR_CHOICES,PAYMENT_STATUS

from django.db import transaction

from django.utils.translation import ugettext_lazy as _
import datetime


class MessageForm(ModelForm):

    receiver = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class' : 'select2 form-control'}))

    class Meta:
        model = Message
        fields = ('receiver','message_content')

    @transaction.atomic    
    def save(self):        
        message = super().save(commit=False)   
        # message.save()        
        return message

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        (1,'admin'),
        (2,'doctor'),
    )
    user_type =forms.ChoiceField(choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    name =  forms.CharField(max_length=30)
    dob = forms.DateField()
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email')

class CustomUserCreationFormDoctor(UserCreationForm):
    dob = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker','autocomplete':'off'}))
    departmentname = forms.ModelChoiceField(queryset=Department.objects.all(), to_field_name="departmentname",
        widget=forms.Select(attrs={'class' : 'form-control'}))
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    first_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    last_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'})) 
    password1 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   
    password2 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))  


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username','phone')
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormDoctor, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Re-Type Password"
        self.fields['dob'].label = "Date of Birth"

    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_doctor = True
        

        user.save()    
        


        # user.role.set(range(Role.DOCTOR))     
        doctor = Doctor.objects.create(user=user)  
        Employee.objects.create(user=user)  
        # doctor.departmentname.add(*self.get('departmentname'))    
        # doctor.usericon.add(*self.get('usericon'))    
            
        return doctor


class CustomUserCreationFormNurse(UserCreationForm):
    dob = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    first_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    last_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'})) 
    password1 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   
    password2 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username')
        

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormNurse, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Re-Type Password"
        self.fields['dob'].label = "Date of Birth"


    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_nurse = True

        user.save()    
        

        Employee.objects.create(user=user)   
        return user
            
        

class CustomUserCreationFormPatient(UserCreationForm):
    dob = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    first_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    last_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'})) 
    sex = forms.ChoiceField(choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    password1 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   
    password2 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username','phone')

   
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormPatient, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Re-Type Password"
        self.fields['dob'].label = "Date of Birth"
       
    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_patient = True

        user.save()    

        patient = Patient.objects.create(user=user)              
        return patient           

class CustomUserCreationFormReception(UserCreationForm):
    dob = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    first_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    last_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'})) 
    password1 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))    
    password2 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username','phone')
        

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormReception, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Re-Type Password"
        self.fields['dob'].label = "Date of Birth"


    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_receptionist = True
        

        user.save()    

        Employee.objects.create(user=user)  
        return user           

class CustomUserCreationFormLabaratorist(UserCreationForm):
    dob = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    first_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    last_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'})) 
    password1 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   
    password2 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username','phone')
        

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormLabaratorist, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Re-Type Password"
        self.fields['dob'].label = "Date of Birth"


    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_labaratorist = True

        user.save()    

        Employee.objects.create(user=user)  
        return user           

class CustomUserCreationFormPharmacist(UserCreationForm):
    dob = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    first_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    last_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'})) 
    password1 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   
    password2 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username','phone')
        


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormPharmacist, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Re-Type Password"
        self.fields['dob'].label = "Date of Birth"


    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_pharmacist = True
     
        user.save()    
        
        Employee.objects.create(user=user)   
        return user 


class CustomUserCreationFormAccountant(UserCreationForm):
    dob = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    first_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    last_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'})) 
    password1 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   
    password2 = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','type' : 'password',}))   

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username','phone')
        

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormAccountant, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Re-Type Password"
        self.fields['dob'].label = "Date of Birth"


    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_accountant = True
        
   
        user.save()    
        

        Employee.objects.create(user=user)    

        return user 
# class CustomUserChangeFormDoctor(ModelForm):

#     class Meta:
#         model = CustomUser
#         fields = ('first_name','last_name','dob','departmentname','email','username')

#     @transaction.atomic    
#     def save(self):        
#         user = super().save(commit=False)   
#         user.save()        
#         doctor = Doctor.objects.get(user=user)         
#         # doctor.departmentname.add(*self.get('departmentname'))    
#         # doctor.usericon.add(*self.get('usericon'))    
            
#         return doctor

class addPatientForm(forms.Form):
    name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    address = forms.CharField(max_length=300,
        widget=forms.Textarea(attrs={'class' : 'form-control','rows':'4'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    sex = forms.ChoiceField(choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    dob = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    age = forms.IntegerField(
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    blood = forms.ChoiceField(choices=BLOOD_GROUPS,
        widget=forms.Select(attrs={'class' : 'form-control'}))

class addDepartmentForm(forms.Form):
    departmentname = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Department Name','autocomplete':'off'}))
    description = forms.CharField(max_length=200,
        widget=forms.Textarea(attrs={'class' : 'form-control','rows':'5','autocomplete':'off'}))
    
    # class Meta:
    #     model = Department
    #     fields = ['departmentname','description','image']
    #     widgets = {
    #         'departmentname': TextInput(attrs={'class' : 'form-control','placeholder':'Enter Department Name'}),
    #         'description' : Textarea(attrs={'class' : 'form-control','rows':'5'}),
            
    #     }
        

class addDoctorForm(forms.Form):
    name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Full Name'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    departmentname = forms.ModelChoiceField(queryset=Department.objects.all(), to_field_name="departmentname",
        widget=forms.Select(attrs={'class' : 'form-control'}))

class addAccountantForm(forms.Form):
    name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Full Name'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    address = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))

class addNurseForm(forms.Form):
    name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Full Name'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    address = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    
class addPharmacistForm(forms.Form):
    name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Full Name'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    address = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))

class addLabaratoristForm(forms.Form):
    name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Full Name'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    address = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    

class addReceptionistForm(forms.Form):
    name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Full Name'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    address = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))





class createPayrollForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class' : 'select2 form-control'}))
    month = forms.ChoiceField(choices=MONTHS,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    year = forms.ChoiceField(choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class' : 'form-control '}))
    basic = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','id':'basic','autocomplete':'off'}))
    status = forms.ChoiceField(choices=PAYMENT_STATUS,
        widget=forms.Select(attrs={'class' : 'select form-control'}))
    

class addBedForm(forms.Form):
    #choice
    number = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','onkeypress':'return event.charCode >= 48 && event.charCode <= 57','autocomplete':'off'}))
 
    bed_type =  forms.ChoiceField(choices=BED_TYPES,
        widget=forms.Select(attrs={'class' : 'form-control '}))
    
    description = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    

############
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.bedinfo()
class addBedAllotmentForm(forms.Form):
    #choice
    bed_number =  MyModelChoiceField(queryset=Bed.objects.all(),to_field_name="bedinfo",
        widget=forms.Select(attrs={'class' : 'select form-control'}))
    #choice
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class' : 'select2 form-control'}))
    allotment_time = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    discharge_time = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))

class addPrescriptionForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class' : 'select2 form-control'}))
    
    date = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
            'class' : 'form-control datepicker',
            'data-format' : 'D, dd MM yyyy',
            'placeholder' : 'Appointment Date',
            'autocomplete':'off'
            }))
    
    time = forms.TimeField(
        widget=forms.TextInput(attrs={
            'class' : 'form-control timepicker',
            'data-template' : 'dropdown',
            'placeholder' : 'time here',
            'data-show-seconds' : 'false',
            'data-default-time' : '00:05 AM',
            'data-show-meridian' : 'false',
            'data-minute-step' : '5',
            'autocomplete':'off'
            }))
    case_history = forms.CharField(
        widget=forms.Textarea(attrs={'class' : 'form-control ','rows':'4'}))
    medication = forms.CharField(
        widget=forms.Textarea(attrs={'class' : 'form-control ','rows':'4'}))
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class' : 'form-control ','rows':'4'}))

class addReportForm(forms.Form):
    type = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Full Name'}))
    description = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    #choice
    patient = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    date = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))

class addDiagnosisReportForm(forms.Form):
    type = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Enter Full Name'}))
    description = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    #choice
    document = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    date = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))

class addAppointmentForm(forms.Form):
    notify = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
        'type':'checkbox','value':'checked'}))
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class' : 'select2 form-control'}))
    
    date = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
            'class' : 'form-control datepicker',
            'data-format' : 'D, dd MM yyyy',
            'placeholder' : 'Appointment Date',
            'autocomplete':'off'
            }))
    
    time = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
            'class' : 'form-control timepicker',
            'data-template' : 'dropdown',
            'placeholder' : 'time here',
            'data-show-seconds' : 'false',
            'data-default-time' : '00:05 AM',
            'data-show-meridian' : 'false',
            'data-minute-step' : '5',
            'autocomplete':'off'
            }))

class applyAppointmentForm(forms.Form):    
    date = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
            'class' : 'form-control datepicker',
            'data-format' : 'D, dd MM yyyy',
            'placeholder' : 'Appointment Date',
            'autocomplete':'off'
            }))
    
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={'class' : 'select2 form-control'}))

class addInvoiceForm(forms.Form):
    title = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control',
        'data-validate' : 'required',
        'data-message-required' : 'Value Required',}))
 
    ##read only code needed
    invoicenum = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','readonly':''}))
    
    ##choice from patients db
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class' : 'select2 form-control'}))
    
    creationdate = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
            'class' : 'form-control datepicker',
            }))

    duedate = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
            'class' : 'form-control datepicker',
            'data-format' : 'D, dd MM yyyy',         
            }))
    
    vatpercent = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))

    discount = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))


    status = forms.ChoiceField(choices=PAYMENT_STATUS,
        widget=forms.Select(attrs={'class' : 'select2'}))
    
    description = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control',
        'placeholder' : 'Description',
        }))

    amount = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control',
        'placeholder' : 'Description',
        'min' : 0,}))
    
###labaratorist

class addBloodDonorForm(forms.Form):
    name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    address = forms.CharField(max_length=300,
        widget=forms.Textarea(attrs={'class' : 'form-control','rows':'4'}))
    phone = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    sex = forms.ChoiceField(choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class' : 'form-control'}))
    last_donation = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'class' : 'form-control datepicker'}))
    age = forms.IntegerField(
        widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'off'}))
    blood = forms.ChoiceField(choices=BLOOD_GROUPS,
        widget=forms.Select(attrs={'class' : 'form-control'}))
       
   