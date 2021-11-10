import random
import itertools

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from faker.providers import person, lorem
from tqdm import tqdm

from core import models


fake = Faker()
fake.add_provider(lorem)
fake.add_provider(person)
avatars = ('img/samples/sonic.png', 'img/samples/ugandan.png')


def gen_users(qty: int, start_idx=1, it_num=None):
    desc = "Generate User records"
    if it_num:
        desc = f'{it_num}) {desc}'

    users = []
    for i in tqdm(range(qty), ascii=True, desc=desc, leave=False):
        idx = start_idx + i
        users.append(User(
            username=f'user_{idx}',
            password=f'user_{idx}',
            email=f'user_{idx}@example.com'
        ))
        i += 1
    return tuple(users)


def gen_profiles(qty: int, start_idx=1, it_num=None):
    desc = "Generate Profile records"
    if it_num:
        desc = f'{it_num}) {desc}'

    users = User.objects.all()[start_idx:start_idx + qty]
    profiles = []
    for user in tqdm(users, ascii=True, desc=desc, leave=False):
        profiles.append(models.Profile(
            user=user,
            avatar=random.choice(avatars),
            nickname=fake.name()
        ))
    return tuple(profiles)


def gen_tags(qty: int, start_idx=1, it_num=None):
    desc = "Generate Tag records"
    if it_num:
        desc = f'{it_num}) {desc}'

    tags = []
    for i in tqdm(range(qty), ascii=True, desc=desc, leave=False):
        tags.append(models.Tag(name=f'tag_{start_idx + i}'))
    return tuple(tags)


def gen_questions(qty: int, start_idx=1, it_num=None):
    desc = "Generate Question records"
    if it_num:
        desc = f'{it_num}) {desc}'

    profiles = tuple(models.Profile.objects.all())
    profiles_qty = len(profiles)
    questions = []
    for _ in tqdm(range(qty), ascii=True, desc=desc, leave=False):
        profile_idx = random.choice(range(profiles_qty))
        questions.append(
            models.Question(
                author=profiles[profile_idx],
                title=fake.sentence(),
                description=fake.text(),
            )
        )
    return tuple(questions)


def gen_question_tags(qty: int, start_idx=1, it_num=None):
    desc = "Generate Question-Tag records"
    if it_num:
        desc = f'{it_num}) {desc}'

    MAX_TAGS_PER_QUESTION = 5

    rels = []
    tags = tuple(models.Tag.objects.all())
    tags_qty = len(tags)
    questions = tuple(models.Question.objects.all()[start_idx:start_idx + qty])

    for question in tqdm(questions, ascii=True, desc=desc, leave=False):
        tags_per_question = random.randint(1, MAX_TAGS_PER_QUESTION)
        tags_indices = random.sample(range(tags_qty), tags_per_question)
        for tag_idx in tags_indices:
            rels.append(
                models.Question.tags.through(
                    question=question,
                    tag=tags[tag_idx]
                )
            )

    return tuple(rels)


def gen_comments(qty: int, start_idx=1, it_num=None):
    desc = "Generate Comment records"
    if it_num:
        desc = f'{it_num}) {desc}'

    profiles = models.Profile.objects.all()
    profiles_qty = profiles.count()
    questions = models.Question.objects.all()
    questions_qty = questions.count()
    comments = []

    profiles = tuple(profiles)
    questions = tuple(questions)

    for _ in tqdm(range(qty), ascii=True, desc=desc, leave=False):
        profile_idx = random.randint(0, profiles_qty - 1)
        question_idx = random.randint(0, questions_qty - 1)
        comments.append(models.Comment(
            author=profiles[profile_idx],
            question=questions[question_idx],
            content=fake.text(),
            is_correct=(random.choice((True, False))),
        ))
        pass

    return tuple(comments)


def create_gen_questions_likes():
    questions_id = tuple(models.Question.objects.all().values_list('id', flat=True))
    profiles_id = tuple(models.Profile.objects.all().values_list('id', flat=True))

    like_rel = itertools.product(questions_id, profiles_id)

    def gen_question_likes(qty: int, start_idx=1, it_num=None):
        desc = "Generate QuestionRatingPoint records"
        if it_num:
            desc = f'{it_num}) {desc}'

        likes = []

        for _ in tqdm(range(qty), ascii=True, desc=desc, leave=False):
            question_id, profile_id = next(like_rel)

            likes.append(models.QuestionRatingPoint(
                profile_id = profile_id,
                question_id = question_id,
                type=random.choice(('l', 'd')),
            ))

        return tuple(likes)

    return gen_question_likes


def create_gen_comments_likes():
    comments_id = tuple(models.Comment.objects.all().values_list('id', flat=True))
    profiles_id = tuple(models.Profile.objects.all().values_list('id', flat=True))

    like_rel = itertools.product(comments_id, profiles_id)

    def gen_comment_likes(qty: int, start_idx=1, it_num=None):
        desc = "Generate CommentRatingPoint records"
        if it_num:
            desc = f'{it_num}) {desc}'

        likes = []

        for _ in tqdm(range(qty), ascii=True, desc=desc, leave=False):
            comment_id, profile_id = next(like_rel)

            likes.append(models.CommentRatingPoint(
                profile_id = profile_id,
                comment_id = comment_id,
                type=random.choice(('l', 'd')),
            ))

        return tuple(likes)

    return gen_comment_likes


def fill_tables(table, gen, qty: int, label: str, chunk_size=100_000):
    filled_qty = 0

    fill_range = tuple(map(lambda n: (n + 1) * chunk_size,
                           range(qty // chunk_size)))
    if qty % chunk_size > 0:
        fill_range +=  (qty % chunk_size,)

    i = 1
    for chunk in tqdm(fill_range, ascii=True, desc=label):
        records = gen(chunk, filled_qty + 1, i)
        table.objects.bulk_create(records)
        filled_qty += chunk
        i += 1


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        USERS_QTY = 10_000
        TAGS_QTY = 10_000
        QUESTIONS_QTY = 100_000
        COMMENTS_QTY = 1_000_000
        QUESTION_LIKES_QTY = 1_000_0
        COMMENT_LIKES_QTY = 1_000_000

        fill_tables(
            User, gen_users,
            USERS_QTY, "Filling User table",
        )
        fill_tables(
            models.Profile, gen_profiles,
            USERS_QTY, "Filling Profile table",
        )
        fill_tables(
            models.Tag, gen_tags,
            TAGS_QTY, "Filling Tag table",
        )
        fill_tables(
            models.Question, gen_questions,
            QUESTIONS_QTY, "Filling Question table", 10_000
        )
        fill_tables(
            models.Question.tags.through, gen_question_tags,
            QUESTIONS_QTY, "Filling Question-Tag table", 10_000
        )
        fill_tables(
            models.Comment, gen_comments,
            COMMENTS_QTY, "Filling Comment table", 10_000
        )
        fill_tables(
            models.QuestionRatingPoint, create_gen_questions_likes(),
            QUESTION_LIKES_QTY, "Filling QuestionRatingPoint table", 10_000
        )
        fill_tables(
            models.CommentRatingPoint, create_gen_comments_likes(),
            COMMENT_LIKES_QTY, "Filling CommentRatingPoint table", 10_000
        )
