from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import DoMasterAllIndiaData, SoTalukaMappingDelhiHyd


@receiver(pre_save, sender=SoTalukaMappingDelhiHyd)
def signal_so_taluka_mapping_update(sender, instance, **kwargs):
    instance.crm_updated = "N"


@receiver(pre_save, sender=DoMasterAllIndiaData)
def signal_do_master_update(sender, instance, **kwargs):
    instance.crm_updated = "N"
