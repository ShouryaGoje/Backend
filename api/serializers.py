from rest_framework import serializers
from .models import *

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','f_name','l_name','dob','password']


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['p_name','p_dob']

class ProfileAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['u_id','p_name','p_dob']

class ProfileDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['u_id','p_name']

class GraphDataReceiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphDatabase
        fields =['u_id','p_name','time_array','volume_array']

class GraphDataRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphDatabase
        fields = ['u_id','p_name','date']

class GraphDataSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphDatabase
        fields =['u_id','p_name','time_array','volume_array','date','total_volume']

    
class ReportGeneratorRequestSerializer(serializers.Serializer):
    u_id = serializers.IntegerField()
    p_name = serializers.CharField(max_length=50)
    from_date = serializers.DateField()
    to_date = serializers.DateField()

class GenerateAnalysisSerializer(serializers.Serializer):
    u_id = serializers.IntegerField()
    p_name = serializers.CharField(max_length=50)
    from_date = serializers.DateField()
    to_date = serializers.DateField()


# class TestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = test
#         fields = ['array']