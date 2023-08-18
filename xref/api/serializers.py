from rest_framework import serializers
from .models import Person, CsvFile, CsvRow
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email')

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'email', 'gmail', 'is_duke', 'netid', 'unique_id', 'comments')

class CsvFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CsvFile
        fields = ('id', 'csv_title')

class CsvRowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CsvRow
        fields = ('id', 'course_name', 'people', 'letter_grade')

# grade serializer
class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name',)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvFile
        fields = ('csv_title',)

# class GradeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CsvRow
#         fields = ('people', 'letter_grade', 'course_name',)

class JoinSerializer(serializers.ModelSerializer):
    people = PeopleSerializer()
    course_name = CourseSerializer()

    class Meta:
        model = CsvRow
        fields = ('letter_grade', 'people', 'course_name',)

# class DetailSerializer(serializers.ModelSerializer):
#     course_name = CourseSerializer()
#     grade = GradeSerializer()

#     class Meta:
#         model = CsvRow
#         fields = ('id', 'grade','course_name',)