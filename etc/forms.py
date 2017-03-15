
from django import forms

from .models import SpectralTemplate, VPHSetup
from .models import PhotometricFilter
from .models import SeeingTemplate

from django.utils.safestring import mark_safe

# LIST = [('value', 'label')]
STYPE = [('P', 'Point'),
         ('E', 'Extended')]

ISIZE = [('A', 'Area'),
         ('R', 'Radius')]

OMODE = [('LCB', 'LCB IFU'),
         ('MOS', 'MOS')]

SKYCOND = [('Photometric', 'Photometric'),
           ('Clear', 'Clear'),
           ('Spectroscopic', 'Spectroscopic')]

MOONPH = [('Bright', 'Bright'),
          ('Grey', 'Grey'),
          ('Dark', 'Dark')]

IFLUX = [('C', 'Continuum'),
         ('L', 'Line + Continuum')]

RLINECHOICES = [('N', 'No'),
                ('Y', 'Yes')]

PLOTCHOICES = [('no', 'No'),
                ('yes', 'Yes')]


CONTMAGFLUX = [('M', 'Continuum mag'),
               ('F', 'Continuum flux')]

CMODE = [('T', 'ExpTime to SNR'),
         ('S', 'SNR to ExpTime')]

def template_choice(iflux_var):
    if iflux_var == 'C' or iflux_var:
        q = SpectralTemplate.objects.all()#[0:46]
        q = q.exclude(name__contains='smooth')
        namelist = [(o.pk, o.name) for o in q]
        return namelist


def vph_choice():
    return [(o.pk, o.name) for o in VPHSetup.objects.all()]


def filter_choice():
    return [(o.pk, o.name) for o in PhotometricFilter.objects.all()]

