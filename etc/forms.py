
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

SKYCOND = [
 ('Photometric', 'Photometric'),
 ('Clear', 'Clear'),
 ('Spectroscopic', 'Spectroscopic'),
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
    botton = "<a class=\"\" href=\"Javascript:newPopupBig('/static/etc/help/%s.txt');\" type=\"link\"><span class=\"glyphicon glyphicon-question-sign\"></span></a>"
    size_help = botton % "size"
    contfluxval_help = botton % "continuumflux"
    contmagval_help = botton % "continuummagnitude"
    lineflux_help = botton % "lineflux.txt"
    linewave_help = botton % "inewavelength"
    linefwhm_help = botton % "linefwhm"

    stype = forms.ChoiceField(label="Source type", initial="P", choices=STYPE, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selector()'}))
    size = forms.FloatField(label="Size", initial=1.0, min_value=0.0, max_value=3600, help_text=size_help, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))

    iflux = forms.ChoiceField(label="Input flux", initial="C", choices=IFLUX, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selectInputflux()'}))
    rline = forms.ChoiceField(label="Resolved line?", initial="N", choices=RLINECHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selectRline()','disabled':'true'})) #attrs={'disabled':'disabled'}

    spectype = forms.ChoiceField(label="Input spectrum", initial=1, choices=template_choice()) #, widget=forms.Select(attrs={'size':'4', 'style':'width:100px' }))
    pfilter = forms.ChoiceField(label="Continuum band", initial=3, choices=filter_choice()) #, widget=forms.Select(attrs={'size':'5', 'style':'width:100px' }))

    contmagflux = forms.ChoiceField(label="", initial="M", choices=CONTMAGFLUX, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selectcontmagflux()'}))
    contmagval = forms.FloatField(label="Continuum mag", help_text=contmagval_help, initial=20.0, widget=forms.TextInput(attrs={'size':'7'}))
    contfluxval = forms.FloatField(label="Continuum flux", help_text=contfluxval_help, initial=1e-16, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))

    lineflux = forms.FloatField(label="Line flux (cgs units)", help_text=lineflux_help, initial=1e-13, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))
    linewave = forms.FloatField(label="Line wavelength (Angstroms)", help_text=linewave_help, initial=6562.8, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))
    linefwhm = forms.FloatField(label="Line FWHM (Angstroms)", help_text=linefwhm_help, initial=6, widget=forms.TextInput(attrs={'size':'7','disabled':'true'}))


class InstrumentForm(forms.Form):
    botton = "<a class=\"\" href=\"Javascript:newPopupBig('/static/etc/help/%s');\" type=\"link\"><span class=\"glyphicon glyphicon-question-sign\"></span></a>"
    om_val_help = botton % "observingmodes.txt"
    vph_help = botton % "vphsetup.html"

    om_val = forms.ChoiceField(label="Observing mode", help_text=om_val_help, initial="LCB", choices=OMODE) #, widget=forms.Select(attrs={'size':'2', 'style':'width:100px' }))
    vph = forms.ChoiceField(label="VPH setup", help_text=vph_help, initial=1, choices=vph_choice())

class AtmosphericConditionsForm(forms.Form):
    botton = "<a class=\"\" href=\"Javascript:newPopupBig('/static/etc/help/%s');\" type=\"link\"><span class=\"glyphicon glyphicon-question-sign\"></span></a>"
    airmass_help = botton % "airmass.txt"
    seeing_help = botton % "seeing.txt"

    skycond = forms.ChoiceField(label="Sky condition", initial="Photometric", choices=SKYCOND)
    moonph = forms.ChoiceField(label="Moon phase", initial="Dark", choices=MOONPH)
    airmass = forms.FloatField(label="Airmass", help_text=airmass_help, initial=1.0, min_value=0.0, max_value=5, widget=forms.TextInput(attrs={'size':'7'}))
    seeing = forms.FloatField(label="Seeing", help_text=seeing_help, initial=0.5, min_value=0.0, max_value=5, widget=forms.TextInput(attrs={'size':'7'}))

class ObservationalSetupForm(forms.Form):
    botton = "<a class=\"\" href=\"Javascript:newPopupBig('/static/etc/help/%s');\" type=\"link\"><span class=\"glyphicon glyphicon-question-sign\"></span></a>"
    nfibers_help = botton % "skyfiber.txt"
    lineap_help = botton % "lineaperture.txt"
    contap_help = botton % "continuumaperture.txt"

    numframes = forms.IntegerField(label="Num. Exp.", initial=1, min_value=1, widget=forms.TextInput(attrs={'size':'7'}))
    exptimepframe = forms.FloatField(label="Exptime per frame (sec)", initial=3600.0, min_value=1.0, widget=forms.TextInput(attrs={'size':'7'}))
    # LCB: default=8 bundles (56 fibers), max=89 bundles (623 fibers); min= 1 bundle.
    # MOS: default=max=92 bundles (644 fibers), min= 1 bundle (7 fibers);
    nfibers = forms.IntegerField(label="(*)No. of bundles", help_text=nfibers_help, initial=8, min_value=1, max_value=89, widget=forms.TextInput(attrs={'size':'6'}))
    lineap = forms.FloatField(label="Line aperture", help_text=lineap_help, initial=1.0, widget=forms.TextInput(attrs={'size':'5','disabled':'true'}))
    contap = forms.FloatField(label="Continuum aperture", help_text=contap_help, initial=1.0, widget=forms.TextInput(attrs={'size':'5','disabled':'true'}))