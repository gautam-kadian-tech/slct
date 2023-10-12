from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from analytical_data.models.state_head_models import AutomatedModelsRunStatus
from analytical_data.utils.send_email import EmailService


@receiver(post_save, sender=AutomatedModelsRunStatus)
def my_callback(sender, instance, **kwargs):
    if instance.run_successful == False:
        EmailService.mail(
            "Model Run Failure",
            "",
            ["shivansh.gupta@in.ey.com", "jatin.yadav@dianapps.com"],
            f"""
            <html>
                <body>
                    Dear Sir/ Ma'am,
                    <p>
                    {instance.model_name} has failed to run at {instance.run_date}. Please find the error log below.
                    </p>
                    <p>
                        {instance.error_msg}
                    </p>
                    Please take neccesary action.
                </body>
            </html>
                """,
        )
