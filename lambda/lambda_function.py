"""
 Copyright (C) 2020 Dabble Lab - All Rights Reserved
 You may use, distribute and modify this code under the
 terms and conditions defined in file 'LICENSE.txt', which
 is part of this source code package.
 
 For additional copyright information please
 visit : http://dabblelab.com/copyright
 """

from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model.interfaces.alexa.presentation.apl import (RenderDocumentDirective, ExecuteCommandsDirective)
from utils import (load_json_from_path, create_single_video_playlist, create_all_video_playlist, create_presigned_url)

import logging
import json
import random

# Initializing the logger and setting the level to "INFO"
# Read more about it here https://www.loggly.com/ultimate-guide/python-logging-basics/
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

playlist = [
                {
                "url": create_presigned_url("Media/001.mp4"),
                "title": "Video 1 Title",
                "subtitle": "Video 1 Subtitle"
                },
                {
                "url": create_presigned_url("Media/001.mp4"),
                "title": "Video 2 Title",
                "subtitle": "Video 2 Subtitle"
                }
            ]

# Intent Handlers

#This Handler is called when the skill is invoked by using only the invocation name(Ex. Alexa, open template four)
class LaunchRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        video_directive = RenderDocumentDirective(
                            token = "videoplayer", 
                            document = load_json_from_path("apl/render-videoplayer.json"), 
                            datasources = create_all_video_playlist(playlist)
                            )
        return (
            handler_input.response_builder
                .add_directive(video_directive)
                .response
            )

class ChooseVideoIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("ChooseVideoIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        video_number = int(handler_input.request_envelope.request.intent.slots["VideoNumberSlot"].value) - 1
        if video_number in range(0,len(playlist)-1):
            video_directive = RenderDocumentDirective(
                                token = "videoplayer",
                                document = load_json_from_path("apl/render-videoplayer.json"),
                                datasources = create_single_video_playlist(playlist, video_number)
                                )
            handler_input.response_builder.add_directive(video_directive)
        else:
            speech_output = random.choice(language_prompts["INVALID_VIDEO_NUM"]).format(1, len(playlist))
            reprompt = random.choice(language_prompts["INVALID_VIDEO_NUM_REPROMPT"])
            handler_input.response_builder.speak(speech_output).ask(reprompt)
        return (
            handler_input.response_builder
                .response
            )

class PlayIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.ResumeIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        video_directive = ExecuteCommandsDirective(
                            token = "videoplayer",
                            commands = [
                                {
                                    "type": "ControlMedia",
                                    "componentId": "videoPlayer",
                                    "command": "play"
                                },
                                {
                                    "type": "showOverlayShortly"
                                }
                            ]
                            )
        return (
            handler_input.response_builder
                .add_directive(video_directive)
                .response
            )

class PauseIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.PauseIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        video_directive = ExecuteCommandsDirective(
                            token = "videoplayer",
                            commands = [
                                {
                                    "type": "ControlMedia",
                                    "componentId": "videoPlayer",
                                    "command": "pause"
                                }
                            ]
                            )
        return (
            handler_input.response_builder
                .add_directive(video_directive)
                .response
            )

class NextIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NextIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        video_directive = ExecuteCommandsDirective(
                            token = "videoplayer",
                            commands = [
                                {
                                    "type": "Sequential",
                                    "commands": [
                                        {
                                            "type": "ControlMedia",
                                            "componentId": "videoPlayer",
                                            "command": "next"
                                        },
                                        {
                                            "type": "ControlMedia",
                                            "componentId": "videoPlayer",
                                            "command": "play"
                                        },
                                        {
                                            "type": "showOverlayShortly",
                                            "delay": "500"
                                        }
                                    ]
                                }
                            ]
                            )

        return (
            handler_input.response_builder
                .add_directive(video_directive)
                .response
            )

class PreviousIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.PreviousIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        video_directive = ExecuteCommandsDirective(
                            token = "videoplayer",
                            commands = [
                                {
                                    "type": "Sequential",
                                    "commands": [
                                        {
                                            "type": "ControlMedia",
                                            "componentId": "videoPlayer",
                                            "command": "previous"
                                        },
                                        {
                                            "type": "ControlMedia",
                                            "componentId": "videoPlayer",
                                            "command": "play"
                                        },
                                        {
                                            "type": "showOverlayShortly",
                                            "delay": "500"
                                        }
                                    ]
                                }
                            ]
                            )

        return (
            handler_input.response_builder
                .add_directive(video_directive)
                .response
            )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["CANCEL_STOP_RESPONSE"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["HELP"])
        reprompt = random.choice(language_prompts["HELP_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class UserEventHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input)
    
    def handle(self,handler_input):
        return(
            handler_input.response_builder
                .response
            )

# This handler handles utterances that can't be matched to any other intent handler.
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["FALLBACK"])
        reprompt = random.choice(language_prompts["FALLBACK_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class SessionEndedRequesthandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with the reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Exception Handlers

# This exception handler handles syntax or routing errors. If you receive an error stating 
# the request handler is not found, you have not implemented a handler for the intent or 
# included it in the skill builder below
class CatchAllExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return True
    
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = language_prompts["ERROR"]
        reprompt = language_prompts["ERROR_REPROMPT"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# Interceptors

# This interceptor logs each request sent from Alexa to our endpoint.
class RequestLogger(AbstractRequestInterceptor):

    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))

# This interceptor logs each response our endpoint sends back to Alexa.
class ResponseLogger(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))

# This interceptor is used for supporting different languages and locales. It detects the users locale,
# loads the corresponding language prompts and sends them as a request attribute object to the handler functions.
class LocalizationInterceptor(AbstractRequestInterceptor):

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        
        try:
            with open("languages/"+str(locale)+".json") as language_data:
                language_prompts = json.load(language_data)
        except:
            with open("languages/"+ str(locale[:2]) +".json") as language_data:
                language_prompts = json.load(language_data)
        
        handler_input.attributes_manager.request_attributes["_"] = language_prompts

# Skill Builder
# Define a skill builder instance and add all the request handlers,
# exception handlers and interceptors to it.

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ChooseVideoIntentHandler())
sb.add_request_handler(PlayIntentHandler())
sb.add_request_handler(PauseIntentHandler())
sb.add_request_handler(NextIntentHandler())
sb.add_request_handler(PreviousIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(UserEventHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequesthandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()