from django.contrib import admin

from .models import Exercise, Execution, Reference, Instrument


# Inlines
class ExerciseInline(admin.StackedInline):
     model = Execution


# Model register
# The models define the look and feel of the models in Admin
# e.g. the list_display, filter definitions, search fields, groupings
class ExerciseAdmin(admin.ModelAdmin):
    """
    Model: Exercise
    """
    inlines = [
        ExerciseInline
    ]

    fieldsets = [
        (None, {'fields': ['exercise_name']}),
        ('Time information', {'fields': ['exercise_added']}),
        ('Reference', {'fields': ['exercise_reference']}),
    ]

    # Admin change list
    list_display = ('exercise_name',
                    'was_added_recently')
    list_filter = ['exercise_added']
    search_fields = ['exercise_name']


class ReferenceAdmin(admin.ModelAdmin):
    """
    Model: Reference
    """
    list_display = ('reference_name', 'reference_author', 'reference_ISBN')
    search_fields = ['reference_name', 'reference_author']


class ExecutionAdmin(admin.ModelAdmin):
    """
    Model: Execution
    """
    list_display = ('date_of_execution_formatted',
                    'duration_executed',
                    'execution_rating',
                    'was_executed_recently',
                    'instrument')
    list_filter = ['execution_start']
    search_fields = ['instrument']


class InstrumentAdmin(admin.ModelAdmin):
    """
    Model: Instrument
    """
    list_display = ('instrument_type',
                    'instrument_brand',
                    'instrument_store')


# Register Models
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Instrument, InstrumentAdmin)

