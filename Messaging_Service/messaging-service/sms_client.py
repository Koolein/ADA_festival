from twilio.rest import Client
from access_secret import access_secret


def send_sms(user_numbers):

  twilio_sid = access_secret('TWILIO_ACC_SID')
  sms_auth_token = access_secret('TWILIO_AUTH_TOKEN')

  client = Client(twilio_sid, sms_auth_token)

  for number in user_numbers:
    message = client.messages.create(
      from_='+19123944524',
      body='Changes or announcements have been made for a festival you have tickets for, check the website for more details',
      to=number
  )
    print(message.sid)


