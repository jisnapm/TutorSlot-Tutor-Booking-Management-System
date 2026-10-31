from rest_framework import serializers
from booking.models import TutorDB, StudentDB

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorDB
        fields = "__all__"
        read_only = [id, ]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDB
        fields = "__all__"
        read_only = [id, ]

    def validate(self, validated_data):
        ph = validated_data.get("phone")
        c_date = validated_data.get("class_date")

        if StudentDB.objects.filter(
            phone = ph,
            class_date = c_date
        ).exists():
            raise serializers.ValidationError("Already booked a slot for this day! Try another day!")
        else:
            return validated_data