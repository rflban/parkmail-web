from django.urls import path
from django.views.generic import RedirectView
from core.views import LastestQuestionsView, HotQuestionsView, TagView, \
                       QuestionView, QuestionFormView, SettingsView, \
                       SignUpView, SignInView


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home', permanent=False), name='index'),
    path('home/', LastestQuestionsView.as_view(), name='home'),
    path('home/', LastestQuestionsView.as_view(), name='new_questions'),
    path('hot/', HotQuestionsView.as_view(), name='hot_questions'),
    path('tag/<str:tag>', TagView.as_view(), name='tag'),
    path('question/<int:id>', QuestionView.as_view(), name='question'),
    path('question/new', QuestionFormView.as_view(), name='question_form'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
]
