from django.contrib import admin

from .models import Exercise, Execution, ExerciseReference


# Register your models here.
# class ExerciseInline(admin.StackedInline):
#     model = Exercise
#     extra = 3
#
#
class ExerciseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['exercise_name']}),
        ('Time information', {'fields': ['exercise_added', 'exercise_times_executed']}),
        ('Reference', {'fields': ['exercise_reference']}),
    ]

    # Admin change list
    list_display = ('exercise_name', 'exercise_times_executed', 'was_added_recently')
    list_filter = ['exercise_added']
    search_fields = ['exercise_name']


# class ExecutionAdmin(admin.ModelAdmin):
#     inlines = [ExerciseInline]

# Register Models
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Execution)
admin.site.register(ExerciseReference)

