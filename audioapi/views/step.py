"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from audioapi.models import Step, Session, AudioUser
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

def verify(request):
    # Verify step count
    count = request.data["step_count"]
    if not -1 < int(count) < 10 :
        raise Exception('Step count must be between 0 and 9')

    session = Session.objects.get(session=request.data["session_id"])
    existing_counts = session.session_steps
    print(existing_counts)
    if count in session.session_steps.all():
        raise Exception('Step must be unique within each Session')
        

class StepView(ViewSet):
    """Step view"""

    # def retrieve(self, request, pk):
    #     """Handle GET requests for single step entry

    #     Returns:
    #         Response -- JSON serialized step entry
    #     """
    #     try:
    #         step = Step.objects.get(pk=pk)
    #         serializer = StepSerializer(step)
    #         return Response(serializer.data)
    #     except Step.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    # def list(self, request):
    #     """Handle GET requests to get all step data

    #     Returns:
    #         Response -- JSON serialized list of step data
    #     """
    #     step = Step.objects.all()

    #     # Search Query
    #     step_id = request.query_params.get('id', None)
    #     if step_id is not None:
    #         step = step.filter(step=step_id)

    #     serializer = StepSerializer(step, many=True)
    #     return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized step instance
        """
        
        # Verify step data
        verify(request)

        session=Session.objects.get(session=request.data["session_id"])

        step = Step.objects.create(
            session=session,
            step_count=request.data["step_count"]
        )
        serializer = StepSerializer(step)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        """Handle PUT requests for a step

        Returns:
            Response -- Empty body with 204 status code
        """
        
        verify(request)

        step = Step.objects.get(pk=pk)
        step = Step.objects.get(step_id=step.step)

        # Currently allowing step ID to be modified-- if not desired can easily disable
        # Currently not allowing associated user to be modified
        step.step = request.data["step_id"]
        step.ticks = request.data["ticks"]
        step.selected_tick = request.data["selected_tick"]
        step.step_count = request.data["step_count"]
        step.step_id = request.data["step_id"]

        step.save()
        step.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        step = Step.objects.get(pk=pk)
        step = Step.objects.get(step_id=step.step)
        step.delete()
        step.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

            


class StepSerializer(serializers.ModelSerializer):
    """JSON serializer for step
    """
    class Meta:
        model = Step
        fields = ('id', 'session_id', 'step_count')
        depth = 1

