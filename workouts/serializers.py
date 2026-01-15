from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import WorkoutPlan, WorkoutTask
from branches.serializers import GymBranchSerializer

User = get_user_model()


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class WorkoutPlanSerializer(serializers.ModelSerializer):
    created_by = TrainerSerializer(read_only=True)
    gym_branch = GymBranchSerializer(read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'title', 'description', 'created_by', 'gym_branch', 'created_at']
        read_only_fields = ['id', 'created_by', 'gym_branch', 'created_at']


class WorkoutPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']

    def validate(self, data):
        request = self.context.get('request')
        if not request:
            return data
        
        user = request.user
        # Only trainers can create workout plans
        if user.role != 'trainer' and user.role != 'admin':
            raise serializers.ValidationError({"permission": "Only trainers can create workout plans"})
        
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['created_by'] = user
        validated_data['gym_branch'] = user.gym_branch
        return super().create(validated_data)


class WorkoutTaskSerializer(serializers.ModelSerializer):
    workout_plan = WorkoutPlanSerializer(read_only=True)
    member = MemberSerializer(read_only=True)

    class Meta:
        model = WorkoutTask
        fields = ['id', 'workout_plan', 'member', 'status', 'due_date', 'created_at']
        read_only_fields = ['id', 'created_at']


class WorkoutTaskCreateSerializer(serializers.ModelSerializer):
    workout_plan_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutPlan.objects.all(), source='workout_plan'
    )
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='member'), source='member'
    )

    class Meta:
        model = WorkoutTask
        fields = ['id', 'workout_plan_id', 'member_id', 'status', 'due_date']
        read_only_fields = ['id']

    def validate(self, data):
        request = self.context.get('request')
        if not request:
            return data
        
        user = request.user
        workout_plan = data.get('workout_plan')
        member = data.get('member')

        # Admin can bypass restrictions
        if user.role == 'admin':
            return data

        # Only trainers can create tasks
        if user.role != 'trainer':
            raise serializers.ValidationError({"permission": "Only trainers can assign workout tasks"})

        # Trainer can only assign tasks from their branch's workout plans
        if workout_plan.gym_branch != user.gym_branch:
            raise serializers.ValidationError({"workout_plan_id": "You can only use workout plans from your branch"})

        # Trainer can only assign tasks to members in their branch
        if member.gym_branch != user.gym_branch:
            raise serializers.ValidationError({"member_id": "You can only assign tasks to members in your branch"})

        # Member must have role 'member'
        if member.role != 'member':
            raise serializers.ValidationError({"member_id": "Tasks can only be assigned to members"})

        return data


class WorkoutTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTask
        fields = ['status']

    def validate_status(self, value):
        if value not in ['pending', 'in_progress', 'completed']:
            raise serializers.ValidationError("Status must be pending, in_progress, or completed")
        return value
