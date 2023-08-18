from rest_framework import viewsets, permissions, generics
from .serializers import PersonSerializer,  CsvFileSerializer, CsvRowSerializer, JoinSerializer, UserSerializer
import copy
from .models import Person, CsvFile, CsvRow
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import pandas as pd
from django.shortcuts import redirect
from django.db.models import Q
import requests
from django.http import QueryDict
from .utils import get_error_msg
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from django.db import transaction


# Create your views here.


class PersonViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def create(self, request, *args, **kwargs):
        try:
            duke_api_token = '38c02129fe1667fbc5c588b0d7a03708'
            mutable_data = request.data.copy()
            netid = request.data.get("netid")
            if netid:
                duke_api = (
                    "https://streamer.oit.duke.edu/ldap/people/netid/"
                    + netid
                    + "?access_token="
                    + duke_api_token
                )
                response = requests.get(duke_api)
                data = response.json()
                if response.status_code == 200 and len(data) > 0:
                    mutable_data["name"] = data[0]["display_name"]
                    mutable_data["email"] = data[0]["emails"][0]
                    mutable_data["unique_id"] = data[0]["duid"]
                    mutable_data["is_duke"] = True

            email = mutable_data.get("email")
            existing_person = Person.objects.filter(email=email).first()
            if existing_person:
                serializer = self.get_serializer(existing_person, data=mutable_data)
            else:
                serializer = self.get_serializer(data=mutable_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        except Exception as e:
            print("An error occurred:", str(e))


class CsvFileViewSet(viewsets.ModelViewSet):
    queryset = CsvFile.objects.all()
    serializer_class = CsvFileSerializer


class CsvRowViewSet(viewsets.ModelViewSet):
    queryset = CsvRow.objects.all()
    serializer_class = CsvRowSerializer


class JoinViewSet(viewsets.ModelViewSet):
    queryset = CsvRow.objects.all()
    serializer_class = JoinSerializer

    # @action(detail=False, method=['GET'])
    def list_by_person(self, request, people_id=None):
        grades = CsvRow.objects.filter(people__id=people_id)
        serializer = JoinSerializer(grades, many=True)
        return Response(serializer.data)


class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    @transaction.atomic
    def post(self, request, format=None):
        csv_file = request.FILES["file"]
        form_data = request.data

        course_name = form_data.get("courseName")
        overwriteConfirmation = form_data.get("overwriteConfirmation")

        # deal with csv duplication
        csvfile = CsvFile.objects.filter(csv_title=course_name).first()
        if csvfile:
            if overwriteConfirmation == "false":
                return Response(
                    {"message": "Duplicate CSV file upload", "duplicate": True}
                )
            elif overwriteConfirmation == "true":
                csvfile.delete()

        csvfile_serializer = CsvFileSerializer(data={"csv_title": course_name})
        if csvfile_serializer.is_valid():
            csvfile_serializer.save()
        else:
            return Response(csvfile_serializer.errors, status=400)

        csvfile = CsvFile.objects.filter(csv_title=course_name).first()
        people_use_api = []
        new_people = []
        old_people = []
        source = []
        is_existing = []

        duke_api_token = '38c02129fe1667fbc5c588b0d7a03708'

        print("form_data: ", form_data)

        # deal with csv for each row
        df = pd.read_csv(csv_file, na_filter=False)
        for index, row in df.iterrows():
            name = row.get(form_data.get("name").rstrip("\r\n"))
            email = row.get(form_data.get("email").rstrip("\r\n"))
            gmail = row.get(form_data.get("gmail").rstrip("\r\n"))
            netid = row.get(form_data.get("netid").rstrip("\r\n"))
            unique_id = row.get(form_data.get("unique_id").rstrip("\r\n"))
            grade = row.get(form_data.get("grade").rstrip("\r\n"))

            name = name if name else None
            email = email if email else None
            gmail = gmail if gmail else None
            netid = netid if netid else None
            unique_id = unique_id if unique_id else None
            grade = grade if grade else None

            is_duke = False
            useAPI = False
            is_updated = False

            initial_name = name
            initial_email = email
            initial_unique_id = unique_id

            # "csv" "api" ""
            person_source = {
                "name": "",
                "email": "",
                "gmail": "",
                "is_duke": "",
                "netid": "",
                "unique_id": "",
            }
            # "new" "update" ""
            person_is_existing = {
                "name": "",
                "email": "",
                "gmail": "",
                "is_duke": "",
                "netid": "",
                "unique_id": "",
            }

            old_person = None
            new_person = None

            if netid:
                duke_api = (
                    "https://streamer.oit.duke.edu/ldap/people/netid/"
                    + netid
                    + "?access_token="
                    + duke_api_token
                )
                response = requests.get(duke_api)
                data = response.json()
                if response.status_code == 200 and len(data) > 0:
                    name = data[0]["display_name"]
                    email = data[0]["emails"][0]
                    unique_id = data[0]["duid"]
                    is_duke = True

                    person_source["name"] = "api"
                    person_source["email"] = "api"
                    person_source["unique_id"] = "api"
                    person_source["is_duke"] = "api"
            if (
                name != initial_name
                or email != initial_email
                or unique_id != initial_unique_id
            ):
                useAPI = True

            person_data = {
                "name": name,
                "email": email,
                "gmail": gmail,
                "is_duke": is_duke,
                "netid": netid,
                "unique_id": unique_id,
            }

            print("person_data: ", person_data)

            netid_duke_email = netid + "@duke.edu"

            try:
                if netid:
                    person = Person.objects.get(netid=netid)
                elif email:
                    person = Person.objects.get(Q(email=email) | Q(email=netid_duke_email))
                elif name:
                    person = Person.objects.get(name=name)
                
                old_person = copy.deepcopy(person)
                
                for field in person_data:
                    if person_data[field] is None:
                        continue
                    elif getattr(person, field) is None:
                        person_is_existing[field] = "new"
                        person_source[field] = person_source[field] if person_source[field] else "csv"
                        is_updated = True
                    elif getattr(person, field) != person_data[field]:
                        person_is_existing[field] = "update"
                        person_source[field] = person_source[field] if person_source[field] else "csv"
                        is_updated = True

                new_person_serializer = PersonSerializer(person, data=person_data)
            
            except Person.DoesNotExist:
                for field in person_data:
                    if person_data[field] is not None:
                        person_is_existing[field] = "new"
                        person_source[field] = person_source[field] if person_source[field] else "csv"
                is_updated = True
                # update person and csvrow
                new_person_serializer = PersonSerializer(data=person_data)

            if new_person_serializer.is_valid():
                person = new_person_serializer.save()
                csvrow = CsvRow.objects.create(
                    course_name=csvfile, people=person, letter_grade=grade
                )
            else:
                csvfile.delete()
                print(new_person_serializer.errors)
                field, error_msg = get_error_msg(new_person_serializer.errors)
                error_data = new_person_serializer.data.get(field)
                column_name = form_data.get(field).rstrip("\r\n")
                return Response(
                    {
                        "field": column_name,
                        "error_msg": error_msg,
                        "index": index,
                        "error_data": error_data,
                    },
                    status=400,
                )
            
            new_person = person
            old_person = person if old_person is None else old_person

            if useAPI:
                people_use_api.append(person)
            
            if is_updated:
                new_people.append(new_person)
                old_people.append(old_person)
                source.append(person_source)
                is_existing.append(person_is_existing)

        people_use_api_serializer = PersonSerializer(people_use_api, many=True)
        new_people_serializer = PersonSerializer(new_people, many=True)
        old_people_serializer = PersonSerializer(old_people, many=True)

        print(new_people_serializer.data)
        print(old_people_serializer.data)
        print(source)
        print(is_existing)

        return Response(
            {
                "message": "CSV file uploaded and processed successfully!",
                "people_use_api": people_use_api_serializer.data,
                "new_people": new_people_serializer.data,
                "old_people": old_people_serializer.data,
                "source": source,
                "is_existing": is_existing,
            }
        )


class CsvFileViewSet(viewsets.ModelViewSet):
    queryset = CsvFile.objects.all()
    serializer_class = CsvFileSerializer
    # filter_backends = [Search]
    search_fields = ["csv_title"]


class KeywordSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword")

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(email__icontains=keyword)
                | Q(netid__icontains=keyword)
                | Q(unique_id__icontains=keyword)
                | Q(comments__icontains=keyword)
                | Q(gmail__icontains=keyword)
            ).distinct()

        return queryset

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class LoginView(APIView):
    #permission_classes = (permissions.AllowAny,)
    #authentication_classes = (SessionAuthentication,)
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        print("5")
        # if serializer.is_valid(raise_exception=True):
        print("4")
        username = request.data.get('username')
        password = request.data.get('password')
        print("3")
        user = authenticate(request, username=username, password=password)
        print("2")
        print(user)
        if user is not None:
            print("1")
            if user.is_active:
                login(request, user)
                return Response({'message': 'Login successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Your account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # permission_classes = (permissions.AllowAny,)
	# authentication_classes = (SessionAuthentication,)
	# ##
	# def post(self, request):
	# 	data = request.data
	# 	serializer = UserLoginSerializer(data=data)
	# 	if serializer.is_valid(raise_exception=True):
    #         username = request.data.get('username')
    #         password = request.data.get('password')
	# 		user = authenticate(request, username=username, password=password)
	# 		login(request, user)
	# 		return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response({'message': 'Logout successfully'}, status=status.HTTP_200_OK)

class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

def post_view(request):
    # Process the post request here

    # Redirect to the desired page
    return redirect("http://localhost:3000/")
