import cherrypy, json, logging
from twilio.rest import TwilioRestClient

logger = logging.getLogger(__name__)

class AlertRobinService(object):
    exposed = True

    logger.debug("Hola %s" % __name__)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self, *args, **kwargs):
        logger.info("Order created.")
        logger.debug("Request data %s" % json.dumps(cherrypy.request.json))

        # Pull config
        twilio_account = cherrypy.request.app.config['twilio']['account']
        twilio_token = cherrypy.request.app.config['twilio']['token']
        twilio_sender_number = cherrypy.request.app.config['twilio']['sender']
        
        recipients = json.loads(cherrypy.request.app.config['contactlist']['recipients'])
        message_body = cherrypy.request.app.config['contactlist']['message_body']
        logger.debug(message_body)

        # Send the SMS
        client = TwilioRestClient(twilio_account, twilio_token)

        messages = {}
        for recipient in recipients.keys():
            recipient_number = recipients[recipient]
            message = client.messages.create(from_=twilio_sender_number, to=recipient_number, body=message_body)
            messages[recipient] = message.sid
            logger.info("Sent SMS %s to %s (%s)" % (message.sid, recipient, recipient_number))

        # Respond with success
        cherrypy.response.status = "201 Resource Created"
        return messages
