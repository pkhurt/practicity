from django.contrib import admin

from .models import Exercise, Execution, ExerciseReference


# Register your models here.
# class ExerciseInline(admin.StackedInline):
#     model = Exercise
#     extra = 3
#
#
class ExerciseAdmin(admin.ModelAdmin):
    """
    This class defines the look and feel of the model Exercise in Admin
    e.g. the list_display, filter definitions, search fields, groupings
    """

    fieldsets = [
        (None, {'fields': ['exercise_name']}),
        ('Time information', {'fields': ['exercise_added']}),
        ('Reference', {'fields': ['exercise_reference']}),
    ]

    # Admin change list
    list_display = ('exercise_name', 'was_added_recently')
    list_filter = ['exercise_added']
    search_fields = ['exercise_name']


class ExerciseReferenceAdmin(admin.ModelAdmin):
    """
    This class defines the look and feel of the model ExerciseReference in Admin
    e.g. the list_display, filter definitions, search fields, groupings
    """
    list_display = ('exercise_reference_name', 'exercise_reference_author', 'exercise_reference_ISBN')
    search_fields = ['exercise_reference_name', 'exercise_reference_author']


class ExecutionAdmin(admin.ModelAdmin):
    """
    This class defines the look and feel of the model Execution in Admin
    e.g. the list_display, filter definitions, search fields, groupings
    """
    list_display = ('date_of_execution_formatted', 'duration_executed', 'execution_rating', 'was_executed_recently')
    list_filter = ['execution_start']


# class ExecutionAdmin(admin.ModelAdmin):
#     inlines = [ExerciseInline]

# Register Models
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(ExerciseReference, ExerciseReferenceAdmin)

