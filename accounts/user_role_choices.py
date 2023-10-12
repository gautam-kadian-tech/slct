"""User role choices."""
from django.db.models import TextChoices


class UserRoleChoice(TextChoices):
    """user role choices"""

    LOGISTICS = "LOGISTICS"
    NSH = "NSH"  # National Sales Head
    NLH = "NLH"  # National Logistics Head
    NTH = "NTH"  # National Technical Head
    SLCTADMIN = "SLCTADMIN"
    ZLH = "ZLH"  # Zonal Logistics Head
    ZSH = "ZSH"  # Zonal Sales Head
    SH = "SH"  # State Head
    RH = "RH"  # Regional Head
    DI = "DI"
    STRATEGY = "STRATEGY"
    LEADERSHIP = "LEADERSHIP"
    LP = "LP"
    SLH = "SLH"  # Secondary Logistics Head
    SLR = "SLR"  # Secondary Logistics Regional Head
    BG = "BG"
    PLH = "PLH"
    RRC = "RRC"
    TSM = "TSM"  # Territory Sales Manager
    IMN = "IMN"  # Influencer Manager – National
    IMS = "IMS"  # Influencer Manager – State
    CBT = "CBT"  # Central Branding Team
    SM = "SM"  # State Marketing In-charge
    LBT = "LBT"  # Strategy Head
    RRCCLINKER = "RRCCLINKER"  # Road rake coordinator – Clinker
    AACLOGISTICS = "AACLOGISTICS"  # AAC Logistics Team
    HA = "HA"  # Handling Agent
    RRCCEMENT = "RRCCEMENT"  # Road rake coordinator – Cement
    AACBUSINESS = "AACBUSINESS"  # AAC Business Head
    TRANSPORTEROWNER = "TRANSPORTEROWNER"  # Transporter (Owner)
    TRANSPORTERPLANT = "TRANSPORTERPLANT"  # Transporter (Plant)
    SANH = "SANH"  # Sales Account National Head
    SAT = "SAT"  # Sales Account Team
    PPH = "PPH"  # Packing Plant Head
    NONTRADE = "NONTRADE"  # Non Trade Head
    PPINCHARGE = "PPINCHARGE"  # Packing Plant Shift In-charge
    AACPACKER = "AACPACKER"  # AAC Packer
    # LP = "LP"  # Logistics Planning
    DP = "DP"  # Demand Planning
    FCFPRICING = "FCFPRICING"  # 4X4 Pricing Strategy
    FCFCHANNEL = "FCFCHANNEL"  # 4X4 Channel & Counter Strategy
    FCFBRANDING = "FCFBRANDING"  # 4X4 Branding Budgeting Strategy
    INFLMEET = "INFLMEET"  # Influencer Meets Invitee List Model
    BACKUNLOADING = "BACKUNLOADING"  # Back-unloading Prediction Model
    PSNM = "PSNM"  # Pricing Strategy in New Markets
    FDWH = "FDWH"  # Forecasts for demurrages, wharfage, handling, and damages
    ETA = "ETA"  # ETA Model
    FREIGHTESTIMATION = "FREIGHTESTIMATION"  # Freight estimation for new routes
    DOAUGMENTATION = "DOAUGMENTATION"  # Market wise DO Augmentation
    DOLEAGUE = "DOLEAGUE"  # DO League Table
    CONTRIBUTIONANA = "CONTRIBUTIONANA"  # Contribution Analysis Model
    DLS = "DLS"  # Daily Logistics Scheduling
    PACKINGPLANTMODEL = (
        "PACKINGPLANTMODEL"  # Packing Plant Daily and Shift-wise Planning
    )
    BACKHAULING = "BACKHAULING"  # Backhauling Opportunities for Inbound Trucks
    GODOWNADDITION = (
        "GODOWNADDITION"  # Analysis to identify potential hotspots for godown addition
    )
    GDTRANSFER = "GDTRANSFER"  # Decision model on Wharfage vs GD Transfer
    SALESMDMADMIN = "SALESMDMADMIN"
    LOGISTICSMDMADMIN = "LOGISTICSMDMADMIN"
    USERADMIN = "USERADMIN"
    SALESEXCELLENCE = "SALESEXCELLENCE"


class UserActionChoices(TextChoices):
    LOGIN = "Login"
    LOGOUT = "Logout"
