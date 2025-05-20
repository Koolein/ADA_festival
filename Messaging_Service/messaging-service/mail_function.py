from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Personalization
from access_secret import access_secret


def send_mail(recipients):

    sendgrid_api_key = access_secret('SENDGRID_API')

    sg = SendGridAPIClient(api_key=sendgrid_api_key)
    from_email = Email('maxrobertdl@gmail.com')
    subject = 'Updates on your festival(s)'
    content = Content('text/html','<strong>One of your festivals have updates, check the FestiFlow website for more info!</strong>')

    mail = Mail()
    mail.from_email = from_email
    mail.subject = subject
    mail.add_content(content)

    for recipient_email  in recipients:
        personalization = Personalization()
        personalization.add_to(Email(recipient_email))  # Use Email instead of To here
        mail.add_personalization(personalization)

    # Send the email
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Error sending email:", str(e))