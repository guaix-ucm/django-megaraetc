
from django import forms

from .models import SpectralTemplate, VPHSetup
from .models import PhotometricFilter

from django.utils.safestring import mark_safe



# LIST = [('value', 'label')]
STYPE=[('P','Point'),
       ('E','Extended')]

OMODE = [
 ('LCB', 'LCB'),
 ('MOS', 'MOS'),
]

MOONPH = [
 ('Bright', 'Bright'),
 ('Grey', 'Grey'),
 ('Dark', 'Dark'),
]

IFLUX=[('C','Continuum'),
       ('L','Line + Continuum')]

RLINECHOICES=[('N','No'),
              ('Y','Yes')]

CONTMAGFLUX=[('M','Continuum mag'),
            ('F','Continuum flux')]

def template_choice():
    return [(o.pk, o.name) for o in SpectralTemplate.objects.all()]

def vph_choice():
    return [(o.pk, o.name) for o in VPHSetup.objects.all()]

def filter_choice():
    return [(o.pk, o.name) for o in PhotometricFilter.objects.all()]


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class TargetForm(forms.Form):
    stype = forms.ChoiceField(label="Source type", initial="P", choices=STYPE, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selector()'}))
    size = forms.FloatField(label="Size", initial=1.0, min_value=0.0, max_value=3600, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))

    iflux = forms.ChoiceField(label="Input flux", initial="C", choices=IFLUX, widget=forms.RadioSelect(attrs={'onclick':'selectInputflux()'}))
    rline = forms.ChoiceField(label="Resolved line?", initial="N", choices=RLINECHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selectRline()','disabled':'true'})) #attrs={'disabled':'disabled'}

    spectype = forms.ChoiceField(label="Input spectrum", initial=1, choices=template_choice()) #, widget=forms.Select(attrs={'size':'4', 'style':'width:100px' }))
    pfilter = forms.ChoiceField(label="Continuum band", initial=3, choices=filter_choice()) #, widget=forms.Select(attrs={'size':'5', 'style':'width:100px' }))

    contmagflux = forms.ChoiceField(label="", initial="M", choices=CONTMAGFLUX, widget=forms.RadioSelect(attrs={'onclick':'selectcontmagflux()'}))
    contmagval = forms.FloatField(label="", initial=20.0, widget=forms.TextInput(attrs={'size':'7'}))
    contfluxval = forms.FloatField(label="", initial=1e-16, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))

    lineflux = forms.FloatField(label="Line flux (cgs units)", initial=1e-13, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))
    linewave = forms.FloatField(label="Line wavelength (Angstroms)", initial=6562.8, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))
    linefwhm = forms.FloatField(label="Line FWHM (Angstroms)", initial=6, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))


class InstrumentForm(forms.Form):
    om_val = forms.ChoiceField(label="Observing mode", initial="LCB", choices=OMODE) #, widget=forms.Select(attrs={'size':'2', 'style':'width:100px' }))
    vph = forms.ChoiceField(label="VPH setup", initial=1, choices=vph_choice()) #, widget=forms.Select(attrs={'size':'3', 'style':'width:100px' }))

class AtmosphericConditionsForm(forms.Form):
    moonph = forms.ChoiceField(label="Moon phase", initial="Dark", choices=MOONPH)
    airmass = forms.FloatField(label="Airmass", initial=1.0, min_value=0.0, max_value=5, widget=forms.TextInput(attrs={'size':'7'}))
    seeing = forms.FloatField(label="Seeing", initial=0.5, min_value=0.0, max_value=5, widget=forms.TextInput(attrs={'size':'7'}))

class ObservationalSetupForm(forms.Form):
    numshot = forms.IntegerField(label="Num. Exp.", initial=1, min_value=1, widget=forms.TextInput(attrs={'size':'7'}))
    exptimepshot = forms.FloatField(label="Exptime per shot(sec)", initial=3600.0, min_value=1.0, widget=forms.TextInput(attrs={'size':'7'}))
    nfibers = forms.IntegerField(label="(*)No. of sky fibers", initial=100, min_value=0, max_value=3600, widget=forms.TextInput(attrs={'size':'6'}))
    lineap = forms.FloatField(label="Line aperture", initial=1.0, widget=forms.TextInput(attrs={'size':'5','disabled':'true'}))
    contap = forms.FloatField(label="Continuum aperture", initial=1.0, widget=forms.TextInput(attrs={'size':'5','disabled':'true'}))