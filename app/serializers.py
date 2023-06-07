from io import BytesIO
from .models import *
from rest_framework import serializers
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  '__all__'
        extra_kwargs = {
            'master_primary_colour':{'read_only':True},
            'master_secondary_colour':{'read_only':True},
            'is_anonymous': {'write_only': True},
            'is_authenticated': {'write_only': True},
            'is_active': {'write_only': True},
            'is_staff': {'write_only': True}
        }
class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiters
        fields = '__all__'
        extra_kwargs = {
            'master_primary_colour':{'read_only':True},
            'master_secondary_colour':{'read_only':True},
            'is_anonymous': {'write_only': True},
            'is_authenticated': {'write_only': True},
            'is_active': {'write_only': True},
            'is_staff': {'write_only': True}
        }
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'Assessment', 'question', 'option1', 'option2', 'option3', 'option4', 'answer')


class AssessmentSerializer(serializers.ModelSerializer):
    Question_list = QuestionSerializer(read_only=True, many=True)
    class Meta:
        model = Assessment
        fields = ('id', 'name', 'tags', 'description', 'Question_list')
        
class SnippetListSerializer(serializers.ModelSerializer):
    snippet_details = serializers.HyperlinkedIdentityField(view_name='snip:snippet-detail')

    class Meta:
        model = Assessment
        fields = ['id','name','snippet_details']
        
class PlanSerializer(serializers.ModelSerializer):
    class Meta :
        model = Plan
        fields = '__all__'
 
class AdminChangePasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(required=True, max_length=30)
    newpassword = serializers.CharField(required=True, max_length=30)
    confirmpassword = serializers.CharField(required=True, max_length=30)

class RecruiterChangePasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(required=True, max_length=30)
    newpassword = serializers.CharField(required=True, max_length=30)
    confirmpassword = serializers.CharField(required=True, max_length=30)

    
class resetpasswordSerializer(serializers.Serializer):
    Email = serializers.EmailField(required=True, max_length=50)
    otp = serializers.CharField(required=True, max_length=15)
    newpassword = serializers.CharField(required=True, max_length=30)
    confirmpassword = serializers.CharField(required=True, max_length=30)

THUMBNAIL_SIZE = (200, 200)

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

class ThumbnailMixin:
    def create_thumbnail(self, file):
        image = Image.open(file)
        image.thumbnail((100, 100))
        thumb_io = BytesIO()
        image.save(thumb_io, image.format, quality=80)
        thumbnail = SimpleUploadedFile(file.name, thumb_io.getvalue(), content_type='image/jpeg')
        return thumbnail

class FileUploadSerializer(serializers.ModelSerializer,ThumbnailMixin):
    location = serializers.CharField(required=True, max_length=15)
    experience = serializers.CharField(required=True, max_length=15)
    company = serializers.CharField(required=True, max_length=15)
    designation = serializers.CharField(required=True, max_length=15)
    download_count = serializers.IntegerField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    file = serializers.ListField(
        child=serializers.FileField(max_length=100000, 
        allow_empty_file=False,
        use_url=False ))
    

    class Meta:
        model = FileUpload
        fields = ('id', 'location', 'experience', 'company', 'designation', 'file', 'download_count','view_count')

    def create(self, validated_data):
        location=validated_data['location']
        experience=validated_data['experience']
        company=validated_data['company']
        designation=validated_data['designation']
        file=validated_data['file'] 
        
        image_list = []
        for img in file:
            photo=FileUpload.objects.create(file=img, location=location, experience=experience, company=company, designation=designation)
            imageurl = f'{photo.file.url}'
            image_list.append(imageurl)   
        
        return ({
                               'location': location,
                               'experience': experience,
                               'company': company,
                               'designation': designation,
                               'file': image_list
                               })
        
        
class FileUploadDisplaySerializer(serializers.ModelSerializer):        
    class Meta:
        model = FileUpload
        fields = ('id', 'location', 'experience', 'company', 'designation', 'file', 'download_count','view_count')
