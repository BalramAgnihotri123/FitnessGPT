from django.urls import path
import copy

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bot.models import user_history
from bot.utils import get_response, get_linked_response, checkPrompt, checkPromptLinked
from .serializers import userSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {"POST": "sessions/"},
        {"GET": "sessions/id"},
        {"POST": "sessions/id/prompt"},
    ]
    return Response(routes)


@api_view(['POST'])
def createSession(request):
    id = None
    if id:
        pass
    else:
        user = user_history.objects.create()

    return Response({'user_id': str(user.id)})


@api_view(['GET'])
def getSession(request, id):
    user = user_history.objects.get(id = id)
    serializer  = userSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def getResponse(request, id):
    user =  user_history.objects.get(id = id)

    prompt = request.data['data']['text']

    # If user history already exist
    if user.data:
        print("\n history exits\n")
        recent_history = user.data[-4:]
        temp_recent_history = copy.deepcopy(recent_history)
        recent_history.reverse()
        linker_prompts = []
        for i in temp_recent_history:
            if i['role'] == 'USER':
                linker_prompts.append(i['text'])
            else:
                pass
        linker_prompts.append(prompt)
        linked = checkPromptLinked(linker_prompts)
        print(linked)
        # if linked
        if linked:  
            print("\nlinked\n")
            history = []
            for i in range(0, len(temp_recent_history), 2):
                try:
                    history.append({"text":f"\nuser: {temp_recent_history[i]['text']}"}) 
                    history.append({"text":f"\nbot: {temp_recent_history[i+1]['text'][:200]}"})
                except:
                    pass

            new_history = " ".join([d['text'] for d in history])
            print("new_history",new_history)

            new_prompt = " ".join([prompt, " providing the previous chat context: ", new_history])
            new_response = get_linked_response(new_prompt)

            chat_data = user.data
            chat_data.append({'role':'USER', "text":prompt})
            chat_data.append({'role':'GPT-3', "text":new_response})
            user.data = chat_data
            user.save()

        # if not linked
        else:
            fitness_related = checkPrompt(prompt)
            print("\nnot linked prompts\n")
            # if fitness related
            if fitness_related:
                print("\nfitness related\n")
                new_response = get_response(prompt)

                chat_data = user.data
                chat_data.append({'role':'USER', "text":prompt})
                chat_data.append({'role':'GPT-3', "text":new_response})
                user.data = chat_data
                user.save()

            else:
                return Response({'response': "Please be more direct as I am only programmed to answer fitness-related questions. Can you please ask a fitness-related question?"})

    else:
        print("\nno history found\n")
        fitness_related = checkPrompt(prompt)
        if fitness_related:
            print("\nfitness related\n")
            new_response = get_response(prompt)
            chat_data = user.data
            chat_data.append({'role':'USER', "text":prompt})
            chat_data.append({'role':'GPT-3', "text":new_response})
            user.data = chat_data
            user.save()
        else:
            return Response({'response': "Please be more direct as I am only programmed to answer fitness-related questions. Can you please ask a fitness-related question?"})


    return Response({'response': str(new_response)})