from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
# from django.db import models
# models.get_models(include_auto_created=True)
from django.contrib import messages, auth

from . decorators import *
from . forms import CustomUserCreationForm, addPatientForm, addDepartmentForm, addDoctorForm, addAccountantForm, addNurseForm, addPharmacistForm, addLabaratoristForm, addReceptionistForm, addAppointmentForm, addInvoiceForm, addBloodDonorForm, createPayrollForm, addBedForm, addBedAllotmentForm, addPrescriptionForm, CustomUserCreationFormDoctor, CustomUserCreationFormNurse, CustomUserCreationFormPatient,CustomUserCreationFormReception,CustomUserCreationFormLabaratorist,CustomUserCreationFormAccountant,CustomUserCreationFormPharmacist,applyAppointmentForm,MessageForm
from . models import Patient, Department, Doctor, PaymentHistory, BedAllotment, BloodBank, Medicine, Appointment, Invoice, BloodDonor, Payroll, Bed, Prescription, CustomUser, RequestedAppointment,Employee,DiagnosisReport,Message

@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            doctors_count = Doctor.objects.all().count()
            patients_count = Patient.objects.all().count()
            nurses_count = CustomUser.objects.filter(is_nurse=True).count()
            pharmacist_count = CustomUser.objects.filter(
                is_pharmacist=True).count()
            labaratorist_count = CustomUser.objects.filter(
                is_labaratorist=True).count()
            accountant_count = CustomUser.objects.filter(
                is_accountant=True).count()

            context = {
                'doctors_count': doctors_count,
                'patients_count': patients_count,
                'nurses_count': nurses_count,
                'pharmacist_count': pharmacist_count,
                'labaratorist_count': labaratorist_count,
                'accountant_count': accountant_count,

            }
            
            return render(request, 'Hospital/admindash.html',context)
        if request.user.is_doctor:
           return render(request, 'Hospital/doctor/doctordash.html')
        if request.user.is_nurse:
           return render(request, 'Hospital/nurse/nursedash.html')
        if request.user.is_accountant:
           return render(request, 'Hospital/accountant/account_dash.html')
        if request.user.is_receptionist:
           return render(request, 'Hospital/reception/receptiondash.html')
        if request.user.is_labaratorist:
           return render(request, 'Hospital/labaratorist/labdash.html')
        if request.user.is_pharmacist:
           return render(request, 'Hospital/pharmacist/pharmdash.html')
        if request.user.is_patient:
            dms = Message.objects.filter(receiver=request.user)
            a = 0
            for dm in dms:
                if not dm.is_read:
                    a = a + 1
         
            context = {'dms':dms,'a':a}
            return render(request, 'Hospital/patient/patientdash.html',context)


    
    

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    messages.add_message(request, messages.INFO,
                         'You are Successfully Logged Out')
    messages.add_message(request, messages.INFO, 'Thanks for visiting.')
    return HttpResponseRedirect(reverse('Hospital:login'))


def login(request):
    if request.method == 'post':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.INFO,
                                 'Your are now Logged in.')
            return HttpResponseRedirect(reverse('Hospital:home'))
        else:
            context = {
                'errors':user.errors
            }
            return render(request, 'Hospital/registration/login.html',context)
    else:
        return render(request, 'Hospital/registration/login.html')


@login_required
@admin_required
def admindash(request):
    doctors_count = Doctor.objects.all().count()
    patients_count = Patient.objects.all().count()
    nurses_count = CustomUser.objects.filter(is_nurse=True).count()
    pharmacist_count = CustomUser.objects.filter(is_pharmacist=True).count()
    labaratorist_count = CustomUser.objects.filter(is_labaratorist=True).count()
    accountant_count = CustomUser.objects.filter(is_accountant=True).count()


    context = {
        'doctors_count': doctors_count,
        'patients_count': patients_count,
        'nurses_count': nurses_count,
        'pharmacist_count': pharmacist_count,
        'labaratorist_count': labaratorist_count,
        'accountant_count': accountant_count,

    }

    return render(request, 'Hospital/admindash.html', context)


def doctor(request):
    doctors = Doctor.objects.all()
    doctors_count = Doctor.objects.all().count()
    context = {
        'doctors': doctors,
        'doctors_count': doctors_count
    }
    return render(request, 'Hospital/doctor.html', context)


def department(request):
    departments = Department.objects.all()

    return render(request, 'Hospital/department.html', {'departments': departments})

@login_required
@admin_required
def accountant(request):
    accountants = CustomUser.objects.filter(is_accountant=True)

    return render(request, 'Hospital/accountant.html', {'accountants': accountants})

@login_required
@admin_required
def bedallotment(request):
    bedallotments = BedAllotment.objects.all()
    return render(request, 'Hospital/bedallotment.html', {'bedallotments': bedallotments})

@login_required
@admin_required
def birthreport(request):
    return render(request, 'Hospital/birthreport.html')

@login_required
@admin_required
def bloodbank(request):
    bloodbanks = BloodBank.objects.all()
    return render(request, 'Hospital/bloodbank.html', {'bloodbanks': bloodbanks})

@login_required
@admin_required
def blooddonor(request):
    blooddonors = BloodDonor.objects.all()
    return render(request, 'Hospital/blooddonor.html', {'blooddonors': blooddonors})


def contactemails(request):
    return render(request, 'Hospital/contactemails.html')

@login_required
@admin_required
def createpayroll(request):
    if request.method == 'POST':
        form = createPayrollForm(request.POST)

        if True:
            new_payroll = Payroll(
                employee=Employee.objects.get(pk=request.POST['employee']),
                month=request.POST['month'],
                year=request.POST['year'],
                basic=request.POST['basic'],
                total_allowance=request.POST['total_allowance'],
                total_deduction=request.POST['total_deduction'],
                net=request.POST['net_salary'],
                status=request.POST['status'],)

            new_payroll.save()
            messages.success(request, "aa")
            request.session['foo'] = 2
            return HttpResponseRedirect(reverse('Hospital:payrolllist'))

    else:
        form = createPayrollForm()
        context = {'form': form}
        return render(request, 'Hospital/createpayrollx.html', context)



