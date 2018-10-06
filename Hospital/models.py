from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from .choices import PAYMENT_STATUS

from django.utils import timezone
import datetime

 

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=30)
    usericon = models.ImageField(upload_to='media/',default='aa',blank=True)
    is_doctor = models.BooleanField(default=False,blank=True)
    is_nurse = models.BooleanField(default=False,blank=True)
    is_accountant = models.BooleanField(default=False,blank=True)
    is_labaratorist = models.BooleanField(default=False,blank=True)
    is_pharmacist = models.BooleanField(default=False,blank=True)
    is_patient = models.BooleanField(default=False,blank=True)
    is_admin = models.BooleanField(default=False,blank=True)
    is_receptionist = models.BooleanField(default=False,blank=True)

    def name(self):
        return self.first_name + " " + self.last_name
        
class Department(models.Model):
    departmentname = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    depticon = models.ImageField(upload_to='media/',default='aa',blank=True)
    
    def __str__(self):
        return self.departmentname

class Employee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,primary_key=True)
    

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
        # if self.user.is_receptionist:
        #     return self.user.first_name + " " + self.user.last_name + "(Reception)"
        # if self.user.is_labaratorist:
        #     return "Dr. " + self.user.first_name + " " + self.user.last_name + "(Labaratorist)"
        # if self.user.is_pharmacist:
        #     return self.user.first_name + " " + self.user.last_name + "(Pharmacist)"
        # if self.user.is_accountant:
        #     return self.user.first_name + " " + self.user.last_name + "(Accountant)"
    # def name(self):
    #     return self.user.first_name + " " + self.user.last_name
        

class Patient(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,primary_key=True)
    blood_group = models.CharField(max_length=30)
    sex = models.CharField(max_length=8)
    dob = models.CharField(max_length=30)
    usericon = models.ImageField(upload_to='media/',default='aa',blank=True)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    def name(self):
        return self.user.first_name + " " + self.user.last_name
  



class Doctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,primary_key=True)
    usericon = models.ImageField(upload_to='media/',default='aa',blank=True)
    departmentname = models.CharField(max_length=30)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
   
class Payroll(models.Model):
    month = models.CharField(max_length=30)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.CharField(max_length=30)
    basic = models.IntegerField()
    total_allowance = models.IntegerField()
    total_deduction = models.IntegerField()
    net = models.IntegerField()
    status = models.CharField(choices=PAYMENT_STATUS, max_length=10)
     

class PayrollAllowance(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    allowance = models.IntegerField()

class PayrollDeduction(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    deduction = models.IntegerField()
    

class PaymentHistory(models.Model):
    invoice_number = models.CharField(max_length=30,primary_key=True)
    title = models.CharField(max_length=30)
    patient =  models.ForeignKey(Patient, on_delete=models.CASCADE)
    creation_date = models.CharField(max_length=30)
    due_date = models.CharField(max_length=30)
    vat_percentage = models.CharField(max_length=30)
    discount_amount = models.IntegerField()
    status = models.CharField(max_length=30)
     
    def __str__(self):
        return self.invoice_number

class Bed(models.Model):
    bed_number = models.CharField(max_length=30)
    bed_type = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    
    
    def bedinfo(self):
        return str(self.bed_type) + " - " + str(self.bed_number)

class BedAllotment(models.Model):
    bed_number = models.CharField(max_length=30,blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    allotment_time = models.CharField(max_length=30)
    discharge_time = models.CharField(max_length=30)
    
    def __str__(self):
        return self.bed_number
    
   


class BloodBank(models.Model):
    blood_group = models.CharField(max_length=30)
    qty = models.CharField(max_length=30)
    def __str__(self):
        return self.blood_group

class BloodDonor(models.Model):
    blood_group = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    age = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=30)
    last_donation = models.CharField(max_length=30)
    
    
    def __str__(self):
        return self.name


########
class Medicine(models.Model):
    name = models.CharField(max_length=30)
    medicine_category = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    manufacturing_company = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Report(models.Model):
    REPORT_CHOICES = (
        (1,'Operation'),
        (2,'Birth'),
        (3,'Death')
    )
    report_type = models.PositiveSmallIntegerField(choices=REPORT_CHOICES)
    date = models.CharField(max_length=30)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=30)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.patient



####add appointment DOCTOR
class Appointment(models.Model):
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    notify = models.CharField(max_length=30)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.patient
        
####add prescription DOCTOR
class Prescription(models.Model):
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=30,blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    case_history = models.CharField(max_length=30)
    medication = models.CharField(max_length=30)
    note = models.CharField(max_length=30)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

####accountant
class Invoice(models.Model):
    title = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    creation_date = models.CharField(max_length=30)
    due_date = models.CharField(max_length=30)
    vat_percentage = models.CharField(max_length=30)
    discount_amount = models.CharField(max_length=30)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=10)
    description = models.CharField(max_length=30)
    amount = models.CharField(max_length=30)


   
class RequestedAppointment(models.Model):
    date = models.CharField(max_length=30)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor =  models.ForeignKey(Doctor, on_delete=models.CASCADE)

class DiagnosisReport(models.Model):
    report_type = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=3000)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=30)
    diagnosis_file = models.FileField(upload_to='media/')
    
    def __str__(self):
        return self.patient

# class ChatMessage(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     message = models.TextField(max_length=3000)
#     message_html = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):        
#         return self.message

# class Chat(models.Model):
#     DIALOG = 'D'
#     CHAT = 'C'
#     CHAT_TYPE_CHOICES = (
#         (DIALOG, _('Dialog')),
#         (CHAT, _('Chat'))
#     )
 
#     type = models.CharField(
#         _('Тип'),
#         max_length=1,
#         choices=CHAT_TYPE_CHOICES,
#         default=DIALOG
#     )
#     members = models.ManyToManyField(User, verbose_name=_("Member"))
 
#     @models.permalink
#     def get_absolute_url(self):
#         return 'users:messages', (), {'chat_id': self.pk }
 
 
# class Message(models.Model):
#     chat = models.ForeignKey(Chat, verbose_name=_("Chat"))
#     author = models.ForeignKey(User, verbose_name=_("User"))
#     message = models.TextField(_("Message"))
#     pub_date = models.DateTimeField(_('Message date'), default=timezone.now)
#     is_readed = models.BooleanField(_('Readed'), default=False)
 
#     class Meta:
#         ordering=['pub_date']
 
#     def __str__(self):
#         return self.message

class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser)

    # example functionality you may wish to add later
    group_name = models.CharField(max_length=512, default="Group", blank=False, null=False)
    profile_picture = models.FileField(upload_to='media/', default='uploads/user.jpg')

    
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="sender")
    # receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="receiver")
    receiver = models.ManyToManyField(CustomUser)
    message_content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    conversation = models.ForeignKey(Conversation, blank=False, null=False,on_delete=models.CASCADE)

    # ordering = ["-pub_date"]
 
    class Meta:
        ordering=['pub_date']
 
    def __str__(self):
        return self.message


