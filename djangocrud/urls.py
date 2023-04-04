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
from tasks import views
from pointing_poker import views as pointerviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signup, name='signup'),
    path('tasks/',views.tasks, name='tasks'),
    path('tasks_completed/',views.tasks_completed, name='tasks_completed'),
    path('logout/',views.signout, name='logout'),
    path('snippet/',views.snippet, name='snippet'),
    path('snippets/',views.snippets, name='snippets'),
    path('tasks/create/',views.create_task, name='create_task'),
    path('tasks/<int:task_id>/',views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/completed',views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete',views.delete_task, name='delete_task'),
    path('signin/',views.signin, name='signin'),
    path('pointing/',pointerviews.game_session_list, name='pointing'),
    path('pointing/create_game_session',pointerviews.create_game_session, name='game_session'),
    path('pointing/join_session/<int:game_session_id>/',pointerviews.join_session, name='join_session'),
    path('pointing/game_session/<int:game_session_id>/card_selection/<int:user_id>/', pointerviews.card_selection, name='select_cards'),


]
