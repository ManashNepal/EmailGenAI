import yagmail

def send_email(user_email, app_password, to_email, subject, body):
    yag = yagmail.SMTP(user=user_email, password=app_password)
    yag.send(to=to_email, subject=subject, contents=body)
