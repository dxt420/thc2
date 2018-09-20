# from . settings import LOGIN_REDIRECT_URL,LOGIN_URL
from django.contrib.auth.decorators import user_passes_test
from . models import Role

def admin_required(function=None):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_admin
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def doc_required(function=None):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_doctor
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def nurse_required(function=None):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == Role.NURSE
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def patient_required(function=None):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == Role.PATIENT
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def labaratorist_required(function=None):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == Role.LABARATORIST
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def accountant_required(function=None):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == Role.ACCOUNTANT
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def pharmacist_required(function=None):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == Role.PHARMACIST
    )
    if function:
        return actual_decorator(function)
    return actual_decorator