def viewpayrolldetails(request, id):
    payroll = Payroll.objects.get(pk=id)
    context = {
        'payroll': payroll,
    }
    return render(request, 'Hospital/modals/payroll_list_details.html', context)

@login_required
@admin_required
def markpaid(request,id):
    mark_paid_object = Payroll.objects.get(pk=id)

    if mark_paid_object.status == 'paid':
        mark_paid_object.status = 'unpaid'
        mark_paid_object.save()

    messages.success(request, "aa")
    request.session['foo'] = 4
    return HttpResponseRedirect(reverse('Hospital:payrolllist'))

@login_required
@admin_required
def markunpaid(request,id):
    mark_paid_object = Payroll.objects.get(pk=id)

        
    if mark_paid_object.status == 'unpaid':
        mark_paid_object.status = 'paid'
        mark_paid_object.save()
        
    messages.success(request, "aa")
    request.session['foo'] = 4
    return HttpResponseRedirect(reverse('Hospital:payrolllist'))
    

@login_required
@admin_required
def deathreport(request):
    return render(request, 'Hospital/deathreport.html')


def department_facilities(request):
    return render(request, 'Hospital/department.html')


def frontend(request):
    return render(request, 'Hospital/frontendhome.html')

@login_required
@admin_required
def labaratorist(request):
    labaratorists = CustomUser.objects.filter(is_labaratorist=True)
    return render(request, 'Hospital/labaratorist.html', {'labaratorists': labaratorists})

@login_required
@admin_required
def manageprofile(request):
    admin = CustomUser.objects.filter(is_admin=True)
    form = CustomUserCreationFormDoctor()
    context = {
        'admin': admin,
        'form': form,

    }
    return render(request, 'Hospital/manageprofile.html',context)

@login_required
@admin_required
def medicine(request):
    return render(request, 'Hospital/medicine.html')


def noticeboard(request):
    return render(request, 'Hospital/noticeboard.html')

@login_required
@admin_required
def nurse(request):
    nurses = CustomUser.objects.filter(is_nurse=True)
    return render(request, 'Hospital/nurse.html', {'nurses': nurses})

@login_required
@admin_required
def operationreport(request):
    return render(request, 'Hospital/operationreport.html')


def patient(request):
    patients = Patient.objects.all()
    context = {'patients': patients}
    return render(request, 'Hospital/patient.html', context)

@login_required
@admin_required
def paymenthistory(request):
    paymenthistory = PaymentHistory.objects.all()
    return render(request, 'Hospital/paymenthistory.html', {'paymenthistory': paymenthistory})

@login_required
@admin_required
def payrolllist(request):
    payrolls = Payroll.objects.all()
    return render(request, 'Hospital/payrolllist.html', {'payrolls': payrolls})

@login_required
@admin_required
def pharmacist(request):
    pharmacists = CustomUser.objects.filter(is_pharmacist=True)
    return render(request, 'Hospital/pharmacy.html', {'pharmacists': pharmacists})

@login_required
@admin_required
def receptionist(request):
    receptionists = CustomUser.objects.filter(is_receptionist=True)
    return render(request, 'Hospital/receptionist.html', {'receptionists': receptionists})


def systemsettings(request):
    return render(request, 'Hospital/systemsettings.html')


def addpatientmodal(request):
    if request.method == 'POST':
        form = CustomUserCreationFormPatient(request.POST)

        if form.is_valid():
            patient = form.save()

            patient.blood_group = request.POST['blood_group']
            patient.sex = request.POST['sex']
            patient.dob = request.POST['dob']

            patient.save()
            patient.usericon = request.FILES['usericon']
            patient.save()
            user = patient.user
            user.usericon = request.FILES['usericon']
            user.save()
            messages.error(request, "Error in details")
            request.session['foo'] = 2
            return HttpResponseRedirect(reverse('Hospital:patient'))
        else:
            messages.error(request, "Error in details")
            request.session['foo'] = 1
            return HttpResponseRedirect(reverse('Hospital:patient'))

    else:
        form = CustomUserCreationFormPatient()
        context = {'form': form}
        return render(request, 'Hospital/modals/add_patient.html', context)

def addpatientmodalD(request):
    if request.method == 'POST':
        form = CustomUserCreationFormPatient(request.POST)

        if True:
            patient = form.save()

            patient.blood_group = request.POST['blood_group']
            patient.sex = request.POST['sex']
            patient.dob = request.POST['dob']

            patient.save()
            patient.usericon = request.FILES['usericon']
            patient.save()
            user = patient.user
            user.usericon = request.FILES['usericon']
            user.save()
            if request.user.is_doctor:
                return HttpResponseRedirect(reverse('Hospital:patientD'))
            if request.user.is_nurse:
                return HttpResponseRedirect(reverse('Hospital:patientN'))

    else:
        form = CustomUserCreationFormPatient()
        context = {'form': form}
        if request.user.is_doctor:
            return render(request, 'Hospital/doctor/modals/addpatient.html', context)
        if request.user.is_nurse:
            return render(request, 'Hospital/nurse/modals/addpatient.html', context)


def editappointmentmodal(request, id):
    appointment = Appointment.objects.get(pk=id)
    # patient = Patient.objects.get(=id)
    form = addAppointmentForm(initial = {'patient':appointment.patient.pk})
    context = {
        'appointment': appointment,
        'form': form,

    }

    return render(request, 'Hospital/doctor/modals/editappointment.html', context)

def editappointment(request):
    if request.method == 'POST':
        app_id = request.POST.get('did', None)
        appointment = Appointment.objects.get(pk=app_id)
        appointment.date = request.POST['date']
        appointment.time = request.POST['time']
        appointment.patient = get_object_or_404(Patient, pk=request.POST['patient'])
        appointment.notify = request.POST['notify']
        appointment.save()
        messages.success(request, "a")
        request.session['foo'] = 4
        return HttpResponseRedirect(reverse('Hospital:appointmentD'))



