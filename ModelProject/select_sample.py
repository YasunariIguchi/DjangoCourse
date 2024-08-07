import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Person

persons = Person.objects.filter(first_name="Taro")
for p in persons:
    print(p.id, p)

# print(persons)