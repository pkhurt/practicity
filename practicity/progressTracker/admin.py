from django.contrib import admin

from .models import Exercise, PracticeSession


# Register your models here.
class ExerciseInline(admin.StackedInline):
    model = Exercise
    extra = 3


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise_name', 'exercise_executed', 'was_added_recently')

    fieldsets = [
        (None, {'fields': ['exercise_name']}),
        ('Time information', {'fields': ['exercise_add_date', 'exercise_executed']}),
        ('Related practice session', {'fields': ['practice_session']}),
    ]


class PracticeSessionAdmin(admin.ModelAdmin):
    inlines = [ExerciseInline]


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(PracticeSession, PracticeSessionAdmin)

