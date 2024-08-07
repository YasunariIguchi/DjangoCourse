import os
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelExam.settings")
from django import setup
setup()

from ModelApp.models import Tests, Classes, Students, TestResults

from django.db.models import Avg, Max, Min, Sum

def insert_data():
    class_names =[
        "classA",
        "classB",
        "classC",
        "classD",
        "classE",
        "classF",
        "classG",
        "classH",
        "classI",
        "classJ",
    ]
    student_names =[
        "studentA",
        "studentB",
        "studentC",
        "studentD",
        "studentE",
        "studentF",
        "studentG",
        "studentH",
        "studentI",
        "studentJ",
    ]
    test_names = [
        "数学",
        "英語",
        "国語",
    ]
    for class_name in class_names:
        class_obj, created=Classes.objects.update_or_create(name=class_name)
        
        for student_name in student_names:
            Students.objects.update_or_create(name=f'{class_name} {student_name}',classes=class_obj, grade=1)
    
    for test_name in test_names:
        test_obj, created=Tests.objects.update_or_create(name=test_name)
    
    # insert test_result
    for student in Students.objects.all():
        for test in Tests.objects.all():
            score = random.randint(50,100)
            TestResults.objects.update_or_create(
                student=student,
                test=test,
                defaults={"score": score} 
            )
        
def check_student1():
    try:
        student = Students.objects.get(id=1)
        print(f"Student Name: {student.name}")
        
        test_results = TestResults.objects.filter(student=student)
        for result in test_results:
            print(f"Test: {result.test.name}, Score: {result.score}")
    except Students.DoesNotExist:
        print("Student with ID 1 does not exist.")
          
def analyze_test_result():
    classes = Classes.objects.all()
    tests = Tests.objects.all()
    
    for class_obj in classes:
        print(f"Class: {class_obj.name}")
        for test in tests:
            results = TestResults.objects.filter(student__classes=class_obj, test=test)
            total_score = results.aggregate(Sum('score'))['score__sum'] or 0
            avg_score = results.aggregate(Avg('score'))['score__avg'] or 0
            max_score = results.aggregate(Max('score'))['score__max'] or 0
            min_score = results.aggregate(Min('score'))['score__min'] or 0
            
            print(f"  Test: {test.name}")
            print(f"    Total Score: {total_score}")
            print(f"    Average Score: {avg_score:.2f}")
            print(f"    Max Score: {max_score}")
            print(f"    Min Score: {min_score}")
    


#insert_data()
#check_student1()
analyze_test_result()
