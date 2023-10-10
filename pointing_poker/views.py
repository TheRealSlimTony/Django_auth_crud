# from django.shortcuts import render, redirect, get_object_or_404
# from .models import GameSession,Card,vote,Participant
# from .forms import JoinGameForm
# from django.contrib.auth.decorators import login_required
# from django.db.models import Avg
# import re


# def game_session_list(request):
#     game_sessions = GameSession.objects.all()
#     context = {'context':game_sessions}
#     return render(request, 'pointing.html', context)

# def create_game_session(request):

#     if request.method == 'POST':
#         print('*********************POST***************************',request.POST,'*********************POST***************************')
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         start_time = request.POST.get('start_time')
#         game_session = GameSession(name= name,description = description, start_time = start_time)
#         game_session.save()
#         print('game session id:',game_session.id)
#         # return render(request, 'create_game_session.html')
#         return redirect('join_session',game_session_id=game_session.id)
#         # return redirect('game_session',game_session_id=game_session.id)
#     else:
#         if request.method == 'GET':
#             print('**********************GET***************************')
#             return render(request,'create_game_session.html')

# def card_selection(request, game_session_id,user_id):
#     game_session = get_object_or_404(GameSession, id=game_session_id)

#     print('se unio con el usurio :',user_id)
#     print('game session id  :',game_session_id)
#     print(GameSession)
#     participants = Participant.objects.filter(game_session=game_session)
#     form = JoinGameForm()

#     if request.method == 'POST' and request.POST['card'] != 'Clear':
#         print('*********************esto es el post**********************\n',request.POST)
#         id = request.POST['user_id']
#         card = request.POST['card']
#         session_id = request.POST['session_id']
#         match = re.search(r'/(\d+)/$', session_id)
#         if match:
#             session_id = match.group(1)
#         print('este es el id: ',id)
#         print('este es el puntaje votado: ',card)
#         print('este es el session id:',session_id)
#         participant = Participant.objects.filter(id=id).first()
#         print(participant.name)
#         participant_name = participant.name
#         participant, created = Participant.objects.get_or_create(
#             name=participant_name,
#             game_session=game_session,
#             defaults={
#                 'voted': True,
#                 'point': int(card)
#             }
#         )
#         if not created:
#             participant.voted = True
#             participant.point = int(card)
#             participant.save()

#         score = Participant.objects.filter(game_session=session_id).aggregate(Avg('point'))['point__avg']
#         print('el avg point es :',score)
#         return render(request, 'card_selection.html', {
#                 'participants': participants,
#                 'user_id':user_id,
#                 'session_id':"http://127.0.0.1:8000/pointing/join_session/{}/".format(game_session_id),
#                 'score':score
#             })
#     elif request.method == 'POST' and request.POST['card'] == 'Clear':
#         Participant.objects.all().update(point=0)
#         Participant.objects.all().update(voted=0)
#         return render(request,'card_selection.html',{
#             'game_session': game_session,
#             'participants': participants,
#             'user_id': user_id,
#             'session_id':"http://127.0.0.1:8000/pointing/join_session/{}/".format(game_session_id)
#         })


#     elif request.method == 'GET':
#           print('esto fue un get ')
#           return render(request, 'card_selection.html', {
#                 'game_session': game_session,
#                 'participants': participants,
#                 'user_id':user_id,
#                 'session_id':"http://127.0.0.1:8000/pointing/join_session/{}/".format(game_session_id)
#             })

# def join_session(request, game_session_id):
#     game_session = get_object_or_404(GameSession, id=game_session_id)
#     form = JoinGameForm()
#     if request.method == 'GET':
#         return render(request,'join_session.html',{'form':form,'game_session_id':game_session_id})
#     elif request.method == 'POST':
#         form = JoinGameForm(request.POST)
#         if form.is_valid():
#             # Si el formulario es válido, crear un nuevo participante y guardar la información en la base de datos
#             participant = Participant.objects.create(
#                 name=form.cleaned_data['name'],
#                 game_session=game_session
#             )
#             participant.save()
#             participants = Participant.objects.filter(game_session=game_session)
#             print(participants)
#             request.session['id']=participant.id
#             user_id = request.session['id']
#             print('el usuario: ',user_id)
#             return redirect('select_cards',game_session_id=game_session.id,user_id=user_id)

#         else:
#             return render(request, 'join_session.html', {'form': form, 'game_session_id': game_session_id})
