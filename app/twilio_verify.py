from flask import current_app
from app import app
from twilio.rest import Client, TwilioException
import requests
import os


TWILIO_ACCOUNT_SID= os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_ID= os.getenv('TWILIO_VERIFY_SERVICE_ID')




def _get_twilio_verify_client():
    return Client(app.config['TWILIO_ACCOUNT_SID'],app.config['TWILIO_AUTH_TOKEN']).verify.services(app.config['TWILIO_VERIFY_SERVICE_ID'])
#        current_app.config['TWILIO_ACCOUNT_SID'],
#        current_app.config['TWILIO_AUTH_TOKEN']).verify.services(
#            current_app.config['TWILIO_VERIFY_SERVICE_ID'])




def request_verification_token(phone):
    verify = _get_twilio_verify_client()
    try:
        verify.verifications.create(to=phone, channel='sms')
    except TwilioException:
        verify.verifications.create(to=phone, channel='call')


def check_verification_token(phone, token):
    verify = _get_twilio_verify_client()
    try:
        result = verify.verification_checks.create(to=phone, code=token)
    except TwilioException:
        return False
    return result.status == 'approved'