def seeing_choice():
    return [(o.pk, o.name) for o in SeeingTemplate.objects.all()]


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class TargetForm(forms.Form):
    botton2 = "<a class=\"\" href=\"Javascript:newPopupBig('/static/etc/help/%s.txt');\" type=\"link\"><span class=\"glyphicon glyphicon-question-sign\"></span></a>"
    stype_help2 = botton2 % "sourcetype"

    botton = "<a class=\"splinkcol\" href=\"Javascript:newPopupBig('/static/etc/help/%s.txt');\" type=\"link\" >"
    suf = "Radius</a>"
    stype_help = botton % "sourcetype" + "Source Type</a>"
    inputsize_help = botton % "inputsize" + "Input Size</a>"
    size_help = botton % "size" + "Area (sq.arcsec)</a>"
    radius_help = botton % "radius" + "Radius (arcsec)</a>"
    inputflux_help = botton % "inputflux" + "Input flux</a>"
    rline_help = botton % "rline" + "Resolved line?</a>"
    inputspectrum_help = botton % "inputspectrum" + "Input spectrum</a>"
    spectype_help = botton % "contband" + "Continuum band</a>"

    contmagflux_help = botton % "contmagflux" + "</a>"
    contmagval_help = botton % "continuummagnitude" + "Continuum mag</a>"
    contfluxval_help = botton % "continuumflux" + "Continuum flux</a>"
    lineflux_help = botton % "lineflux" + "Line flux (cgs units)</a>"
    linewave_help = botton % "linewavelength" + "Line wavelength (Angstrom)</a>"
    linefwhm_help = botton % "linefwhm" + "Line FWHM (Angstrom)</a>"

    testarea = "<a href=\"Javascript:newPopupBig('/static/etc/help/size.txt');\" type=\"link\" >Area</a>"

    # stype = forms.ChoiceField(label="Source type", help_text=stype_help2, initial="P", choices=STYPE, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selector()'}))
    stype = forms.ChoiceField(label=mark_safe(stype_help), initial="P", choices=STYPE, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selector()'}))
    isize = forms.ChoiceField(label=mark_safe(inputsize_help), initial="A", choices=ISIZE, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selectInputSize()','disabled':'true', 'placeholder':'inputsize'}))
    size = forms.FloatField(label=mark_safe(size_help), initial=1.0, min_value=0.0, max_value=3600, widget=forms.TextInput(attrs={'disabled':'true', 'placeholder':'Area'}))
    radius = forms.FloatField(label=mark_safe(radius_help), initial=1.0, min_value=0.0, max_value=3600, widget=forms.TextInput(attrs={'disabled':'true', 'placeholder':'Radius (arcsec)'}))

    iflux = forms.ChoiceField(label=mark_safe(inputflux_help), initial="C", choices=IFLUX, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selectInputflux()'}))
    rline = forms.ChoiceField(label=mark_safe(rline_help), initial="N", choices=RLINECHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selectRline()','disabled':'true'})) #attrs={'disabled':'disabled'}

    spectype = forms.ChoiceField(label=mark_safe(inputspectrum_help), initial=1, choices=template_choice(iflux))  # , widget=forms.Select(attrs={'size':'4', 'style':'width:100px' }))
    pfilter = forms.ChoiceField(label=mark_safe(spectype_help), initial=3, choices=filter_choice())  # , widget=forms.Select(attrs={'size':'5', 'style':'width:100px' }))

    contmagflux = forms.ChoiceField(label=" ", initial="M", choices=CONTMAGFLUX, help_text=contmagflux_help, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'onclick':'selectcontmagflux()'}))
    contmagval = forms.FloatField(label=mark_safe(contmagval_help), initial=20.0, widget=forms.TextInput(attrs={'size':'7', 'placeholder':'Continuum mag'}))
    contfluxval = forms.FloatField(label=mark_safe(contfluxval_help), initial=1e-16, widget=forms.TextInput(attrs={'size':'7','disabled':'true', 'placeholder':'Continuum flux'}))

    lineflux = forms.FloatField(label=mark_safe(lineflux_help), initial=1e-13, widget=forms.TextInput(attrs={'size':'7','disabled':'true', 'placeholder':'lineflux'}))
    linewave = forms.FloatField(label=mark_safe(linewave_help), initial=6562.8, widget=forms.TextInput(attrs={'size':'7','disabled':'true', 'placeholder':'linewave'}))
    linefwhm = forms.FloatField(label=mark_safe(linefwhm_help), initial=6, widget=forms.TextInput(attrs={'size':'7','disabled':'true', 'placeholder':'Linefwhm'}))


class InstrumentForm(forms.Form):
    # botton = "<a class=\"\" href=\"Javascript:newPopupBig('/static/etc/help/%s');\" type=\"link\"><span class=\"glyphicon glyphicon-question-sign\"></span></a>"
    botton = "<a class=\"splinkcol\" href=\"Javascript:newPopupBig('/static/etc/help/%s');\" >"
    om_val_help = botton % "observingmodes.txt" + "Observing mode</a>"
    vph_help = botton % "vphsetup.html" +"VPH setup</a>"

    om_val = forms.ChoiceField(label=mark_safe(om_val_help), initial="LCB", choices=OMODE, widget=forms.Select(attrs={'placeholder':'OM', 'onload':'selectorOmode()', 'oninput':'selectorOmode()'})) #, widget=forms.Select(attrs={'placeholder':'Observing mode'}))
    vph = forms.ChoiceField(label=mark_safe(vph_help), initial=1, choices=vph_choice())

class AtmosphericConditionsForm(forms.Form):
    hintbotton = "<a class=\"\" href=\"Javascript:newPopupBig('/static/etc/help/%s.pdf');\" type=\"link\"><span class=\"glyphicon glyphicon-question-sign\"></span></a>"
    seeing_hint = hintbotton % "seeing_values.xlsx"
    botton = "<a class=\"splinkcol\" href=\"Javascript:newPopupBig('/static/etc/help/%s.txt');\" >"
    bottonht = "<a class=\"splinkcol\" href=\"Javascript:newPopupBig('/static/etc/help/%s.html');\" >"
    skycond_help = botton % "skycond" + "Sky condition</a>"
    moonph_help = botton % "moonph" + "Moon phase</a>"
    airmass_help = botton % "airmass" + "Airmass</a>"
    # seeing_help = botton % "seeing" + "Seeing (arcsec)</a>"
    seeing_help = bottonht % "seeing" + "Seeing (arcsec)</a>"

    skycond = forms.ChoiceField(label=mark_safe(skycond_help), initial="Photometric", choices=SKYCOND)
    moonph = forms.ChoiceField(label=mark_safe(moonph_help), initial="Dark", choices=MOONPH)
    airmass = forms.FloatField(label=mark_safe(airmass_help), initial=1.0, min_value=0.0, max_value=5, widget=forms.TextInput(attrs={'placeholder':'Airmass'}))
    # seeing = forms.FloatField(label=mark_safe(seeing_help), initial=0.5, min_value=0.5, max_value=2.0, widget=forms.TextInput(attrs={'placeholder':'Seeing'}))
    seeing = forms.ChoiceField(label=mark_safe(seeing_help), help_text=seeing_hint, initial=6, choices=seeing_choice())

class ObservationalSetupForm(forms.Form):
    hintbotton = "<a class=\"\" href=\"Javascript:newPopupBig('/static/etc/help/%s.txt');\" type=\"link\"><span class=\"glyphicon glyphicon-question-sign\"></span></a>"
    ntbundles_hint = hintbotton % "hint_bundles"

    botton = "<a class=\"splinkcol\" href=\"Javascript:newPopupBig('/static/etc/help/%s.txt');\" >"
    cmode_help = botton % "cmode" + "Calculation mode</a>"
    numframes_help = botton % "numframes" + "Number of exp. frames</a>"
    exptimepframe_help = botton % "exptimeperframe" + "<span id='id_nexp'>Exptime per frame (s)</span></a>"
    nsbundles_help = botton % "skybundle" + "<span id='id_nst'>Number of Sky Fibers</span></a>"
    ntbundles_help = botton % "targetbundle" + "<span id='id_ntt'>Number of Target Fibers</span></a>"
    lineap_help = botton % "lineaperture" + "Line aperture</a>"
    contap_help = botton % "continuumaperture" + "Continuum aperture</a>"

    cmode = forms.ChoiceField(label=mark_safe(cmode_help), initial="T", choices=CMODE, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, attrs={'placeholder':'T', 'onclick':'selectorCmode()', 'onload':'selectorCmode()'}))
    numframes = forms.IntegerField(label=mark_safe(numframes_help), initial=1, min_value=1, widget=forms.TextInput(attrs={'placeholder':'numframes'}))
    exptimepframe = forms.FloatField(label=mark_safe(exptimepframe_help), initial=3600, min_value=1.0, widget=forms.TextInput(attrs={'placeholder':'exptime'}))
    # LCB: default=8 sky bundles (56 fibers), max=89 sky bundles (623 fibers); min= 1 bundle.
    # MOS: default=max=92 sky bundles (644 fibers), min= 1 bundle (7 fibers);
    nsbundles = forms.IntegerField(label=mark_safe(nsbundles_help), initial=56, min_value=1, max_value=567, widget=forms.TextInput(attrs={'placeholder':'56', 'oninput':'calculateNtbund()'}))
    ntbundles = forms.IntegerField(label=mark_safe(ntbundles_help), help_text=ntbundles_hint, initial=567, min_value=1, max_value=567, widget=forms.TextInput(attrs={'placeholder':'56', 'oninput':'calculateNsbund()'}))
    lineap = forms.FloatField(label=mark_safe(lineap_help), initial=1.0, widget=forms.TextInput(attrs={'disabled':'true', 'placeholder':'lineap'}))
    contap = forms.FloatField(label=mark_safe(contap_help), initial=1.0, widget=forms.TextInput(attrs={'disabled':'true', 'placeholder':'contap'}))

class OutputSetupForm(forms.Form):
    plotflag = forms.ChoiceField(label="Graphic output?", initial="no", choices=PLOTCHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))