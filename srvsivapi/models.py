from django.db import models

MODEOFRECEIPTS = (
    ('PO','PO'),
    ('LOA','LOA'),
    ('MRN','MRN'),
    ('STV','STV'),
    ('MTN','MTN')
)

DEPARTMENTS = (
    ('HR','Human Resources'),
    ('SL1','SL1'),
    ('SL2','SL2'),
    ('CNM','Contracts and Materials'),
    ('FNA','Finance and Accounts'),
    ('SO1','SO1'),
    ('SO2','SO2')
)

class Employee(models.Model):
    emp_no = models.CharField( max_length=15 )
    name = models.CharField( max_length=50)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

class SRV(models.Model):
    mode_of_receipt = models.CharField(max_length = 10, choices=MODEOFRECEIPTS)
    indent_department = models.CharField(max_length = 10)
    remarks = models.CharField(max_length = 1000)
    name_supplier = models.CharField(max_length = 50)
    indent_ref_no = models.CharField(max_length = 50)
    indent_date = models.DateField(auto_now=False, auto_now_add=False)
    srvsiv_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    inspected_by = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='ins')
    inspected_countersigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='inscounter')
    received_by = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='receive')
    received_countersigned_by = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='receivecounter')

class Items(models.Model):
    description = models.CharField(max_length=100)
    received_qty = models.IntegerField()
    rejected_qty = models.IntegerField()
    unit_rate = models.FloatField()
    srv_id = models.ForeignKey(SRV, on_delete=models.CASCADE)

class SIV(models.Model):
    srv_id = models.ForeignKey(SRV, on_delete=models.CASCADE)
    issued_reason = models.CharField(max_length=1000)
    issued_to = models.ForeignKey(Employee, on_delete=models.CASCADE)


# Create your models here.
