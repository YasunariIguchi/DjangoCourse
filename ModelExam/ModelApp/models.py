from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Tests(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "tests"
        
    def __str__(self) -> str:
        return self.name
        
class Classes(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "classes"

class Students(models.Model):
    GRADE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    ]
    name = models.CharField(max_length=50)
    classes = models.ForeignKey("Classes", on_delete=models.CASCADE)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    
    class Meta:
        db_table = "students"
        
    def __str__(self) -> str:
        return self.name
    
class TestResults(models.Model):
    student = models.ForeignKey("Students", on_delete=models.CASCADE)
    test = models.ForeignKey("Tests", on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        db_table = "test_results"
        
    def __str__(self) -> str:
        return f"{self.student.name} - {self.test.name}: {self.score}"