def editpatientmodal(request, pat_id):
    patient = Patient.objects.get(pk=pat_id)
    form = CustomUserCreationFormPatient()
    context = {
        'patient': patient,
        'form': form,

    }

    return render(request, 'Hospital/modals/edit_patient.html', context)

def editpatientmodalD(request, pat_id):
    patient = Patient.objects.get(pk=pat_id)
    form = CustomUserCreationFormPatient()
    context = {
        'patient': patient,
        'form': form,

    }

    return render(request, 'Hospital/doctor/modals/editpatient.html', context)

def editreceptionistmodal(request, id):
    receptionist = CustomUser.objects.get(pk=id)
    form = CustomUserCreationFormReception()
    context = {
        'receptionist': receptionist,
        'form': form,

    }
    return render(request, 'Hospital/modals/editreception.html', context)

def editaccountantmodal(request, id):
    accountant = CustomUser.objects.get(pk=id)
    form = CustomUserCreationFormAccountant()
    context = {
        'accountant': accountant,
        'form': form,

    }
    return render(request, 'Hospital/modals/editaccountant.html', context)

def editlabaratoristmodal(request, id):
    labaratorist = CustomUser.objects.get(pk=id)
    form = CustomUserCreationFormLabaratorist()
    context = {
        'labaratorist': labaratorist,
        'form': form,

    }
    return render(request, 'Hospital/modals/editlabaratorist.html', context)

def editpharmacistmodal(request, id):
    pharmacist = CustomUser.objects.get(pk=id)
    form = CustomUserCreationFormPharmacist()
    context = {
        'pharmacist': pharmacist,
        'form': form,

    }
    return render(request, 'Hospital/modals/editpharmacist.html', context)

def editpatient(request):
    if request.method == 'POST':

        pat_id = request.POST.get('did', None)
        patient = Patient.objects.get(pk=pat_id)
        user = patient.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.save()
        patient.sex = request.POST['sex']
        patient.dob = request.POST['dob']
        patient.blood_group = request.POST['blood_group']
        patient.save()
        if request.FILES:
            patient.usericon = request.FILES['usericon']
            patient.save()
        return HttpResponseRedirect(reverse('Hospital:patient'))

def editpatientD(request):
    if request.method == 'POST':

        pat_id = request.POST.get('did', None)
        patient = Patient.objects.get(pk=pat_id)
        user = patient.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.save()
        patient.sex = request.POST['sex']
        patient.dob = request.POST['dob']
        patient.blood_group = request.POST['blood_group']
        patient.save()
        if request.FILES:
            patient.usericon = request.FILES['usericon']
            patient.save()
        return HttpResponseRedirect(reverse('Hospital:patientD'))

def deletedepartment(request, id):
    dept = get_object_or_404(Department, pk=id).delete()
    messages.success(request, "a")
    request.session['foo'] = 3
    return HttpResponseRedirect(reverse('Hospital:department'))

def deletebed(request, id):
    bed = get_object_or_404(Bed, pk=id).delete()
    messages.success(request, "a")
    request.session['foo'] = 3
    return HttpResponseRedirect(reverse('Hospital:bed'))


def deleteappointment(request, id):
    get_object_or_404(Appointment, pk=id).delete()
    messages.success(request, "d")
    request.session['foo'] = 3
    return HttpResponseRedirect(reverse('Hospital:appointmentD'))

def deleteappointmentrequest(request, id):
    get_object_or_404(RequestedAppointment, pk=id).delete()
    messages.success(request, "d")
    request.session['foo'] = 3
    return HttpResponseRedirect(reverse('Hospital:appointmentrequestD'))
    

def deletedoctor(request, id):
    doc = get_object_or_404(Doctor, pk=id).delete()
    messages.success(request, "a")
    request.session['foo'] = 3
    return HttpResponseRedirect(reverse('Hospital:doctor'))


def deletepatient(request, id):
    get_object_or_404(CustomUser, pk=id).delete()
    messages.error(request, "Error in details")
    request.session['foo'] = 3
    if request.user.is_doctor and request.user.is_admin:
        return HttpResponseRedirect(reverse('Hospital:patient'))
    if request.user.is_doctor:
        return HttpResponseRedirect(reverse('Hospital:patientD'))

def deleteprescription(request, id):
    get_object_or_404(Prescription, pk=id).delete()
    messages.success(request, "a")
    request.session['foo'] = 3
    return HttpResponseRedirect(reverse('Hospital:prescriptionD'))

def deletenurse(request, id):
    get_object_or_404(CustomUser, pk=id).delete()
    return HttpResponseRedirect(reverse('Hospital:nurse'))
    
def deletereceptionist(request, id):
    get_object_or_404(CustomUser, pk=id).delete()
    return HttpResponseRedirect(reverse('Hospital:receptionist'))

def deleteaccountant(request, id):
    get_object_or_404(CustomUser, pk=id).delete()
    return HttpResponseRedirect(reverse('Hospital:accountant'))

def deletelabaratorist(request, id):
    get_object_or_404(CustomUser, pk=id).delete()
    return HttpResponseRedirect(reverse('Hospital:labaratorist'))

def deletepharmacist(request, id):
    get_object_or_404(CustomUser, pk=id).delete()
    return HttpResponseRedirect(reverse('Hospital:pharmacist'))
    


def editdepartment(request):

    if request.method == 'POST':

        dep_id = request.POST.get('did', None)
        department = Department.objects.get(pk=dep_id)
        department.departmentname = request.POST['departmentname']
        department.description = request.POST['description']
        department.save()
        if request.FILES:
            department.depticon = request.FILES['depticon']
            department.save()
        messages.success(request, "aa")
        request.session['foo'] = 4
        return HttpResponseRedirect(reverse('Hospital:department'))

    return render(request, 'Hospital/modals/edit_department.html', {'department': department})


