from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import nested_admin
from .models import Content, CustomUser, Quiz, Question, Choice

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_teacher', 'is_student')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_teacher', 'is_student')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 4

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]

class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at')
    fields = ['title', 'description', 'file', 'body', 'youtube_url', 'uploaded_by', 'quiz']

    def save_model(self, request, obj, form, change):
        if obj.quiz:
            obj.title = obj.quiz.title
        super().save_model(request, obj, form, change)

admin.site.register(Quiz, QuizAdmin)