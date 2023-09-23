from langchain.agents.tools import Tool
import boto3

class Tools():

  def __init__(self):

    self.tools = [
        Tool(
            name="Get Customer Identity", 
            func=self.verify_customer,
            description="Get customer identity based on phone number"
        ),
        
        Tool(
            name="Get Customer Loan",
            func=self.get_loans,
            description="Retrieves customer's loan information based on phone number"
        ),
        
        Tool(
            name="Get Saved Payment Method",
            func=self.get_payment_method,
            description="Retrieves saved payment method info for the customer"
        ),
        
        Tool(
            name="Process Payment",
            func=self.make_payment,
            description="Processes ACH payment with provided payment details"
        )
        
    ]

  def verify_customer(self, phone_number):
      return "Based on the phone number provided, we have received the following identity: Kenton Blacutt, 123 Main Street, Anytown, USA 12345." 

  def get_loans(self, phone_number):
    return [
        {
            "loanNumber": "123456789",
            "originalAmount": "200000", 
            "currentBalance": "185000",
            "interestRate": "4.5%",
            "nextPaymentAmount": "850.25",
            "nextPaymentDueDate": "08/31/2023" 
        }
    ]

  def get_payment_method(self, phone_number):
      return {
          "routingNumber": "123456789",
          "accountNumber": "987654321", 
          "accountType": "Checking"
      }

  def make_payment(self, _input):
      return "The payment was made successfully." # Confirmation number 
  
tools = Tools().tools