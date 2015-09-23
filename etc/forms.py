
from django import forms

from .models import SpectralTemplate, VPHSetup
from .models import PhotometricFilter


OMODE = [
 (1, 'LCB'),
 (2, 'MOS'),
]

MOONPH = [
 (1, 'B'),
 (2, 'G'),
 (3, 'D'),
]

STYPE=[('point','Point'),
       ('extended','Extended')]

IFLUX=[('cont','Cont'),
       ('lpcont','L+Cont')]

def template_choice():
    return [(o.pk, o.name) for o in SpectralTemplate.objects.all()]

def vph_choice():
    return [(o.pk, o.name) for o in VPHSetup.objects.all()]

def filter_choice():
    return [(o.pk, o.name) for o in PhotometricFilter.objects.all()]


class TargetForm(forms.Form):
    stype = forms.ChoiceField(label="Source type", choices=STYPE, widget=forms.RadioSelect())
    size = forms.FloatField(initial=1.0, min_value=0.0, max_value=3600)
    iflux = forms.ChoiceField(label="Input flux", choices=IFLUX, widget=forms.RadioSelect())
    pfilter = forms.ChoiceField(label="Band", choices=filter_choice)
    spectype = forms.ChoiceField(label="Input spectrum", choices=template_choice)
    rline = forms.BooleanField(label="Resolved line")

class InstrumentForm(forms.Form):
    omode = forms.ChoiceField(label="Observing mode", choices=OMODE)
    vph = forms.ChoiceField(label="VPH setup", choices=vph_choice)

class AtmosphericConditionsForm(forms.Form):
    moonph = forms.ChoiceField(label="Moon pahse", choices=MOONPH)
    airmmass = forms.FloatField(label="Airmass", initial=1.0, min_value=0.0, max_value=5)
    seeing = forms.FloatField(label="Seeing", initial=0.5, min_value=0.0, max_value=5)

class ObservationalSetupForm(forms.Form):
    exptime = forms.FloatField(initial=14.0, min_value=1.0, max_value=3600)
    nfibers = forms.IntegerField(initial=56, min_value=0, max_value=3600)