def editdepartmentmodal(request, dep_id):
    department = Department.objects.get(pk=dep_id)
    return render(request, 'Hospital/modals/edit_department.html', {'department': department})


def editdoctormodal(request, doc_id):

    doctor = Doctor.objects.get(pk=doc_id)
    form = CustomUserCreationFormDoctor(initial = {'departmentname':doctor.departmentname})
    
    context = {
        'doctor': doctor,
        'form': form
    }

    return render(request, 'Hospital/modals/editdoctor.html', context)


def editbedmodal(request, bed_id):

    bed = Bed.objects.get(pk=bed_id)
    form = addBedForm(initial = {'departmentname':doctor.departmentname})
    
    context = {
        'bed': bed,
        'form': form
    }

    return render(request, 'Hospital/nurse/modals/editbed.html', context)


def editbed(request):
    if request.method == 'POST':
           bed_id = request.POST.get('did', None)
           bed = Bed.objects.get(pk=bed_id)
           bed.bed_number=request.POST['number'],
           bed.bed_type=request.POST['bed_type'],
           bed.description=request.POST['description']

           bed.save()
           return HttpResponseRedirect(reverse('Hospital:bed'))

def editdoctor(request):
    if request.method == 'POST':

        doc_id = request.POST.get('did', None)
        doctor = Doctor.objects.get(pk=doc_id)
        user = doctor.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.save()
        doctor.departmentname = request.POST['departmentname']
        doctor.save()
        if request.FILES:
            doctor.docicon = request.FILES['usericon']
            doctor.save()
        messages.success(request, "aa")
        request.session['foo'] = 4
        return HttpResponseRedirect(reverse('Hospital:doctor'))

    return render(request, 'Hospital/modals/editdoctor.html', {'doctor': doctor})


def editnursemodal(request, nur_id):

    nurse = CustomUser.objects.get(pk=nur_id)
    context = {

        'nurse': nurse,

    }

    return render(request, 'Hospital/modals/editnurse.html', context)


def editnurse(request):
    if request.method == 'POST':
        nur_id = request.POST.get('did', None)
        nurse = CustomUser.objects.get(pk=nur_id)
        nurse.first_name = request.POST['first_name']
        nurse.last_name = request.POST['last_name']
        nurse.email = request.POST['email']
        nurse.phone = request.POST['phone']
        nurse.save()
        if request.FILES:
            nurse.usericon = request.FILES['usericon']
            nurse.save()
        return HttpResponseRedirect(reverse('Hospital:nurse'))

    return render(request, 'Hospital/modals/editnurse.html', {'nurse': nurse})


def editreceptionist(request):
    if request.method == 'POST':
        rec_id = request.POST.get('did', None)
        receptionist = CustomUser.objects.get(pk=rec_id)
        receptionist.first_name = request.POST['first_name']
        receptionist.last_name = request.POST['last_name']
        receptionist.email = request.POST['email']
        receptionist.phone = request.POST['phone']
        receptionist.save()
        if request.FILES:
            receptionist.usericon = request.FILES['usericon']
            receptionist.save()
        return HttpResponseRedirect(reverse('Hospital:receptionist'))

 
def editlabaratorist(request):
    if request.method == 'POST':
        lab_id = request.POST.get('did', None)
        labaratorist = CustomUser.objects.get(pk=lab_id)
        labaratorist.first_name = request.POST['first_name']
        labaratorist.last_name = request.POST['last_name']
        labaratorist.email = request.POST['email']
        labaratorist.phone = request.POST['phone']
        labaratorist.save()
        if request.FILES:
            labaratorist.usericon = request.FILES['usericon']
            labaratorist.save()
        return HttpResponseRedirect(reverse('Hospital:labaratorist'))

def editaccountant(request):
    if request.method == 'POST':
        acc_id = request.POST.get('did', None)
        accountant = CustomUser.objects.get(pk=acc_id)
        accountant.first_name = request.POST['first_name']
        accountant.last_name = request.POST['last_name']
        accountant.email = request.POST['email']
        accountant.phone = request.POST['phone']
        accountant.save()
        if request.FILES:
            accountant.usericon = request.FILES['usericon']
            accountant.save()
        return HttpResponseRedirect(reverse('Hospital:accountant'))

def editpharmacist(request):
    if request.method == 'POST':
        pha_id = request.POST.get('did', None)
        pharmacist = CustomUser.objects.get(pk=pha_id)
        pharmacist.first_name = request.POST['first_name']
        pharmacist.last_name = request.POST['last_name']
        pharmacist.email = request.POST['email']
        pharmacist.phone = request.POST['phone']
        pharmacist.save()
        if request.FILES:
            pharmacist.usericon = request.FILES['usericon']
            pharmacist.save()
        return HttpResponseRedirect(reverse('Hospital:pharmacist'))


def adddepartmentmodal(request):
    form = addDepartmentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            new_dept = Department(
                departmentname=request.POST['departmentname'],
                description=request.POST['description'])
            new_dept.save()
            if request.FILES:
                new_dept.depticon=request.FILES['depticon']
                new_dept.save()
           
            messages.success(request, "a")
            request.session['foo'] = 2
            return HttpResponseRedirect(reverse('Hospital:department'))
        # else:
        #     messages.error(request, "Error in details")
        #     request.session['foo'] = 1
        #     return HttpResponseRedirect(reverse('Hospital:department'))

    context = {'form': form}
    return render(request, 'Hospital/newdept.html', context)


