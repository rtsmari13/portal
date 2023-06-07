from django.urls import path
from .views import *
from app import views

urlpatterns = [
    path('admin', UserAPIView.as_view()), # post, get
    path('admins', UserAPIViews.as_view()), # Search and pagination
    path('admin/<int:id>', UserAPIView.as_view()), # get by id
    path('login', login_view, name='login'), # login
    path('admin/update/<int:id>', RetrieveUpdateDestroyAPIView.as_view()), # put, delete
    path('passwords', UpdatePassword.as_view()), # admin change password
    path('password', UpdatePasswords.as_view()), # recruiter change password
    path('reset', changepassword),
    path('confirm', reset_request),
    path('recruiter', RecruiterAPIView.as_view()), # post, get
    path('recruiters', RecruiterAPIViews.as_view()), # Search and pagination
    path('recruiter/<int:id>', RecruiterAPIView.as_view()), #get by id
    path('recruiter/update/<int:id>', RetrieveUpdateDestroyAPIViews.as_view()), # put, delete
    # path('assessment', AssessmentAPIView.as_view(),name='snippet-list'), #post, get
    # path('assessment/<int:id>', AssessmentAPIView.as_view()), #get, put and delete
    path('assessments', AssessmentAPIViews.as_view()), #Search and Pagination
    path('plan', PlanAPIView.as_view()), #post
    path('plan/<int:id>', PlanAPIView.as_view()), #get, put and delete
    path('file', FileUploadView.as_view(), name='file-upload'), # post, get
    path('files/<int:id>', FileAPIView.as_view(), name='file'), # get by id
    path('file/<int:id>', FileRetrieveUpdateDestroyAPIViews.as_view()), # put, delete
    path('files', FileUploadAPIViews.as_view()),    # Pagination
    path('media', display_images, name= 'img'),
    # path("showing/<int:id>", views.ImageFetch,name="show"),
    path('view-pdf/<str:filename>', pdf_view.as_view(),name='pdf_view'),
    path('downloadpdf/<str:filename>', DownloadFile.as_view()),
    path('filecount', Download.as_view()), #total download count
    path('fileviewcount',View.as_view()), #total view count
    path('dashboard',TotalcountView.as_view()),
    
    path('snippets', SnippetListView.as_view(), name='snippet-list'),
    path('snippets/<int:pk>', SnippetDetailview.as_view(), name='snippet-detail'),
    
    path('assessment', AssesmentAPIView.as_view(),name='snippet-list'),
    path('assessment/<int:pk>', AssesmentAPIView.as_view()),

    path('question', QuestionAPIView.as_view()),
    path('question/<int:pk>', QuestionAPIView.as_view()),
    
]
