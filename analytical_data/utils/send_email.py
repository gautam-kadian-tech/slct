from django.core.mail import EmailMessage, send_mail


class EmailService(object):
    @classmethod
    def mail(cls, subject: str, body: str, to_email: list, html_body: str):
        send_mail(
            subject, body, "support@shreecement.com", to_email, html_message=html_body
        )

    @classmethod
    def mail_with_attachments(
        cls, subject: str, body: str, to_email: list, attachments: list
    ):
        mail = EmailMessage(
            subject=subject,
            body=body,
            from_email="support@shreecement.com",
            to=to_email,
        )
        with open(attachments, "rb") as file:
            mail.attach("SLCT_Usage_Report.xlsx", file.read(), "text/plain")
        mail.send()

    @classmethod
    def mail_with_attachments_adoption(
        cls, subject: str, body: str, to_email: list, attachments: list
    ):
        mail = EmailMessage(
            subject=subject,
            body=body,
            from_email="support@shreecement.com",
            to=to_email,
        )
        with open(attachments, "rb") as file:
            mail.attach("SLCT_Adoption_Report.xlsx", file.read(), "text/plain")
        mail.send()

    @classmethod
    def mail_with_attachments_adoption(
        cls, subject: str, body: str, to_email: list, attachments: list
    ):
        mail = EmailMessage(
            subject=subject,
            body=body,
            from_email="support@shreecement.com",
            to=to_email,
        )
        with open(attachments, "rb") as file:
            mail.attach("SLCT_Adoption_Report.xlsx", file.read(), "text/plain")
        mail.send()
