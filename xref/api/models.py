from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, null=True, unique=True)
    gmail = models.EmailField(max_length=254, null=True, unique=True)
    is_duke = models.BooleanField()
    netid = models.CharField(max_length=20, null=True, blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
    comments = models.TextField(blank=True)

class CsvFile(models.Model):
    csv_title = models.CharField(max_length=254, unique=True)    # user manually enter course name

class CsvRow(models.Model):
    people = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    course_name = models.ForeignKey(CsvFile, on_delete=models.CASCADE)
    letter_grade = models.CharField(max_length=10, null=True)