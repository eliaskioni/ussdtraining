from ussd.core import UssdView, UssdRequest
import os


class AccountInfoView(UssdView):
    path = os.path.dirname(os.path.abspath(__file__))
    customer_journey_conf = path + "/ussd_journey.yml"
    customer_journey_namespace = 'USSD'

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