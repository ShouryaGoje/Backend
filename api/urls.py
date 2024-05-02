from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('register/', views.Register.as_view()),
    path('display/',views.display),
    path('add-profile/', views.AddProfile.as_view()),
    path('del-profile/', views.DelProfile.as_view()),
    path('graph-data/', views.GraphDataSave.as_view()),
    path('get-graph-data/', views.GarphDataSend.as_view()),
    path('generate-report/', views.GenerateReport.as_view()),
    path('generate-analysis/', views.GenerateAnalysis.as_view())
    # path('test/', views.TestAPIView.as_view())
]
