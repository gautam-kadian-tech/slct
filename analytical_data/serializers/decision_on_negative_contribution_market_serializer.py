"""Analytical data non-trade head serializers module."""
from rest_framework import serializers

from analytical_data.models import (
    NshContributionScenario
)



class NshContributionScenarioSerializer(serializers.ModelSerializer):
    """Nsh Contribution Scenario serializer."""

    class Meta:
        model = NshContributionScenario
        fields = "__all__"