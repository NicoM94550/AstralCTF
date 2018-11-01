# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("ACac1d71ca682f3f8eff1f24430db785e1", "80d05fc7eb0dee76d09e1dfa32ff3ee8")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
def sendMessage(Message):
	client.messages.create(to="+19253219750", from_="+14159407771", body=Message)
