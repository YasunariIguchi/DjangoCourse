import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Students, Schools, Prefectures


prefectures = ["東京", "大阪"]
schools = ["東高校", "西高校", "北高校", "南高校"]
students = ["一郎", "二郎", "三郎"]

# def insert_records():
#     for pn in prefectures:
#         pref = Prefectures(
#             name=pn
#         )
#         pref.save()
#         for sn in schools:
#             school = Schools(
#                 name=sn,
#                 prefecture = pref,
#             )
#             school.save()
#             for stn in students:
#                 student = Students(
#                     name=stn,
#                     school=school,
#                     major="物理",
#                     age=20
#                 )
#                 student.save()
# insert_records()

# Schools.objects.filter(name='東高校').delete()
Prefectures.objects.filter(name='東京').delete()