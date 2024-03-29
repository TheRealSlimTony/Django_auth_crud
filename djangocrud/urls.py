"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from chat import views as chatviews
from chatgpt_module import views as chatgptviews
from pointing_poker import views as pointerviews
from service_ticket import views as tikectviews
from tasks import views
from chatbot import views as chatbotviews

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    # path("tasks/", views.tasks, name="tasks"),
    # path("tasks_completed/", views.tasks_completed, name="tasks_completed"),
    path("logout/", views.signout, name="logout"),
    path("snippet/", views.snippet, name="snippet"),
    path("snippets/", views.snippets, name="snippets"),
    path(
        "snippet_detail/<int:snippet_id>/", views.snippet_detail, name="snippet_detail"
    ),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/completed", views.complete_task, name="complete_task"),
    path("tasks/<int:task_id>/delete", views.delete_task, name="delete_task"),
    path("signin/", views.signin, name="signin"),
    # path("pointing/", pointerviews.game_session_list, name="pointing"),
    # path("pointing/create_game_session",pointerviews.create_game_session,name="game_session",),
    # path("pointing/join_session/<int:game_session_id>/",pointerviews.join_session,name="join_session",),
    # path("pointing/game_session/<int:game_session_id>/card_selection/<int:user_id>/",pointerviews.card_selectionname="select_cards",),
    path("chat/home/", chatviews.home, name="home_chat"),
    path("chat/home/room/<str:room_name>/", chatviews.room, name="room"),
    path("chat/home/check_view/", chatviews.check_view, name="check_view"),
    path("chat/home/create_qr/", chatviews.create_qr, name="create_qr"),
    path("chat/home/read_qr/", chatviews.read_qr, name="read_qr"),
    path("send/", chatviews.send, name="send"),
    path("getMessages/<str:room>/", chatviews.get_messages, name="get_messages"),
    # path("ticket/home/", tikectviews.home, name="ticket_home"),
    # path("ticket/create/", tikectviews.create, name="ticket_create"),
    # path("ticket/detail/<int:ticket_id>/", tikectviews.detail, name="ticket_detail"),
    path("chatgpt/home/", chatgptviews.home, name="home_gpt"),
    path("chatgpt/read_img/", chatgptviews.read_img, name="gpt_read_img"),
    path("chatgpt/encrypt/", chatgptviews.encrypt_text_view, name="encrypt"),
    path("chatgpt/decrypt/", chatgptviews.decrypt_text_view, name="decrypt"),
    path("chatgpt/pdf_chat/", chatgptviews.chat_pdf, name="chat_pdf"),
    path("chatbot/home/", chatbotviews.home, name="chatbot_home"),
]
