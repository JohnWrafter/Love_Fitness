from django import forms

from products.models import Category


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, category):
        return category.friendly_name or category.name


class ProductFinderForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        label='What are you looking for?',
        help_text='Describe the activity, item, or features you have in mind.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'For example: comfortable leggings for running',
        }),
    )
    category = CategoryChoiceField(
        queryset=Category.objects.none(),
        required=False,
        empty_label='Any category',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    max_price = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        required=False,
        label='Maximum budget (£)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'No limit',
            'min': '0',
            'step': '0.01',
        }),
    )
    consent = forms.BooleanField(
        label='I agree to send my request to OpenAI to find matching products.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.order_by(
            'friendly_name',
            'name',
        )


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


class NutritionPlanForm(forms.Form):
    GOAL_CHOICES = [
        ('balanced', 'Plan balanced everyday meals'),
        ('fitness', 'Support my fitness routine'),
        ('plant_based', 'Explore more plant-based meals'),
        ('variety', 'Add more variety to my meals'),
    ]
    MEALS_CHOICES = [(count, str(count)) for count in range(2, 7)]
    COOKING_TIME_CHOICES = [
        ('15 minutes or less', '15 minutes or less'),
        ('30 minutes', 'About 30 minutes'),
        ('45 minutes', 'About 45 minutes'),
        ('no limit', 'No time limit'),
    ]
    BUDGET_CHOICES = [
        ('budget-friendly', 'Budget-friendly'),
        ('moderate', 'Moderate'),
        ('flexible', 'Flexible'),
    ]

    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        label='Nutrition goal',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    preferences = forms.CharField(
        max_length=200,
        label='Dietary preferences',
        help_text='For example: vegetarian, vegan, or no preference.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Vegetarian, vegan, no preference...',
        }),
    )
    restrictions = forms.CharField(
        max_length=300,
        label='Food allergies or restrictions',
        help_text=(
            'List foods to exclude, or enter none. Do not include identifying '
            'or medical details.'
        ),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'For example: peanuts, shellfish, gluten...',
        }),
    )
    meals_per_day = forms.TypedChoiceField(
        choices=MEALS_CHOICES,
        coerce=int,
        label='Meals per day',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    cooking_time = forms.ChoiceField(
        choices=COOKING_TIME_CHOICES,
        label='Cooking time',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    budget = forms.ChoiceField(
        choices=BUDGET_CHOICES,
        label='Food budget',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    consent = forms.BooleanField(
        label='I understand my answers will be sent to OpenAI to generate my meal plan.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )