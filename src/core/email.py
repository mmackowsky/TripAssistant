def send_templated_email(to_email: str, template: str, context) -> None:
    mail_subject = "Activation link has been sent to your email id"
    message = render_to_string(template, context)
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
