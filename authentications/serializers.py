from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from branches.models import GymBranch
from branches.serializers import GymBranchSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gym_branch = GymBranchSerializer(read_only=True)
    gym_branch_id = serializers.PrimaryKeyRelatedField(
        queryset=GymBranch.objects.all(), source='gym_branch', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'gym_branch', 'gym_branch_id', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    gym_branch_id = serializers.PrimaryKeyRelatedField(
        queryset=GymBranch.objects.all(), source='gym_branch', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'gym_branch_id']
        read_only_fields = ['id']

    def validate_role(self, value):
        request = self.context.get('request')
        if not request:
            return value
        
        user = request.user
        # Manager can only create trainer or member
        if user.role == 'manager' and value not in ['trainer', 'member']:
            raise serializers.ValidationError("Manager can only create trainers or members")
        return value

    def validate(self, data):
        request = self.context.get('request')
        if not request:
            return data
        
        user = request.user
        gym_branch = data.get('gym_branch')
        role = data.get('role')

        # Manager must assign users to their own branch
        if user.role == 'manager':
            if gym_branch and gym_branch != user.gym_branch:
                raise serializers.ValidationError({"gym_branch_id": "You can only create users for your own branch"})
            data['gym_branch'] = user.gym_branch

        # Check trainer limit (max 3 per branch)
        if role == 'trainer' and gym_branch:
            trainer_count = User.objects.filter(gym_branch=gym_branch, role='trainer').count()
            if trainer_count >= 3:
                raise serializers.ValidationError({"role": "This branch already has 3 trainers (maximum limit)"})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError({"credentials": "Email and password are required"})

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"credentials": "Invalid email or password"})
        if not user.is_active:
            raise serializers.ValidationError({"credentials": "Account is disabled"})
        return user
