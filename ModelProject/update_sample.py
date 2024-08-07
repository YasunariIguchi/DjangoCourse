import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()
from django.utils import timezone
import pytz

from ModelApp.models import Person

person= Person.objects.get(id=1)
person.birthday = '1993-02-19'
person.update_at = timezone.datetime.now(pytz.timezone("Asia/Tokyo"))
person.save()

# print(persons)

person= Person.objects.filter(first_name="Taro")
for p in person:
    p.first_name = "Yonro"
    p.update_at = timezone.datetime.now(pytz.timezone("Asia/Tokyo"))
    p.save()
    
Person.objects.filter(first_name="Yonro").update(web_site="http://igu.co", update_at=timezone.datetime.now(pytz.timezone("Asia/Tokyo")))