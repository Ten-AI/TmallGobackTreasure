from django.test import TestCase

# Create your tests here.


for i in range(99):
    print("<option value='%d'>%.2f</option>" % (i,float(i)/100))