from django.contrib import admin
from .models import Author,Book,Course,Student

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','in_stock','numpages')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('firstname','lastname','birthdate','city')

@admin.register(Course)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentdetails','course_no','title','textbook')

@admin.register(Student)
class StudentdetailsAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'age','address', 'city','province' )


