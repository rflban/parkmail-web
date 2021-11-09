from random import shuffle

profile = {
    'username': 'Little Cow',
    'avatar': 'img/samples/cow.png',
}

tags = [
    {
        'name': 'perl',
        'relevance': 4
    },
    {
        'name': 'python',
        'relevance': 1
    },
    {
        'name': 'technopark',
        'relevance': 3
    },
    {
        'name': 'mysql',
        'relevance': 1
    },
    {
        'name': 'django',
        'relevance': 2
    },
    {
        'name': 'mailru',
        'relevance': 4
    },
    {
        'name': 'voloshin',
        'relevance': 4
    },
    {
        'name': 'firefox',
        'relevance': 2
    },
]

best_members = (
    'Mr. Freeman',
    'Dr. House',
    'Bender',
    'Queen Victoria',
    'V. Pupkin',
)

def required(request):
    shuffle(tags)
    return { 'tags': tags, 'profile': profile, 'best_members': best_members, 'is_authenticated': False }
