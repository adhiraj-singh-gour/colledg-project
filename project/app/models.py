from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    name=models.CharField(max_length=30,null=False)
    slug=models.CharField(max_length=30,null=True,unique=True)
    description=models.CharField(max_length=30,null=True)
    price=models.IntegerField(null=False)
    discount=models.IntegerField(null=False,default=0)
    active=models.BooleanField(default=False)
    date=models.DateTimeField( auto_now_add=True)
    thumbnail=models.ImageField(upload_to="thumbnail/")
    resource=models.FileField( upload_to="resource/")
    course_length=models.IntegerField(null=False)

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    description=models.CharField(max_length=30,null=False)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)

    class Meta:
        abstract = True                         # Abstract does not create a class CourseProperty.
        

# _____inherit the CoursePropeerty____

class Tag(CourseProperty):
    pass


class Prerequisite(CourseProperty):
    pass

class Learning(CourseProperty):
   pass



class Video(models.Model):
    title=models.CharField(max_length=128,null=False)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    serial_number=models.IntegerField(null=False)
    video_id = models.FileField(upload_to="video/")
    is_preview=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class UserCourse(models.Model):
    
    user=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    date=models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.course.name}'
    


class Payment(models.Model):
    
    order_id=models.CharField( max_length=50,null=False)
    payment_id=models.CharField( max_length=100)
    user_course=models.ForeignKey(UserCourse,null=True, blank=True ,on_delete=models.CASCADE)
    user=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    date=models.DateTimeField( auto_now_add=True)
    status=models.BooleanField(default=False)

 

