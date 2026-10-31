from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from booking.models import TutorDB, StudentDB
from booking.serializers import TutorSerializer, StudentSerializer
from datetime import time, timedelta, datetime
from rest_framework import serializers

# Create your views here.
class TutorListCreateView(APIView):
    def get(self, request):
        qs = TutorDB.objects.all()
        s_instance = TutorSerializer(qs, many= True)
        return Response(data= s_instance.data)

    def post(self, request):
        form_data = request.data
        s_instance = TutorSerializer(data= form_data)
        if s_instance.is_valid():
            s_instance.save()
            return Response(data= {"message": "tutor details added!"})
        else:
            return Response(data= s_instance.errors)

class TutorRetreiveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(TutorDB, id = pk)
        s_instance = TutorSerializer(qs)
        return Response(data= s_instance.data)

    def put(self, request, pk):
        form_data = request.data
        tr_obj = get_object_or_404(TutorDB, id = pk)
        s_instance = TutorSerializer(data= form_data, instance= tr_obj)
        if s_instance.is_valid():
            s_instance.save()
            return Response(data= {"message":"tutor details updated!"})
        else:
            return Response(data= s_instance.errors)

    def delete(self, request, pk):
        dr_obj = get_object_or_404(TutorDB, id = pk)
        dr_obj.delete()
        return Response(data= {"message": "tutor deleted!"})

class BookingsListCreateView(APIView):
    def get(self, request):
        qs = StudentDB.objects.all()
        s_instance = StudentSerializer(qs, many= True)
        return Response(data= s_instance.data)

    # def post(self, request):
    #     form_data = request.data
    #     s_instance = StudentSerializer(data= form_data)
    #     if s_instance.is_valid():
    #         c_date = s_instance.validated_data.get("class_date") 
    #         tr_id = s_instance.validated_data.get("tutor_id")

    #         last_book = StudentDB.objects.filter(
    #             class_date = c_date,
    #             tutor_id = tr_id  
    #         ).order_by("-class_token").first()

    #         if last_book is None:
    #             form_data["class_token"] = 1
    #             form_data["class_time"] = time(9, 0)
    #         else:
    #             form_data["class_token"] = last_book.class_token + 1
    #             current_time = datetime.combine(c_date, last_book.class_time)
    #             next_time = (current_time + timedelta(minutes= 30)).time()

    #             form_data["class_time"] = next_time

    #         # s_instance = StudentSerializer(data= form_data)
    #         # if s_instance.is_valid():
    #         #     s_instance.save()

    #         qs = StudentDB.objects.create(**form_data)
    #         s_instance = StudentSerializer()

    #         return Response(data= {
    #             "Status": "Booked",
    #             "Token": form_data["class_token"],
    #             "Class Time": form_data["class_time"]
    #             })

    #     else:
    #         return Response(data= s_instance.errors)


    def post(self, request):
        form_data = request.data
        s_instance = StudentSerializer(data=form_data)

        if s_instance.is_valid():
            c_date = s_instance.validated_data.get("class_date")
            tr_id = s_instance.validated_data.get("tutor_id")

            last_book = StudentDB.objects.filter(
                class_date=c_date,
                tutor_id=tr_id
            ).order_by("-class_token").first()

            if last_book is None:
                class_token = 1
                class_time = time(9, 0)

            else:
                class_token = last_book.class_token + 1
                current_time = datetime.combine(
                    c_date, last_book.class_time
                )
                next_time = current_time + timedelta(minutes=30)

                # lunch time
                if next_time.time() == time(12, 30):
                    next_time = datetime.combine(c_date, time(13, 30))

                # close
                if next_time.time() == time(17, 0):
                    raise serializers.ValidationError("All the slots are filled for this day! Try another day!")

                class_time = next_time.time()

            s_instance.save(
                class_token=class_token,
                class_time=class_time
            )

            return Response({
                "Status": "Booked",
                "Token": class_token,
                "Class Time": class_time
            })

        else:
            return Response(s_instance.errors, status=400)