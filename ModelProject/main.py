import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Person

p = Person(
    first_name="Taro", last_name="Yamada",
    birthday="1990-01-01", email="aa@bb.com",
    salary=1000, memo="memodesu",web_site="http://ss.jp",
)
p = Person(
    first_name="Taro", last_name="Yamada",
    birthday="1990-01-01", email="aa@bb.com",
    salary=None, memo="memodesu",web_site="http://ss.jp",
)
p = Person(
    first_name="Taro", last_name="Yamada",
    birthday="1990-01-01", email="aa@bb.com",
    salary=None, memo="memodesu",web_site="",
)

#p.save()

# classmethod create

# Person.objects.create(
#     first_name="Jiro", last_name="Ito",
#     birthday="1990-01-01", email="aa@bb.com",
#     salary=None, memo="memodesu",web_site="",
# )

#get_or_create

obj, created = Person.objects.get_or_create(
    first_name="Saburo", last_name="Ito",
    birthday="1990-01-01", email="aa@bb.com",
    salary=2, memo="memodesu",web_site="",
)

print(obj)
print(created)