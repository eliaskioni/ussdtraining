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

To add a django app;

    python manage.py startapp core


Next, we add dependecies that we require to complete this app.

1. [Ussd Airflow](https://django-ussd-airflow.readthedocs.io/en/latest/quick_start.html)
   This module will simplify our work by;
    1. Handling USSD sessions
    2. Processing users input
    3. Serving the right response to the user.

    New terms:
    What is a session in respect to USSD. A session is a unique timed period, where a user can
    interact with a USSD application. This interaction means  a specified flow or journey which
    a customer follows to get value out of the application.

    User input: Is the user response as they use the USSD application, eg, we ask the user what info
    he needs, `1` for account balance or `2` for phone number. User responds with `1` for account
    balance. This is the user input.

    Serving response to user.
    After user selects `1` for account balance, the app echoes his account balance, this process is what is referred
    to as serving response to user in this tutorial.

To add ussd_airflow, we add this change in the requirements.txt file.

    'ussd_airflow'
Because ussd_airflow is a django app, we add ussd_airflow in the settings file, to make django load it,
as follows.
Edit `UssdIntroduction/settings.py` and make this change in the INSTALLED_APPS section, to look as this.

        INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ussd.apps.UssdConfig',
    'core'
]
 Notice we have add 'ussd.apps.UssdConfig' and 'core'.

 With the above change, lets proceed to the next stage.

 The MNO will make requests to our application, and we shall respond with a response to be
 displayed to the user.
 This means we need to expose an endpoint that the mno can make standard HTTP requests to.

 Lets do this.

We will follow django patterns.

We start by editing the `core/views.py` and making this simple change:


    from ussd.core import UssdView


    class AccountInfoView(UssdView):
        pass

What are we doing here. We are importing `UssdView`, from the `ussd_airflow` app we installed.
We then create a simple class `AccountInfoView` and make it inherit from `UssdView`. This will make our class(`AccountInfoView`) have all
the properties and methods exposed by `UssdView`.
`UssdView` will convert a normal web request to a ussd request. The major difference between a web
and a ussd request is a ussd request must be in a session. By inheriting from `UssdView`, our class
`AccountInfoView` can now tie requests it receives to a session.

Next lets edit the `UssdIntroduction/urls.py` and add a url that will link to `AccountInfoView` that we created.

After the change, the file looks like this.

    from django.contrib import admin
    from django.urls import path
    from core.views import AccountInfoView

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('ussd/', AccountInfoView.as_view())
    ]

    This change is to add `ussd' path, so that a request to `http://localhost:8006/ussd`
    is routed to `AccountInfoView` which will serve a response back.


Next, lets add our menus.

We begin by making this change in the `core/views.py` file and its now looks like:

    from ussd.core import UssdView, UssdRequest
    import os


    class AccountInfoView(UssdView):
        path = os.path.dirname(os.path.abspath(__file__))
        customer_journey_conf = path + "/ussd_journey.yml"

        def post(self, request):
            session_id = request.data.get('session_id')
            service_code = request.data.get('service_code')
            phone_number = request.data.get('phone_number')
            user_input = request.data.get('user_input')
            return UssdRequest(
                session_id=session_id,
                phone_number=phone_number,
                ussd_input=user_input,
                service_code=service_code,
                customer_journey_namespace=self.customer_journey_namespace,
                language='en'
            )

     Whats going on:

     We adding customer_journey_conf property, this is the file that will hold
     our customer journey in YAML syntax.

     We then create a post function, this will make our class to accept POST reqeusts.

     In the function, we initialize UssdRequest, the role of this class is to
     convert the web request to a ussd requests, and hand it over to ussd airflow.


     From here on, ussd airflow will deal with the request, read the yaml file with our screens,
     and render the correct response back.


Finally, lets take a look at the `core/ussd_journey.yml`

    initial_screen: welcome_screen

    welcome_screen:
      type: menu_screen
      text:
         en:
           Welcome
      error_message:
        en: |
          Invalid selection. Please try again.
      options:
          - text:
              en: |
                Balance
              default: en
            next_screen: Balance
          - text:
               en: |
                 Phone Number
               default: en
            next_screen: PhoneNumber


    Balance:
      type: quit_screen
      text:
        en: |
          Your balance is KES 100.
        default: en

    PhoneNumber:
      type: quit_screen
      text:
        en: |
          Your phone number is {{phone_number}}.
        default: en


    This file defines the journey the customer will have.

    The first entry is initial_screen, which marks  the first point where airflow
    should start reading and serving the menu from.

    initial_screen: welcome_screen, here its point to the next screen to which to proceed to
    which is,

    welcome_screen:
      type: menu_screen
      text:
         en:
           Welcome
      error_message:
        en: |
          Invalid selection. Please try again.
      options:
          - text:
              en: |
                Balance
              default: en
            next_screen: Balance
          - text:
               en: |
                 Phone Number
               default: en
            next_screen: PhoneNumber

      Lets go through it, the welcome_screen, has properites,
      type: sets the type of screen to render to the user
      text: The text the user on phone will see.
      options: The choices from which the user should choose from.
      error_message: the Text to render to the user in case he does not choose from the
      options that were displayed.


To test this app, lets use postman.

First lets run the application:
    python manage.py migrate
    python manage.py runserver 8006



Sample interactions,

[welcome screen][welcome-screen.png]


User respond with `1` and is served with his balance information.

[Balance screen][balance-screen.png]

We are done, for more info, check our prod code, read on django and ussd airflow.

