from django import forms
from music_app.models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'duration', 'release_year', 'main_artist', 'genre', 'album']
        widgets = {
            'duration': forms.TimeInput(attrs={'type': 'time', 'step': '1'}),
            'release_year': forms.NumberInput(attrs={'min': 1900, 'max': 2030}),
        }