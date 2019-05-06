### Account management application using USSD.

In this tutorial we will create a simple account management system using USSD.
The user will be able to dial a USSD code and access their account balance and other information.
## Introduction
USSD(Unstructured Supplementary Service Data) is a means of communication used
 to send text and receive feedback from a user. The user dials a USSD code and
 gets a specified response from the owner of the code.

In order to build a USSD app you will need:

1. A USSD code (This is how the app is made available to the public)
2. A callback URL (Its through this url that the MNO is able to complete
 the communication between the user and the app)
3. Basic Python 🐍 knowledge, basic django knowledge, as the framework
we will use on this app is build based on Django, which is based on python.
You can proceed without reading both the above, in case you can read Python code

## PREAMBLE

Let’s assume we hold user info and we would like them to access it via USSD.
We will build a simple USSD menu that asks users to enter `1` to view their
account and `2` to view their phone number. On the accounts page, they can
enter `1` for the account number or `2` for the account balance.

## Start of coding.

As a general practise, django and python applications are built in a virtual environment.
A virtual environment is a tool that helps to keep dependencies required by different projects separate.
This project is initialized with Django, Lets add an application. I encourage you to create one for yourself.
I avoid adding the documents for it here as its out of the scope of this tutorial.

python manage.py startapp core