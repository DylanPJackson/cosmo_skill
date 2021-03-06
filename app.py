 # -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import os
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model import ui

from flask import Flask
from flask_ask_sdk.skill_adapter import SkillAdapter

import requests
import psycopg2

import datetime
from datetime import datetime as dt, timedelta, date

from db_config import config
from cal_func import get_freebusy, get_time_available

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Instantiate flask app
app = Flask(__name__)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        logger.info("In Launch can_handle request")

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In Launch handle request")
        
        # Imiplementing testing of requests API
        url = "http://numbersapi.com/4"
        http_response = requests.get(url)
        if http_response.status_code == 200:
            the_fact = http_response.text
        else:
            the_fact = "I had some trouble getting the fact, sorry."

        speak_output = "Welcome, " + the_fact 

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        logger.info("In hello world canhandle request")
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In hello world handle request")

        # Do something to db
        ## God oh why didn't I just make all of these changes as independent handlers...
        #g_id = 4
        #explanation = "Howdy gamer, well done!"
        #time_spent = "10 minutes"
        #date = "2021-10-19"
        #sql = f"INSERT INTO goal_log VALUES ({g_id}, '{explanation}', '{time_spent}', '{date}')"
        #sql = "SELECT * FROM goal_log"
        #params = config()
        #conn = psycopg2.connect(**params)
        #cur = conn.cursor()
        #cur.execute(sql)
        #response = cur.fetchone()
        #from_db = response[1]
        #conn.commit()
        #speak_output = f"Pulling from the freebusy branch. {from_db}"
        #cur.close()
        #conn.close()

        request = handler_input.request_envelope.to_dict()
        access_token = request['context']['system']['user']['access_token']
        if access_token is None:
            speak_output = "Hey buddy, looks like your access token doesn't exist."\
                           " Better give me one if you want this to work."
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .set_card(ui.link_account_card.LinkAccountCard())
                    .response
            )
        else:
            access_token = str(access_token)
            # Will need to update this to reflect datetime of invoking Alexa
            ## Now imagine we get these times from the user... eventually
            offset = datetime.timedelta(hours=-5)
            tz = datetime.timezone(offset, name="EST")
            today = dt.now(tz)
            time_min = today.strftime("%Y-%m-%dT00:00:00-05:00")
            time_max = today.strftime("%Y-%m-%dT23:59:59-05:00") 
            time_zone = "EST"
            ## And imagine we get the calendar id from the user as well
            cal_id = "frprdjackson@gmail.com"
            freebusy_info = get_freebusy(access_token, time_min, time_max,
                                         time_zone, cal_id) 
            time_available = get_time_available(freebusy_info, cal_id)
            # Format time_available
            time_available_str = "{:.1f}".format(time_available)
            time_available_form = float(time_available_str)
            speak_output = f"You have {time_available_form} hours available today"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())


skill_adapter = SkillAdapter(skill = sb.create(), 
    skill_id = 'mzn1.ask.skill.d5ce3dbd-f734-43c6-bb5a-cdb7463e79a6',
    app = app)

@app.route("/", methods = ['POST'])
def invoke_skill():
    return skill_adapter.dispatch_request() 


if __name__ == "__main__":
    app.run("0.0.0.0", port = 8080, debug=True)
