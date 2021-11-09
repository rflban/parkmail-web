from django.views.generic import ListView, TemplateView
from mimesis import Person, Text, Numeric


numeric = Numeric()
person = Person()
text = Text()

questions = [ {
    'id': numeric.increment('id_question'),
    'author': person.username(),
    'avatar': 'img/samples/sonic.png',
    'title': text.title(),
    'description': text.text(5),
    'likes_counter': '%+d' % numeric.integer_number(-100, 100),
    'comments_qty': numeric.integer_number(0, 50),
    'tags': tuple(text.word() for _ in range(numeric.integer_number(1, 10))),
} for _ in range(500) ]

comments = [ {
    'id': numeric.increment('id_comment'),
    'author': person.username(),
    'avatar': 'img/samples/ugandan.png',
    'description': text.text(3),
    'likes_counter': '%+d' % numeric.integer_number(-100, 100),
    'is_correct': numeric.integer_number(0, 1) == 1,
} for _ in range(50) ]


class LastestQuestionsView(ListView):
    template_name = 'core/questions_list.html'
    paginate_by = 5

    def get_queryset(self):
        return questions


class HotQuestionsView(ListView):
    template_name = 'core/questions_list.html'
    paginate_by = 5

    def get_queryset(self):
        return sorted(questions, key=(lambda q: int(q['likes_counter'])), reverse=True)


class TagView(ListView):
    template_name = 'core/tag_questions_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag'].lower()
        return context

    def get_queryset(self):
        tag = self.kwargs['tag'].lower()
        return tuple(filter((lambda q: tag in q['tags']), questions))


class QuestionView(ListView):
    template_name = 'core/question.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = tuple(filter(lambda q: self.kwargs['id'] == q['id'], questions))[0]
        return context

    def get_queryset(self):
        return comments


class QuestionFormView(TemplateView):
    template_name = 'core/questionform.html'


class SettingsView(TemplateView):
    template_name = 'core/settings.html'


class SignUpView(TemplateView):
    template_name = 'core/signup.html'


class SignInView(TemplateView):
    template_name = 'core/signin.html'
