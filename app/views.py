import mimetypes
import os
from rest_framework.decorators import api_view
# Create your views here.
from .models import *
from .serializers import *
from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import exceptions
from app.utils import generate_access_token, generate_refresh_token
from rest_framework.generics import (ListCreateAPIView)
from django.core.mail import send_mail  
from rest_framework import status
from rest_framework import generics

@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):

    Email = request.data.get('Email')
    Password = request.data.get('Password')
    response = Response()
    if (Email is None) or (Password is None):
        return Response({'message' : 'Email or Password is invalid'})
        # raise exceptions.AuthenticationFailed(
        #     'email and password required')

    user = User.objects.filter(Email=Email).first()
    user = User.objects.filter(Password=Password).first()
    admin = Recruiters.objects.filter(Email=Email).first()
    admin = Recruiters.objects.filter(Password=Password).first()
    if User.objects.filter(Email=Email).exists():
        if(user is None):
            return Response({'message' : 'Email or Password is invalid'})


        serialized_user = UserSerializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'status': 'success',
            'access_token': access_token,
            'user': serialized_user,
        }

        return response
    
    if Recruiters.objects.filter(Email=Email).exists():
        if(admin is None):
            return Response({'message' : 'Email or Password is invalid'})


        serialized_user = RecruiterSerializer(admin).data

        access_token = generate_access_token(admin)
        refresh_token = generate_refresh_token(admin)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
          'status': 'success',
          'access_token': access_token,
         'user': serialized_user,
        }

        return response
    
    return Response({
        'message' : "User does not exist"
    })


class UserAPIView(APIView):
    permission_classes = ([AllowAny])

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return Http404

    def get(self, request, id=None, format=None):
        if id:
            data = self.get_object(id)
            serializer = UserSerializer(data)
            return Response(serializer.data)
        else:
            data = User.objects.all().order_by('-id')
            serializer = UserSerializer(data, many=True)
            return Response(serializer.data)
                 
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()

        UserName = user.data.get('UserName')
        Password = user.data.get('Password')
        email = request.data['Email']
        subject = 'Mail From Hiera'
        message = 'Your Credentials are: UserName = '+str(UserName) + '   Password = '+str(Password)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message=message, from_email=from_email, recipient_list=recipient_list)
 
        return Response({
            'message' : 'Admin created successfully',
            'data' : user.data
        })
        
        
class RetrieveUpdateDestroyAPIView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)
    def put(self, request, id=None, format=None):
        user = User.objects.get(id=id)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message' : 'Admin updated successfully',
            'data' : serializer.data
        })

    def delete(self, request, id, format=None):
        user = User.objects.get(id=id)
        user.delete()
        return Response({
            'message' : 'Admin deleted successfully'
        })
        
        
class RecruiterAPIView(APIView):
    permission_classes = ([AllowAny])
    def get_object(self, id):
        try:
            return Recruiters.objects.get(id=id)
        except Recruiters.DoesNotExist:
            return Http404
        
    def get(self, request, id = None, format=None):
        if id:
            data = self.get_object(id)
            serializer = RecruiterSerializer(data)
            return Response(serializer.data)
        else:
            data = Recruiters.objects.all().order_by('-id')
            serializer = RecruiterSerializer(data, many=True)
            return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        recruiter =RecruiterSerializer(data=request.data)
        recruiter.is_valid(raise_exception=True)
        recruiter.save()
        
        UserName = recruiter.data.get('UserName')
        Password = recruiter.data.get('Password')
        email = request.data['Email']
        subject = 'Mail From Hiera'
        message = 'Your Credentials are: UserName = '+str(UserName) + '   Password = '+str(Password)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message=message, from_email=from_email, recipient_list=recipient_list)

        return Response({
            'message' : 'Recruiter created successfully',
            'data' : recruiter.data,
        })
        
        
class RetrieveUpdateDestroyAPIViews(APIView):
    permission_classes = (AllowAny,)
    def put(self, request, id=None,format=None):
        recruiter = Recruiters.objects.get(id=id)
        serializer = RecruiterSerializer(instance=recruiter, data=request.data,partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message' : 'Recruiter updated successfully',
            'data' : serializer.data
        })
        
    def delete(self, request, id, format=None):
        recruiter = Recruiters.objects.get(id=id)
        recruiter.delete()
        return Response({
            'message' : 'Recruiter deleted successfully.'
        })


class UserAPIViews(ListCreateAPIView):
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['UserName']
    
    filterset_fields = ['id', 'UserName']
    search_fields = ['id', 'UserName']
    
    def get_queryset(self):
        return User.objects.filter().order_by('UserName')


