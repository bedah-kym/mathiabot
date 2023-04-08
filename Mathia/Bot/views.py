import json
import requests
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.trainers import ChatterBotCorpusTrainer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    """
        API endpoint to interact with ChatterBot.
    """
    endpoint = "http://127.0.0.1:8000/api/getreplies/3/"
    
    chatterbot = ChatBot(
        'Betaways',read_only=True,
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        filters = [
            'chatterbot.filters.get_recent_repeated_responses'
        ],
        preprocessors=[
            'chatterbot.preprocessors.clean_whitespace'
        ],
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function":LevenshteinDistance,
                "response_selection_method":get_most_frequent_response
            }
        ],
    )
    trainer = ChatterBotCorpusTrainer(chatterbot)
    """
    trainer.train(
    "chatterbot.corpus.english",
    )
    """
    def post(self, request,format=None):
        """
        Return a response to the statement in the posted data.
        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body)

        if 'text' not in input_data:

            return Response({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)
        self.send_reply(response)
        
        response_data = response.serialize()

        return Response(response_data, status=200)
    
    def get(self, request,format=None):
        """
        Return data corresponding to the current conversation.
        """
        return Response({
            'member': self.chatterbot.name
        })
    
    
    def send_reply(self,message):
        """
        send the message from the client in the chatapp model.
        """
        strtoken='1e51e8f61c30893852b4e42aac3bb252aa24bee0'
        endpoint = "http://127.0.0.1:8000/api/newreply/"
        headers={"Authorization":f"token {strtoken}"}
        res= requests.post(endpoint,headers=headers,data=({
            "message":message,
            "sender":"mathia",
            "command":"new_message",
            "chatid": "3"
            }))
        
    
    


