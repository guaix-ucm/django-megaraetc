from django.contrib import admin

# Register your models here.
from .models import SpectralTemplate
from .models import PhotometricFilter
from .models import VPHSetup


admin.site.register(VPHSetup)
admin.site.register(SpectralTemplate)
admin.site.register(PhotometricFilter)