class RecruiterAPIViews(ListCreateAPIView):
    serializer_class = RecruiterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['UserName']
    
    filterset_fields = [ 'UserName']
    search_fields = [ 'UserName']
    
    def get_queryset(self):
        return Recruiters.objects.filter().order_by('UserName')


class FileUploadAPIViews(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FileUploadDisplaySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id','location', 'experience','company','designation']
    
    filterset_fields = ['id','location', 'experience','company','designation']
    # search_fields = ['id','location']
    
    def get_queryset(self):
        return FileUpload.objects.filter().order_by('id')


# class UpdatePassword(APIView):
#     """
#     An endpoint for changing password.
#     """
#     permission_classes = (IsAuthenticated, )

#     def get_object(self, queryset=None):
#         return self.request.user

#     def put(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = ChangePasswordSerializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             oldpassword = serializer.data.get("oldpassword")
#             if not User.objects.filter(Password=oldpassword):
#                 return Response({"oldpassword": ["Wrong password."]}, 
#                                 status=status.HTTP_400_BAD_REQUEST)
#             user = self.get_object()
#             newpassword = serializer.data['newpassword']
#             user.Password = newpassword
#             user.save()
#             return Response({'message':'password changed successfully'}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdatePasswords(APIView):
#     """
#     An endpoint for changing password.
#     """
#     permission_classes = (IsAuthenticated, IsAdminUser )

#     def get_object(self, queryset=None):
#         return self.request.user

#     def put(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = RecChangePasswordSerializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             oldpassword = serializer.data.get("oldpassword")
#             if not Recruiters.objects.filter(Password=oldpassword):
#                 return Response({"oldpassword": ["Wrong password."]}, 
#                                 status=status.HTTP_400_BAD_REQUEST)
#             recruiter = self.get_object()
#             newpassword = serializer.data['newpassword']
#             recruiter.Password = newpassword
#             recruiter.save()
#             return Response({'message':'password changed successfully'}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = AdminChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            oldpassword = serializer.data.get("oldpassword")
            if not User.objects.filter(Password=oldpassword):
                return Response({"oldpassword": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            user = self.get_object()
            newpassword = serializer.data['newpassword']
            user.Password = newpassword
            user.save()
            # return Response(user)
            return Response({'message':'password changed successfully'}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswords(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated, IsAdminUser )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = RecruiterChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            oldpassword = serializer.data.get("oldpassword")
            if not Recruiters.objects.filter(Password=oldpassword):
                return Response({"oldpassword": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            recruiter = self.get_object()
            newpassword = serializer.data['newpassword']
            recruiter.Password = newpassword
            # self.object.set_password(serializer.data.get("newpassword"))
            recruiter.save()
            # return Response(user)
            return Response({'message':'password changed successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([AllowAny])
def changepassword(request):
    
    data = request.data
    Email = data['Email']
    user = User.objects.filter(Email=Email).first()
    recruiter = Recruiters.objects.filter(Email=Email).first()

    if user:
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        Otp = serializer.data['otp']
        if User.objects.filter(Email=Email).exists():
           subject = 'Mail From Hiera'
           message = 'Your otp is: ' + str(Otp)
           from_email = settings.EMAIL_HOST_USER
           recipient_list = [Email]

           send_mail(subject, message=message, from_email=from_email, recipient_list=recipient_list)

        message = {
                 'detail': 'Success Message',
                 'data': serializer.data}
        return Response(message, status=status.HTTP_200_OK)

    if recruiter:
        serializer = RecruiterSerializer(instance=recruiter, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        Otp = serializer.data['otp']
        if Recruiters.objects.filter(Email=Email).exists():
           subject = 'Mail From Hiera'
           message = 'Your otp is: ' + str(Otp)
           from_email = settings.EMAIL_HOST_USER
           recipient_list = [Email]

           send_mail(subject, message=message, from_email=from_email, recipient_list=recipient_list)

        message = {
                 'detail': 'Success Message',
                 'data': serializer.data}
        return Response(message, status=status.HTTP_200_OK)

    else:
        message = {
            'detail': 'Given Email does not exists....'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([AllowAny])
def reset_request(request):
    
    serializer = resetpasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    Email = serializer.data['Email']

    user = User.objects.filter(Email=Email).first()
    recruiter = Recruiters.objects.filter(Email=Email).first()

    if user:
        
        if User.objects.filter(Email=Email).exists():
            newpassword = serializer.data['newpassword']
            confirmpassword = serializer.data['confirmpassword']
            if (newpassword!=confirmpassword):
                return Response({'message':'password mismatch'})
            else:
                user.Password = newpassword
                user.save()
                return Response({
                    'message':'Password reset successfully'
                })

    if recruiter:
        if Recruiters.objects.filter(Email=Email).exists():
            newpassword = serializer.data['newpassword']
            confirmpassword = serializer.data['confirmpassword']
            if (newpassword!=confirmpassword):
                return Response({'message':'password mismatch'})
            else:
                recruiter.Password = newpassword
                recruiter.save()
                return Response({
                    'message':'Password reset successfully'
                })
                
    else:
        return Response({'message':'Given Email does not exists....'})


@api_view(['PUT'])
def reset_password(request):
    """reset_password with email, OTP and new password"""
    data = request.data
    user = User.objects.get(email=data['email'])
    if user.is_active:
        # Check if otp is valid
        if data['otp'] == user.otp:
            if password != '':
                # Change Password
                user.set_password(data['password'])
                user.save() # Here user otp will also be changed on save automatically 
                return Response('any response or you can add useful information with response as well. ')
            else:
                message = {
                    'detail': 'Password cant be empty'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {
                'detail': 'OTP did not matched'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {
            'detail': 'Something went wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

  
class FileRetrieveUpdateDestroyAPIViews(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    def put(self, request, id=None,format=None):
        file = FileUpload.objects.get(id=id)
        serializer = FileUploadDisplaySerializer(instance=file, data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message' : 'File updated successfully',
            'data' : serializer.data
        })
        
    def delete(self, request, id, format=None):
        file = FileUpload.objects.get(id=id)
        file.delete()
        return Response({
            'message' : 'File deleted successfully.'
        })


class FileUploadView(generics.ListCreateAPIView):
   
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FileUploadDisplaySerializer
    def post(self, request, format=None): 
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():    #validate the serialized data to make sure its valid       
            qs = serializer.save()                     
            message = {'detail':qs, 'status':True}
            return Response(message, status=status.HTTP_201_CREATED)
        else: #if the serialzed data is not valid, return erro response
            data = {"detail":serializer.errors, 'status':False}            
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        return FileUpload.objects.all().order_by('-id')
    

class TotalcountView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get(self, request,queryset=None):
        resume = FileUpload.objects.all().count()
        users = Recruiters.objects.all().count()
        user = self.get_object()
        credits = user.Credits
        
        return Response({"TotalResumes":resume,"Totalrecruiter":users,'Credits': credits})
    

class FileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get_object(self, queryset=None):
        return self.request.user
        
    def get(self, request, id = None, format=None):
        self.object = self.get_object()
        
        data = FileUpload.objects.get(id=id)
        try:
            if id:
                serializer = FileUploadDisplaySerializer(data)
      
                return Response({'data':serializer.data,})
        except FileUpload.DoesNotExist:
            return Http404

def display_images(request):
        
        if request.method == 'GET':
            
            file = FileUpload.objects.all()
            return (request,{'img': file , 'media_url':settings.MEDIA_URL})
    

class DownloadFile(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_object(self, queryset=None):
        return self.request.user
    
    def get(self, request, filename=''):
        if filename != '':
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = BASE_DIR + '/media/' + filename
            path = open(filepath, 'rb')
            mime_type, _ = mimetypes.guess_type(filepath)
            user = self.get_object()
            user.Credits = user.Credits-1
            user.save()
            download = FileUpload.objects.get(file=filename)
            download.download_count = download.download_count + 1
            download.save()
            response = HttpResponse(path, content_type=mime_type)
            response['content-Disposition'] = "attachment; filename=%s" % filename
            return response
        

        
from django.db.models import F
from django.db.models import Sum

class Download(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, **kwargs):
        counts = FileUpload.objects.aggregate(Sum('download_count'))
        count = FileUpload.objects.aggregate(Sum('view_count'))
        
        return Response({"Download_Count":counts,"View_Count":count})
        
        
class View(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, **kwargs):
        counts = FileUpload.objects.aggregate(Sum('view_count'))
        return Response(counts)

class downloadcount(APIView):
    permission_classes= (AllowAny,)
    
    def get(self, **kwargs):
        context = super().get(**kwargs)
        slug_url = self.kwargs['slug']
        product = FileUpload.objects.filter(slug=slug_url)
        product.update(view_count = F('view_count') + 1)
        product.save()
        context["products"] = product
        return context
   

    
class PlanAPIView(APIView):
    permission_classes = (AllowAny,)
    def get_object(self, id):
        try:
            return Plan.objects.get(id=id)
        except Plan.DoesNotExist:
            return Http404
        
    def get(self, request, id=None, format=None):
        if id:
            data = self.get_object(id)
            serializer = PlanSerializer(data)
            return Response(serializer.data)
        else:
            data = Plan.objects.all()
            serializer = PlanSerializer(data, many=True)
            return Response(serializer.data)
    
    def post(self, request,*args, **kwargs):
        plan = PlanSerializer(data=request.data)
        plan.is_valid(raise_exception=True)
        plan.save()
        
        return Response({
            'message' : 'Plan created successfully',
            'data' : plan.data
        }) 
        
    def put(self, request, id=None, formate=None):
        plan = Plan.objects.get(id=id)
        plan = PlanSerializer(instance=plan, data=request.data, partial=True)
        plan.is_valid(raise_exception=True)
        plan.save()
        
        return Response({
            'message' : 'Plan updated successfully',
            'data' : plan.data
        })
        
    def delete(self, request, id, format=None):
        plan = Plan.objects.get(id=id)
        plan.delete()
        return Response({
            'message' : 'Plan deleted successfully'
        })
    
    
def pdf_view(request, filename='',*args, **kwargs):
    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + '/media/' + filename
        with open(filepath, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=mypdf.docx'
            return response
        
        
class pdf_view(APIView):
    permission_classes =(AllowAny,)
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get(self,request, filename='', *args, **kwargs):
        if filename != '':
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = BASE_DIR + '/media/' + filename
            with open(filepath, 'rb') as file:
                mime_type, _ = mimetypes.guess_type(filepath)
                # user = self.get_object()
                # user.Credits = user.Credits-1
                # user.save()
                # view = FileUpload.objects.get(file=filename)
                # view.view_count = view.view_count + 1
                # view.save()
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=mypdf'
                return response
    
    
class AssesmentAPIView(APIView):
    permission_classes = ([AllowAny,])

    def get_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Http404
        
    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_object(pk)
            serializer = AssessmentSerializer(data)
            return Response(serializer.data)
        else:
            data = Assessment.objects.all()
            serializer = AssessmentSerializer(data, many=True)
            return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = AssessmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message' : 'Assessment created successfully....',
            'data' : serializer.data
        })
    
    def put(self, request, pk=None, format=None):
        assessment = Assessment.objects.get(pk=pk)
        serializer = AssessmentSerializer(instance=assessment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message' : 'Assessment updated successfully....',
            'data' : serializer.data
        })
    
    def delete(self, request, pk, format=None):
        assessment = Assessment.objects.get(pk=pk)
        assessment.delete()
        return Response({
            'message' : 'Assessment deleted successfully....'
        })
    

class QuestionAPIView(APIView):
    permission_classes = [AllowAny,]
    def get_object(self, pk):
        try:
            return Questions.objects.get(pk=pk)
        except Questions.DoesNotExist:
            raise Http404
        
    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_object(pk)
            serializer = QuestionSerializer(data)
            return Response(serializer.data)
        else:
            data = Questions.objects.all()
            serializer = QuestionSerializer(data, many=True)
            return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message' : 'Questions created successfully....',
            'data' : serializer.data
        })
    
    def put(self, request, pk=None, format=None):
        question = Questions.objects.get(pk=pk)
        serializer = QuestionSerializer(instance=question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message' : 'Questions updated successfully....',
            'data' : serializer.data
        })
    
    def delete(self, request, pk, format=None):
        question = Questions.objects.get(pk=pk)
        question.delete()
        return Response({
            'message' : 'Questions deleted successfully....'
        })
        

            
class AssessmentAPIViews(ListCreateAPIView):
    serializer_class = AssessmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Name']
    
    filterset_fields = ['id', 'Name', 'Tags']
    search_fields = ['id', 'Name', 'Tags']
    
    def get_queryset(self):
        return Assessment.objects.filter().order_by('Name')
    
class SnippetListView(ListAPIView):
    permission_classes = [AllowAny]
    
    # def get(request,self):
    queryset = Assessment.objects.all()
    
    serializer_class = SnippetListSerializer

 
class SnippetDetailview(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    
    # email = "kannannikish@gmail.com"
    # subject = 'Mail From Hiera'
    # message = 'Your Credentials are: UserName = ' +str(serializers.HyperlinkedIdentityField) 
    # from_email = settings.EMAIL_HOST_USER
    # recipient_list = [email]

    # send_mail(subject, message=message, from_email=from_email, recipient_list=recipient_list)
 
    


