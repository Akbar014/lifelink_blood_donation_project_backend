from rest_framework import serializers

from . import models
from django.contrib.auth.models import User


from . constants import GENDER  , BLOOD_GROUP

class DonationRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    class Meta:
        model = models.DonationRequest
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(required=True)
    blood_group = serializers.ChoiceField(choices = BLOOD_GROUP,  required=True)
    gender = serializers.ChoiceField(choices = GENDER,  required=True)
    age = serializers.IntegerField()
    mobile_no = serializers.IntegerField()
    address = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'blood_group', 'mobile_no', 'gender', 'age', 'address', 'password', 'confirm_password']
        # fields =  '__all__'

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        blood_group = self.validated_data['blood_group']
        age = self.validated_data['age']
        address = self.validated_data['address']
        gender = self.validated_data['gender']
        mobile_no = self.validated_data['mobile_no']

        if password != password2:
            raise serializers.ValidationError({'error': "Passwonrd Doesn't Matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email Already Exists'})

        user = User(username = username, email=email, first_name = first_name, last_name = last_name)
       
        user.set_password(password)
        user.is_active = False
        user.save()

        models.UserAccount.objects.create(
            user = user,
            age = age,
            blood_group = blood_group,
            address = address,
            gender = gender,
            mobile_no = mobile_no,

        )
        return user



    

class UserAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    image = serializers.ImageField(allow_null=True, required=False)
    # image_url = serializers.SerializerMethodField()
    class Meta:
        model = models.UserAccount
        fields = [
            'username', 'first_name', 'last_name', 'email', 'image', 'mobile_no', 
            'age', 'blood_group', 'gender', 'address', 'last_donation_date', 
            'is_available_for_donation'
        ]
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def update(self, instance, validated_data):
        
        user_data = validated_data.pop('user', {})

        
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


class DonationHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.DonatioHistory
        fields = '__all__'


class DonationAcceptedSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.DonationAccepted
        fields = '__all__'