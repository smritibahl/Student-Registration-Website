from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    city = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return '%s %s born %s lives in %s' % (self.firstname,self.lastname,self.birthdate,self.city)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    in_stock = models.BooleanField(default=True)
    numpages = models.IntegerField(validators=[MinValueValidator(50),MaxValueValidator(1000)],default=20)

    def __str__(self):
        return '%s by %s %d Pages' % (self.title,self.author,self.numpages)

class Student(User):
    PROVINCE_CHOICES = (
        ('AB', 'Alberta'),  # First value is stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    age = models.IntegerField(default=10)
    image =models.ImageField(upload_to='profile_image',blank='True')

    class Meta:
        verbose_name = "Student"


    def __str__(self):
        return '%s %s %s %d %s %s' % (self.address, self.city,self.province,self.age, self.first_name,self.last_name)


class Course(models.Model):
    course_no = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    textbook =models.ForeignKey(Book)
    student = models.ManyToManyField(Student)

    def studentdetails(self):
        return ','.join([Student.first_name for Student in self.student.all()[:3]])

    def __str__(self):
        return '%s %s %s %s' % (self.course_no,self.title,self.textbook,self.student)

class Topic(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    intro_course = models.BooleanField(default=True)
    NO_PREFERENCE = 0
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    TIME_CHOICES = (
        (0, 'No preference'),
        (1, 'Morning'),
        (2, 'Afternoon'),
        (3, 'Evening')
    )
    time = models.IntegerField(default=0, choices=TIME_CHOICES)
    num_responses = models.IntegerField(default=0)
    avg_age =models.IntegerField(default=20)

    def __str__(self):
        return self.subject