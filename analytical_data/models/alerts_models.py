from django.db import models


class AlertMaster(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    alert_name = models.TextField(db_column="ALERT_NAME", blank=True, null=True)
    email_content = models.TextField(db_column="EMAIL_CONTENT", blank=True, null=True)
    sms_content = models.TextField(db_column="SMS_CONTENT", blank=True, null=True)
    notification_content = models.TextField(
        db_column="NOTIFICATION_CONTENT", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(db_column="LAST_UPDATE_DATE")
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    is_active = models.CharField(
        db_column="IS_ACTIVE", max_length=1, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ALERT_MASTER"


class AlertTransaction(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    alert_id = models.BigIntegerField(db_column="ALERT_ID", blank=True, null=True)
    user_id = models.BigIntegerField(db_column="USER_ID", blank=True, null=True)
    type = models.TextField(db_column="TYPE", blank=True, null=True)
    is_read = models.CharField(db_column="IS_READ", max_length=1, blank=True, null=True)
    mobile_number = models.BigIntegerField(
        db_column="MOBILE_NUMBER", blank=True, null=True
    )
    email = models.CharField(db_column="EMAIL", max_length=100, blank=True, null=True)
    email_content = models.TextField(db_column="EMAIL_CONTENT", blank=True, null=True)
    sms_content = models.TextField(db_column="SMS_CONTENT", blank=True, null=True)
    notification_content = models.TextField(
        db_column="NOTIFICATION_CONTENT", blank=True, null=True
    )
    created_by = models.BigIntegerField(db_column="CREATED_BY")
    creation_date = models.DateTimeField(db_column="CREATION_DATE", auto_now_add=True)
    last_updated_by = models.BigIntegerField(db_column="LAST_UPDATED_BY")
    last_update_date = models.DateTimeField(
        db_column="LAST_UPDATE_DATE", auto_now_add=True
    )
    last_update_login = models.BigIntegerField(db_column="LAST_UPDATE_LOGIN")
    is_active = models.CharField(
        db_column="IS_ACTIVE", max_length=1, blank=True, null=True
    )
    is_sms_send = models.CharField(
        db_column="IS_SMS_SEND", max_length=1, blank=True, null=True
    )
    is_email_send = models.CharField(
        db_column="IS_EMAIL_SEND", max_length=1, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ALERT_TRANSACTION"


class CrmApprovalStageGates(models.Model):
    id = models.BigAutoField(db_column="ID", primary_key=True)
    approval_type = models.CharField(
        db_column="APPROVAL_TYPE", max_length=360, blank=True, null=True
    )
    record_id = models.BigIntegerField(db_column="RECORD_ID", blank=True, null=True)
    is_approved = models.BooleanField(db_column="IS_APPROVED", blank=True, null=True)
    status = models.CharField(db_column="STATUS", max_length=360, blank=True, null=True)
    date_time = models.DateTimeField(db_column="DATE_TIME", blank=True, null=True)
    sync_flag = models.BooleanField(db_column="SYNC_FLAG", blank=True, null=True)
    crm_requisition_number = models.BigIntegerField(
        db_column="CRM_REQUISITION_NUMBER", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "CRM_APPROVAL_STAGE_GATES"
