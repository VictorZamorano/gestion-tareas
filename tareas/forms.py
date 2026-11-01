from django import forms

from .models import Tarea


class TareaForm(forms.ModelForm):
    """Formulario para la creación y edición de tareas.

    Basado en el modelo Tarea, este formulario facilita la entrada de datos
    y asegura la validación de los campos según las reglas definidas en el modelo.
    """

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'completada']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción detallada'}),
            'completada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'completada': 'Completada',
        }
        help_texts = {
            'titulo': 'El título debe ser conciso y descriptivo.',
            'descripcion': 'Proporcione detalles adicionales sobre la tarea.',
            'completada': 'Marque si la tarea ha sido completada.',
        }