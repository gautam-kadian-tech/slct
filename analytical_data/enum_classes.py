"""Choices module."""
from django.db.models import Choices, IntegerChoices, TextChoices


class LpModelDfFnlBrandChoices(Choices):
    """Order master brand choices."""

    Scl = 101
    Shree = 102
    Bangur = 103
    Rockstrong = 104


class BrandChoices(Choices):
    """SCL brand choices."""

    SCL = 101
    Shree = 102
    Bangur = 103
    # Cemento is Rockstrong
    Cemento = 104


class BrandChoices1(Choices):
    SCL = 101
    Shree = 102
    Bangur = 103
    Rockstrong = 104


class DimResourceDesignationChoices(TextChoices):
    """Resource officer designation choices."""

    NTSO = "NTSO"
    TPC = "TPC"
    KAM = "KAM"


class InventoryItemIdChoices(IntegerChoices):
    """Product choices."""

    OPC_43 = 3437, "OPC_43"
    OPC_53 = 3438, "OPC_53"
    PPC = 3439, "PPC"
    PSC = 7147149, "PSC"
    SSC = 7450840, "SSC"
    CC = 7570361, "CC"
    PPC_ROOFON = 7675779, "PPC_ROOFON"
    RHPC = 7812054, "RHPC"
    OPC_53_PREMIUM = 7848842, "OPC_53_PREMIUM"
    PPC_S = 8080262, "PPC_S"


class ApprovalStatusChoices(TextChoices):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class SlctApprovalStatusChoices(TextChoices):
    PENDING = "PENDING"
    INITIATED = "INITIATED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class NSHApprovalChoices(TextChoices):
    """
    Status choices for a scheme to represent states of a scheme.
    Below statuses represent:
        1. PENDING: scheme has not been sent for approval
        2. INITIATED: scheme has been sent for approval
        3. REVIEWAL: scheme has been sent back to state head for reviewal by nsh
        4. APPROVED: scheme has been rejected
        5. REJECTED: scheme has been approved
    """

    PENDING = "PENDING"
    INITIATED = "INITIATED"
    REVIEWAL = "REVIEWAL"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
