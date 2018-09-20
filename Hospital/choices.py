import datetime


GENDER_CHOICES = (
    ('male','Male'),
    ('female','Female'),
)

BLOOD_GROUPS = (
    ('A+','A+'),
    ('A-','A-'),
    ('B+','B+'),
    ('B-','B-'),
    ('AB+','AB+'),
    ('AB-','AB-'),
    ('O+','O+'),
    ('O-','O-'),
)

    
PAYMENT_STATUS = (
    ('paid','Paid'),
    ('unpaid','Unpaid'),
)

BED_TYPES = (
    ('Ward','Ward'),
    ('Cabin','Cabin'),
    ('ICU','ICU'),
)

MONTHS = (
    ('January','January'),
    ('February','February'),
    ('March','March'),
    ('April','April'),
    ('May','May'),
    ('June','June'),
    ('July','July'),
    ('August','August'),
    ('September','September'),
    ('October','October'),
    ('November','November'),
    ('December','December'),
)

YEAR_CHOICES = [(r,r) for r in range(2018,datetime.date.today().year+6)]                 
  