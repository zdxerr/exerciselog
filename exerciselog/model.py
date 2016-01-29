# -*- coding: utf-8 -*-
"""
"""

# from datetime import datetime, date
import datetime
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash

db = SqliteDatabase('people.db')

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    password_hash = CharField()
    email = CharField(unique=True, null=True)
    join_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('username',)

    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop('password')
        if password:
            kwargs['password_hash'] = generate_password_hash(password)
        return super(User, cls).create(**kwargs)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Exercise(BaseModel):
    name = CharField(unique=True)


# Multilanguage Support
# class ExerciseNames(BaseModel):
#     exercise = ForeignKeyField(Exercise)
#     language = CharField()
#     name = CharField()
#     description = TextField()


class Session(BaseModel):
    user = ForeignKeyField(User)
    date = DateField(default=datetime.date.today)
    description = CharField(null=True)
    note = TextField(null=True)


class Set(BaseModel):
    session = ForeignKeyField(Session)
    exercise = ForeignKeyField(Exercise)
    weight = DecimalField(max_digits=2, decimal_places=2)
    repetitions = IntegerField()
    rpe = DecimalField(max_digits=2, decimal_places=1, null=True)


def create_tables():
    for model in (User, Exercise, Session, Set, ):
        model.drop_table(fail_silently=True)
        model.create_table()


if __name__ == '__main__':
    create_tables()

    lutz = User.create(username='Lutz', password='test', email=None)

    session = Session.create(user=lutz, date='2014-08-17',
                             note=("Kniebeuge 157,5x1\n"
                                   "Dücken 62,5x1\n"
                                   "Kreuzheben 180x1\n"
                                   "Bankdrücken 95x1\n"))

    sets = [
        ('Kniebeuge', 157.5, 1, 1),
        ('Drücken', 62.5, 1, 1),
        ('Kreuzheben', 180, 1, 1),
        ('Bankdrücken', 95, 1, 1),
        ('Kniebeuge', 100, 2, 5),
    ]

    # print(sets)
    for exercise, weight, number_of_sets, repetitions in sets:
        try:
            exercise = Exercise.get(Exercise.name==exercise)
        except Exercise.DoesNotExist:
            exercise = Exercise.create(name=exercise)
        for set_number in range(1, number_of_sets + 1):
            Set.create(session=session,
                       exercise=exercise,
                       weight=weight,
                       repetitions=repetitions)


    for s in Set.select().where(Set.session==session):
        print(s.exercise.name, s.weight, s.repetitions)