def adddoctormodal(request):
    form = CustomUserCreationFormDoctor(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        

        if form.is_valid():
            doctor = form.save()
            doctor.departmentname = request.POST['departmentname']
            doctor.save()
            if request.FILES:
                doctor.usericon = request.FILES['usericon']
                doctor.save()
                user = doctor.user
                user.usericon = request.FILES['usericon']
                user.save()
         
           
            messages.success(request, "Successfully added")
            request.session['foo'] = 2
            return HttpResponseRedirect(reverse('Hospital:doctor'))
        else:
            messages.error(request, "Error in details")
            request.session['foo'] = 1
            return HttpResponseRedirect(reverse('Hospital:doctor'))
            
    
    context = {'form': form}
    return render(request, 'Hospital/modals/add_doctor.html', context)



def addnursemodal(request):
    if request.method == 'POST':
        form = CustomUserCreationFormNurse(request.POST)

        if True:
            user = form.save()
            if request.FILES:
                user.usericon = request.FILES['usericon']
                user.save()
            user.phone = request.POST['phone']
            user.save()
            return HttpResponseRedirect(reverse('Hospital:nurse'))

    else:
        form = CustomUserCreationFormNurse()
        context = {'form': form}
        return render(request, 'Hospital/modals/add_nurse.html', context)


def addreceptionistmodal(request):
    if request.method == 'POST':
        form = CustomUserCreationFormReception(request.POST)

        if True:
            user = form.save()
            user.usericon = request.FILES['usericon']
            user.save()
            user.phone = request.POST['phone']
            user.save()
            return HttpResponseRedirect(reverse('Hospital:receptionist'))

    else:
        form = CustomUserCreationFormReception()
        context = {'form': form}
        return render(request, 'Hospital/modals/add_receptionist.html', context)

def addlabaratoristmodal(request):
    if request.method == 'POST':
        form = CustomUserCreationFormLabaratorist(request.POST)

        if True:
            user = form.save()
            user.usericon = request.FILES['usericon']
            user.save()
            user.phone = request.POST['phone']
            user.save()
            return HttpResponseRedirect(reverse('Hospital:labaratorist'))

    else:
        form = CustomUserCreationFormLabaratorist()
        context = {'form': form}
        return render(request, 'Hospital/modals/add_labaratorist.html', context)

def addpharmacistmodal(request):
    if request.method == 'POST':
        form = CustomUserCreationFormPharmacist(request.POST)

        if True:
            user = form.save()
            user.usericon = request.FILES['usericon']
            user.save()
            user.phone = request.POST['phone']
            user.save()
            return HttpResponseRedirect(reverse('Hospital:pharmacist'))

    else:
        form = CustomUserCreationFormPharmacist()
        context = {'form': form}
        return render(request, 'Hospital/modals/add_pharmacist.html', context)

def addaccountantmodal(request):
    if request.method == 'POST':
        form = CustomUserCreationFormAccountant(request.POST)

        if True:
            user = form.save()
            user.usericon = request.FILES['usericon']
            user.save()
            user.phone = request.POST['phone']
            user.save()
            return HttpResponseRedirect(reverse('Hospital:accountant'))

    else:
        form = CustomUserCreationFormAccountant()
        context = {'form': form}
        return render(request, 'Hospital/modals/add_accountant.html', context)






# DOCTOR
#



def patientD(request):
    patients = Patient.objects.all()
    dms = Message.objects.filter(receiver=request.user)

    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
    context = {'patients': patients,'a':a}
    return render(request, 'Hospital/doctor/patient.html', context)


@doc_required
def doctordash(request):
    dms = Message.objects.filter(receiver=request.user)

    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
         

    context = {'dms':dms,'a':a}
    return render(request, 'Hospital/doctor/doctordash.html',context)


def appointmentD(request):
    dms = Message.objects.filter(receiver=request.user)

    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
         

    
    appointments = Appointment.objects.filter(doctor=Doctor.objects.get(pk=request.user.id))
    context = {'appointments': appointments,'a':a}
    return render(request, 'Hospital/doctor/appointment.html', context)


def appointmentrequestD(request):
    dms = Message.objects.filter(receiver=request.user)

    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
    appointments = RequestedAppointment.objects.all()
    context = {'appointments':appointments,'a':a}
    return render(request, 'Hospital/doctor/appointment_request.html',context)


def approveappointment(request,id):
    approved = get_object_or_404(RequestedAppointment, pk=id)
    new_appointment = Appointment(
                date=approved.date,
                time='9:00',
                patient=approved.patient,
                notify=True,
                doctor=approved.doctor)

    new_appointment.save()
    approved.delete()
    return HttpResponseRedirect(reverse('Hospital:appointmentD'))
    
    

def appointmentpatient(request):
    dms = Message.objects.filter(receiver=request.user)

    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
         

    appointments = Appointment.objects.filter(patient=request.user.id)
    context = {'appointments': appointments,'dms':dms,'a':a}
    return render(request, 'Hospital/patient/appointment.html', context)

def pendingappointment(request):
    
    pendings = RequestedAppointment.objects.filter(patient=request.user.id)
    context = {'pendings': pendings}
    return render(request, 'Hospital/patient/appointment_pending.html', context)

def bedallotmentD(request):
       # patients = Patient.objects.all()
       # context = {'patients':patients}
    return render(request, 'Hospital/doctor/bedallotment.html')

def editprescriptionmodal(request,id):
    prescription = get_object_or_404(Prescription, pk=id)
    form = addPrescriptionForm(initial = {'patient':prescription.patient.pk})
    context = {
        'prescription': prescription,
        'form': form,

    }

    return render(request, 'Hospital/doctor/modals/editprescription.html', context)

def editprescription(request):
    if request.method == 'POST':
        pre_id = request.POST.get('did', None)
        prescription = Prescription.objects.get(pk=pre_id)
        prescription.date = request.POST['date']
        
        prescription.patient = get_object_or_404(Patient, pk=request.POST['patient'])
        prescription.case_history = request.POST['case_history']
        prescription.medication = request.POST['medication']
        prescription.note = request.POST['note']
        prescription.save()
        messages.success(request, "aa")
        request.session['foo'] = 4
        return HttpResponseRedirect(reverse('Hospital:prescriptionD'))
  
    

def bloodbankD(request):
    bloodbanks = BloodBank.objects.all()
    return render(request, 'Hospital/doctor/bloodbank.html', {'bloodbanks': bloodbanks})


def medicationhistoryD(request):
       # patients = Patient.objects.all()
       # context = {'patients':patients}
    return render(request, 'Hospital/doctor/medicationhistory.html')


def payrolllistD(request):
    dms = Message.objects.filter(receiver=request.user)

    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
    payrolls = Payroll.objects.filter(employee=Employee.objects.get(pk=request.user))
    context = {'payrolls':payrolls,'a':a}
    return render(request, 'Hospital/doctor/payrolllist.html',context)


def pmnewD(request):
    if request.method == 'POST':
            form = MessageForm(request.POST)

    
            if form.is_valid():
                new_message = form.save()
                new_message.sender = CustomUser.objects.get(pk=request.user.id)
                new_message.save()
                if request.user.is_doctor and request.user.is_active:
                    return HttpResponseRedirect(reverse('Hospital:pmD'))
                if request.user.is_patient and request.user.is_active:
                    return HttpResponseRedirect(reverse('Hospital:messageP'))

            else:
                context = {'form': form}
                if request.user.is_doctor:
                    return render(request, 'Hospital/doctor/pm_new.html',context)
                if request.user.is_patient:
                    return render(request, 'Hospital/patient/pm_read.html',context)

    else:
        form = MessageForm()
        dms = Message.objects.filter(receiver=request.user)
        context = {'form': form,'dms':dms}
        if request.user.is_doctor:
            return render(request, 'Hospital/doctor/pm_new.html',context)
        if request.user.is_patient:
            return render(request, 'Hospital/patient/pm_new.html',context)

def pmD(request):
    # get the conversations the user is in
    conversations = Message.objects.filter(conversation__participants=request.user).order_by('-date')
    dms = conversations.values('conversation').annotate(
        first_msg=Max('conversation__message')
    )

    a = 0
    for conversation in conversations:
        if not conversation.is_read:
            a = a + 1
         

    context = {'dms':dms,'a':a}



    return render(request, 'Hospital/doctor/pm.html',context)

def pmDd(request,id):
    dms = Message.objects.filter(receiver=request.user)
    m = Message.objects.get(id=id)
    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
    context = {'dms':dms,'m':m,'a':a}
    return render(request, 'Hospital/doctor/pm.html',context)

def prescriptionD(request):
    dms = Message.objects.filter(receiver=request.user)
    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
    prescriptions = Prescription.objects.all()
    context = {'prescriptions':prescriptions,'a':a}
    return render(request, 'Hospital/doctor/prescription.html',context)

def prescriptionpatient(request):
    prescriptions = Prescription.objects.filter(patient=request.user.id)
    context = {'prescriptions':prescriptions}
    return render(request, 'Hospital/patient/prescription.html',context)

def doctorpatient(request):
    doctors = Doctor.objects.all()
    return render(request, 'Hospital/patient/doctor.html',{'doctors':doctors})

def profileD(request):
       # patients = Patient.objects.all()
       # context = {'patients':patients}
    return render(request, 'Hospital/doctor/profile.html')


def reportD(request):
       # patients = Patient.objects.all()
       # context = {'patients':patients}
    return render(request, 'Hospital/doctor/report.html')

# doctor modals 


def addappointmentD(request):
    if request.method == 'POST':
        form = addAppointmentForm(request.POST)

        if True:
            new_appointment = Appointment(
                date=request.POST['date'],
                time=request.POST['time'],
                patient=Patient.objects.get(pk=request.POST['patient']),
                notify=request.POST['notify'],
                doctor=Doctor.objects.get(pk=request.user.id))

            new_appointment.save()
            messages.success(request, "d")
            request.session['foo'] = 2
            return HttpResponseRedirect(reverse('Hospital:appointmentD'))

    else:
        form = addAppointmentForm()
        context = {'form': form}
        return render(request, 'Hospital/doctor/modals/addappointment.html', context)


def addbedallotmentD(request):
    if request.method == 'POST':
        form = addBedAllotmentForm(request.POST)

        if True:
            new_bedallotment = BedAllotment(
                bed_number=request.POST['bed_number'],
                patient=request.POST['patient'],
                allotment_time=request.POST['allotment_time'],
                discharge_time=request.POST['discharge_time'],)

            new_bedallotment.save()
            return HttpResponseRedirect(reverse('Hospital:bedallotmentD'))

    else:
        # form = addBedAllotmentForm()
        # context = {'form':form}
        return render(request, 'Hospital/doctor/modals/addbedallotment.html')


def addpatientD(request):
    if request.method == 'POST':
        form = addPatientForm(request.POST)

        if True:
            new_patient = Patient(
                name=request.POST['name'],
                email=request.POST['email'],
                dob=request.POST['dob'],
                age=request.POST['age'],
                address=request.POST['address'],
                phone=request.POST['phone'],
                sex=request.POST['sex'],
                blood_group=request.POST['blood'],)

            new_patient.save()

         
            return HttpResponseRedirect(reverse('Hospital:patientD'))

    else:
        form = addPatientForm()
        context = {'form': form}
        return render(request, 'Hospital/doctor/modals/addpatient.html', context)


def addprescriptionD(request):
    if request.method == 'POST':
        form = addPrescriptionForm(request.POST)

        if True:
            new_prescription = Prescription(
                date=request.POST['date'],
                time=request.POST['time'],
                doctor=Doctor.objects.get(pk=request.user.id),
                patient=Patient.objects.get(pk=request.POST['patient']),
                case_history=request.POST['case_history'],
                medication=request.POST['medication'],
                note=request.POST['note'])

            new_prescription.save()
            messages.success(request, "aa")
            request.session['foo'] = 2
            return HttpResponseRedirect(reverse('Hospital:prescriptionD'))

    else:
        form = addPrescriptionForm()
        context = {'form': form}
        return render(request, 'Hospital/doctor/modals/addprescription.html', context)


def addreportD(request):
       # patients = Patient.objects.all()
       # context = {'patients':patients}
    return render(request, 'Hospital/doctor/modals/addreport.html')


def viewdiagnosisreportD(request,id):
    diags = DiagnosisReport.objects.filter(patient=id)
    context = {'diags':diags}
    return render(request, 'Hospital/doctor/modals/viewdiagnosisreport.html')

def viewdiagnosisreportDD(request):
    if request.method == 'post':
        if True:

            new_diagnosis = DiagnosisReport(
                    date=request.POST['date'],
                    time=request.POST['time'],
                    doctor=Doctor.objects.get(pk=request.user.id),
                    patient=Patient.objects.get(pk=request.POST['patient']),
                    report_type=request.POST['report_type'],
                    description=request.POST['description'],
                    doc_type=request.POST['doc_type'],
                    diagnosis_file=request.POST['file_name'])

            new_diagnosis.save()
            return HttpResponseRedirect(reverse('Hospital:prescriptionD'))
    


def viewpayrolldetailsD(request):
       # patients = Patient.objects.all()
       # context = {'patients':patients}
    return render(request, 'Hospital/doctor/modals/viewpayrolldetails.html')


def viewprescriptionD(request,id):
    prescription = Prescription.objects.get(pk=id)
    context = {'prescription':prescription}
    return render(request, 'Hospital/doctor/modals/viewprescription.html',context)


def viewprofileD(request, patientID):
    patient = Patient.objects.get(pk=patientID)
    context = {
        'patient': patient}
    return render(request, 'Hospital/doctor/modals/viewprofile.html', context)


def viewreportfilesD(request, patientID):

       # context = {'patients':patients}
    return render(request, 'Hospital/doctor/modals/viewreportfiles.html')


# ACOUNTANT
def accountdash(request):
    return render(request, 'Hospital/accountant/account_dash.html')


def invoice(request):
    if request.method == 'POST':
        form = addInvoiceForm(request.POST)

        if True:
            new_invoice = Invoice(
                title=request.POST['title'],
                number=request.POST['invoicenum'],
                patient=Patient.objects.get(pk=request.POST['patient']),
                creation_date=request.POST['creationdate'],
                due_date=request.POST['duedate'],
                vat_percentage=request.POST['vatpercent'],
                discount_amount=request.POST['discount'],
                payment_status=request.POST['status'],)

            new_invoice.save()
            return HttpResponseRedirect(reverse('Hospital:invoicemanage'))

    else:

        in_num = Invoice.objects.all().count()
        form = addInvoiceForm()
        form.fields['invoicenum'].initial = in_num + 1000
        context = {'form': form}
        return render(request, 'Hospital/accountant/invoice.html', context)


def invoicemanage(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'Hospital/accountant/invoice_manage.html', context)


def profileA(request):
    return render(request, 'Hospital/accountant/profile.html')


# LABARATORIST
def labdash(request):
    return render(request, 'Hospital/labaratorist/labdash.html')


def bloodbankL(request):
    bloodbanks = BloodBank.objects.all()
    return render(request, 'Hospital/labaratorist/bloodbank.html', {'bloodbanks': bloodbanks})


def blooddonorL(request):
    blooddonors = BloodDonor.objects.all()
    return render(request, 'Hospital/labaratorist/blooddonor.html', {'blooddonors': blooddonors})


def addblooddonormodal(request):
    if request.method == 'POST':
        form = addBloodDonorForm(request.POST)

        if True:
            new_blooddonor = BloodDonor(
                blood_group=request.POST['blood'],
                email=request.POST['email'],
                address=request.POST['address'],
                phone=request.POST['phone'],
                name=request.POST['name'],
                age=request.POST['age'],
                sex=request.POST['sex'],
                last_donation=request.POST['last_donation'],)

            new_blooddonor.save()
            return HttpResponseRedirect(reverse('Hospital:blooddonorL'))
    else:
        form = addBloodDonorForm()
        context = {'form': form}
        return render(request, 'Hospital/labaratorist/modals/addblooddonor.html', context)


def payrollL(request):
    return render(request, 'Hospital/labaratorist/payrolllist.html')


def profileL(request):
    return render(request, 'Hospital/labaratorist/profile.html')

# nurse


def nursedash(request):
    return render(request, 'Hospital/nurse/nursedash.html')


def bedallotmentN(request):
    bedallotments = BedAllotment.objects.all()
    return render(request, 'Hospital/nurse/bedallotment.html', {'bedallotments': bedallotments})


def addbedallotmentN(request):
    if request.method == 'POST':
        form = addBedAllotmentForm(request.POST)

        if True:
            new_bedallotment = BedAllotment(
                bed_number=request.POST['bed_number'],
                patient=Patient.objects.get(pk=request.POST['patient']),
                allotment_time=request.POST['allotment_time'],
                discharge_time=request.POST['discharge_time'],)

            new_bedallotment.save()
            return HttpResponseRedirect(reverse('Hospital:bedallotmentN'))

    else:
        form = addBedAllotmentForm()
        context = {'form': form}
        return render(request, 'Hospital/nurse/modals/addbedallotment.html', context)


def patientN(request):
    patients = Patient.objects.all()
    context = {'patients': patients}
    return render(request, 'Hospital/nurse/patient.html', context)


def addpatientN(request):
    if request.method == 'POST':
        form = addPatientForm(request.POST)

        if True:
            new_patient = Patient(
                name=request.POST['name'],
                email=request.POST['email'],
                dob=request.POST['dob'],
                age=request.POST['age'],
                address=request.POST['address'],
                phone=request.POST['phone'],
                sex=request.POST['sex'],
                blood_group=request.POST['blood'],)

            new_patient.save()
            return HttpResponseRedirect(reverse('Hospital:patientN'))

    else:
        form = addPatientForm()
        context = {'form': form}
        return render(request, 'Hospital/nurse/modals/addpatient.html', context)


def reportN(request):
    bloodbanks = BloodBank.objects.all()
    return render(request, 'Hospital/nurse/report.html', {'bloodbanks': bloodbanks})


def addreportmodalN(request):
    bloodbanks = BloodBank.objects.all()
    return render(request, 'Hospital/nurse/bloodbank.html', {'bloodbanks': bloodbanks})


def bed(request):
    beds = Bed.objects.all()
    return render(request, 'Hospital/nurse/bed.html', {'beds': beds})


def addbed(request):
    if request.method == 'POST':
        form = addBedForm(request.POST)

        if True:
            new_bed = Bed(
                bed_number=request.POST['number'],
                bed_type=request.POST['bed_type'],
                description=request.POST['description'],)

            new_bed.save()
            return HttpResponseRedirect(reverse('Hospital:bed'))

    else:
        form = addBedForm()
        context = {'form': form}
        return render(request, 'Hospital/nurse/modals/addbed.html', context)


def bloodbankN(request):
    bloodbanks = BloodBank.objects.all()
    return render(request, 'Hospital/nurse/bloodbank.html', {'bloodbanks': bloodbanks})


def blooddonorN(request):
    blooddonors = BloodDonor.objects.all()
    return render(request, 'Hospital/nurse/blooddonor.html', {'blooddonors': blooddonors})


def addblooddonormodalN(request):
    if request.method == 'POST':
        form = addBloodDonorForm(request.POST)

        if True:
            new_blooddonor = BloodDonor(
                blood_group=request.POST['blood'],
                email=request.POST['email'],
                address=request.POST['address'],
                phone=request.POST['phone'],
                name=request.POST['name'],
                age=request.POST['age'],
                sex=request.POST['sex'],
                last_donation=request.POST['last_donation'],)

            new_blooddonor.save()
            return HttpResponseRedirect(reverse('Hospital:blooddonorN'))
    else:
        form = addBloodDonorForm()
        context = {'form': form}
        return render(request, 'Hospital/nurse/modals/addblooddonor.html', context)


def payrollN(request):
    payrolls = Payroll.objects.filter(employee=Employee.objects.get(pk=request.user))
    context = {'payrolls':payrolls}
    return render(request, 'Hospital/nurse/payrolllist.html',context)


def profileN(request):
    return render(request, 'Hospital/nurse/profile.html')

def invoiceP(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'Hospital/patient/invoice.html',context)

def profileP(request):
    return render(request, 'Hospital/patient/profile.html')

def messageP(request):
    dms = Message.objects.filter(receiver=request.user)
    # dmcount = Message.objects.filter(receiver=request.user).count()
    a = 0
    for dm in dms:
        if not dm.is_read:
            a = a + 1
         
    context = {'dms':dms,'a':a}
    return render(request, 'Hospital/patient/pm.html',context)




def messagepD(request,id):
    dms = Message.objects.filter(receiver=request.user)
    m = Message.objects.get(id=id)
    m.is_read = True
    m.save()
    context = {'dms':dms,'m':m}
    
    # return render(request, 'Hospital/patient/pm.html',context)
    if request.user.is_patient:
        return render(request, 'Hospital/patient/pm_read.html',context)
    if request.user.is_doctor:
        return render(request, 'Hospital/doctor/pm_read.html',context)


def applyappointment(request):
    if request.method == 'POST':
            form = applyAppointmentForm(request.POST)

            if True:
                new_appointment = RequestedAppointment(
                    date=request.POST['date'],
                    patient=Patient.objects.get(pk=request.user.id),
                    doctor=Doctor.objects.get(pk=request.POST['doctor']))

                new_appointment.save()
                messages.error(request, "Error in details")
                request.session['foo'] = 2
                return HttpResponseRedirect(reverse('Hospital:pendingappointment'))

    else:
            form = applyAppointmentForm()
            context = {'form': form}
            return render(request, 'Hospital/patient/modals/applyappointment.html', context)




def viewdocprofile(request, id):
    doctor = Doctor.objects.get(pk=id)
    context = {
        'doctor': doctor,
    }
    return render(request, 'Hospital/patient/modals/viewdocprofile.html', context)




   
def newdept(request):
    return render(request, 'Hospital/newdept.html')


def newpat(request):
    form = CustomUserCreationFormPatient(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            patient = form.save()

            patient.blood_group = request.POST['blood_group']
            patient.sex = request.POST['sex']
            patient.dob = request.POST['dob']

            patient.save()
            patient.usericon = request.FILES['usericon']
            patient.save()
            user = patient.user
            user.usericon = request.FILES['usericon']
            user.save()
            messages.error(request, "Error in details")
            request.session['foo'] = 2
            if request.user.is_doctor:
                return HttpResponseRedirect(reverse('Hospital:patientD'))
            if request.user.is_nurse:
                return HttpResponseRedirect(reverse('Hospital:patientN'))
            if request.user.is_admin:
                return HttpResponseRedirect(reverse('Hospital:patient'))
        else:
            messages.error(request, "Error in details")
            request.session['foo'] = 1
            context = {'form': form}
            if request.user.is_doctor:
                return render(request, 'Hospital/doctor/newpat.html',context)
            if request.user.is_nurse:
                return render(request, 'Hospital/nurse/newpat.html',context)
            if request.user.is_admin:
                return render(request, 'Hospital/newpat.html',context)
            

    else:
        context = {'form': form}
        if request.user.is_doctor:
            return render(request, 'Hospital/doctor/newpat.html',context)
        if request.user.is_nurse:
            return render(request, 'Hospital/nurse/newpat.html',context)
        if request.user.is_admin:
            return render(request, 'Hospital/newpat.html',context)

   
def newdoc(request):
    form = CustomUserCreationFormDoctor(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        

        if form.is_valid():
            doctor = form.save()
            doctor.departmentname = request.POST['departmentname']
            doctor.save()
            if request.FILES:
                doctor.usericon = request.FILES['usericon']
                doctor.save()
                user = doctor.user
                user.usericon = request.FILES['usericon']
                user.save()
         
           
            messages.success(request, "Successfully added")
            request.session['foo'] = 2
            return HttpResponseRedirect(reverse('Hospital:doctor'))
        else:
            context = {'form': form}
            return render(request, 'Hospital/newdoc.html',context)

    else:
        context = {'form': form}
        return render(request, 'Hospital/newdoc.html',context)

   
    
