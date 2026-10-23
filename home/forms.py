from django import forms


class WorkoutRoutineForm(forms.Form):
    GOAL_CHOICES = [
        ('general_fitness', 'Improve general fitness'),
        ('build_strength', 'Build strength'),
        ('improve_endurance', 'Improve endurance'),
        ('increase_mobility', 'Improve flexibility and mobility'),
        ('get_started', 'Get started with exercise'),
    ]
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    DAYS_CHOICES = [(day, f'{day} day{"s" if day != 1 else ""}') for day in range(1, 8)]
    DURATION_CHOICES = [
        (20, '20 minutes'),
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '60 minutes'),
        (75, '75 minutes'),
    ]
    LOCATION_CHOICES = [
        ('home', 'At home'),
        ('gym', 'At a gym'),
        ('outdoors', 'Outdoors'),
        ('other', 'Somewhere else'),
    ]

    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    experience = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES,
        label='Experience level',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    days_per_week = forms.TypedChoiceField(
        choices=DAYS_CHOICES,
        coerce=int,
        label='Days per week',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    duration = forms.TypedChoiceField(
        choices=DURATION_CHOICES,
        coerce=int,
        label='Workout duration',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    equipment = forms.CharField(
        max_length=200,
        label='Available equipment',
        help_text='For example: dumbbells, resistance bands, or none.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dumbbells, resistance bands, none...',
        }),
    )
    location = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        label='Workout location',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    limitations = forms.CharField(
        max_length=500,
        label='Injuries or physical limitations (optional)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Share only what is needed to adapt exercises.',
        }),
    )
    consent = forms.BooleanField(
        label='I understand my answers will be sent to OpenAI to generate my routine.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )