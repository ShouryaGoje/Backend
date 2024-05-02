from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
from rest_framework import status
from.serializers import*
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .ReportGenrator.report_gen import generate_report
import numpy as np
import json



# Create your views here.

class Register(APIView):
    serializer_class = UserRegisterSerializer
    def post(self,request,fromat =None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            username = serializer.data.get('username')
            f_name = serializer.data.get('f_name')
            l_name = serializer.data.get("l_name")
            dob = serializer.data.get("dob")
            password = serializer.data.get('password')
            
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

            if age < 5:
                return Response({"error": "User's age must be at least 5 years old"}, status=status.HTTP_400_BAD_REQUEST)

            queryset = User.objects.filter (username = username)
            if queryset.exists():
                return Response(serializer.errors, status=status.HTTP_226_IM_USED)
            
            else :
                user = User(username=username,f_name=f_name,l_name=l_name,dob=dob,password=password)
                user.save()
                profile = Profile(u_id = user.u_id,p_name = f_name, p_dob = dob)
                profile.save()

                return Response(UserRegisterSerializer(user).data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            

class Login(APIView):
    serializer_class = UserLoginSerializer

    def post(self,request,format =None):

        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            queryset = User.objects.filter(username= username,password = password)
            if queryset.exists():
                user = queryset.first()
                profile_queryset = Profile.objects.filter(u_id = user.u_id)
                if profile_queryset.exists():
                    profiles = profile_queryset
                    return Response({'u_id':user.u_id, "profile": ProfileSerializer(profiles,many = True).data},status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'No Profiles Exisits Currently '},status=status.HTTP_204_NO_CONTENT)            
            else:
                return Response({'error': 'Invalid username or password'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class AddProfile(APIView):
    serializer_class = ProfileAddSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            u_id = serializer.data.get('u_id')
            p_name = serializer.data.get('p_name')
            p_dob = serializer.data.get('p_dob')
            dob_date = datetime.strptime(p_dob, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

            if age < 5:
                return Response({"error": "User's age must be at least 5 years old"}, status=status.HTTP_204_NO_CONTENT)
            queryset = Profile.objects.filter(p_name=p_name,u_id=u_id)
            if queryset.exists():
                return Response({'error' : 'Profile name alredy There ','u_id':u_id},status=status.HTTP_226_IM_USED)
            else:
                profile = Profile(p_name=p_name,u_id = u_id, p_dob = p_dob)
                profile.save()
                return Response({'u_id':u_id,"profile":ProfileSerializer(Profile.objects.filter(u_id=u_id),many = True).data},status=status.HTTP_201_CREATED)         
        else:
            return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)

class DelProfile(APIView):
    serializer_class = ProfileDelSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            u_id = serializer.data.get('u_id')
            p_name = serializer.data.get('p_name')
            if p_name == User.objects.filter(u_id=u_id).first().f_name:
                return Response({'error': 'Main Profile, cannot be deleted'},status=status.HTTP_226_IM_USED)

            del_queryset = Profile.objects.filter(u_id=u_id,p_name=p_name)
            if del_queryset.exists():
                del_queryset.delete()
                return Response({'u_id':u_id,"profile":ProfileSerializer(Profile.objects.filter(u_id=u_id),many = True).data},status=status.HTTP_202_ACCEPTED)
                
            else:
                return Response({'error': 'Profile not found'},status=status.HTTP_404_NOT_FOUND)
                 
        else:
            return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    
class GraphDataSave(APIView):
    serializer_class = GraphDataReceiveSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            u_id = serializer.validated_data['u_id']
            p_name = serializer.validated_data['p_name']
            p_id = Profile.objects.filter(u_id=u_id, p_name=p_name).first().p_id
            time_array = serializer.validated_data['time_array']
            volume_array = serializer.validated_data['volume_array']

            # Convert time_array and volume_array to JSON serializable types
            time_array_serializable = list(map(float, time_array))
            volume_array_serializable = list(map(float, volume_array))

            if len(time_array_serializable) < 2 :
                return Response({},status=status.HTTP_100_CONTINUE)

            area_under_curve = np.trapz(time_array_serializable, volume_array_serializable)

            graph_data = GraphDatabase.objects.create(
                u_id=u_id,
                p_name=p_name,
                p_id=p_id,
                time_array=time_array_serializable,
                volume_array=volume_array_serializable,
                total_volume =  np.round(np.abs(area_under_curve),3)
            )

            return Response({"area": np.round(np.abs(area_under_curve),3)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GarphDataSend(APIView):
    serializer_class = GraphDataRequestSerializer
    def post(self, request,format = None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            u_id = serializer.data.get('u_id')
            p_name = serializer.data.get('p_name')
            date = serializer.data.get('date')
            queryset = GraphDatabase.objects.filter(u_id=u_id, p_name=p_name, date=date)
            if queryset.exists():
                data = queryset
                return Response(GraphDataSendSerializer(data, many = True).data,status=status.HTTP_200_OK)
            return Response({'message':f'no data on date {date}'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GenerateReport(APIView):
    serializer_class = ReportGeneratorRequestSerializer
    def post(self, request, fromat = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            u_id = serializer.data.get('u_id')
            p_name = serializer.data.get('p_name')
            from_date = serializer.data.get('from_date')
            to_date = serializer.data.get('to_date')
            queryset = GraphDatabase.objects.filter(date__range=(from_date, to_date), u_id=u_id, p_name=p_name)
            if queryset.exists():
                response  = generate_report(queryset.values())
                
                return response
            return Response({'message':f'No data found between {from_date} and {to_date} '}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GenerateAnalysis(APIView):
    serializer_class = GenerateAnalysisSerializer
    def post(self, request, fromat = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            u_id = serializer.data.get('u_id')
            p_name = serializer.data.get('p_name')
            from_date = serializer.data.get('from_date')
            to_date = serializer.data.get('to_date')
            queryset = GraphDatabase.objects.filter(date__range=(from_date, to_date), u_id=u_id, p_name=p_name)
            if queryset.exists():
                average_time_array = []
                date_array = []
                for dates in queryset:
                    date = dates.date
                    if date in date_array :
                        continue
                    date_array.append(date)
                    mainset = GraphDatabase.objects.filter(date=date,u_id=u_id,p_name=p_name)
                    if mainset.exists():
                        count =0
                        val = 0 
                        for timedata in mainset:
                            count +=1
                            lst = list(timedata.time_array)
                            val += float(lst[-1])
                        average_time_array.append(round(val/count,2))
                    else:
                        average_time_array.append(0)
                return Response({"u_id":u_id,"p_name":p_name,"average_time_array":average_time_array,"date_array":date_array},status=status.HTTP_200_OK)
            return Response({'message':f'No data found between {from_date} and {to_date} '}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


def display(request):
    st=GraphDatabase.objects.all() 

    return render(request,'display.html',{'st':st})

