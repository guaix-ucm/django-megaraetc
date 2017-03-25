from django.db import models


class SpectralTemplate(models.Model):
    name = models.CharField(max_length=10)
    path = models.CharField(max_length=100)
    class Meta:
        managed = True
        db_table = 'etc_spectraltemplate'

    def __str__(self):
        return self.name


class PhotometricFilter(models.Model):
    name = models.CharField(max_length=10)
    path = models.CharField(max_length=100)
    cwl = models.FloatField()
    width = models.FloatField()
    lambda_b = models.FloatField()
    lambda_e = models.FloatField()
    mvega = models.FloatField()
    fvega = models.FloatField()
    class Meta:
        managed = True
        db_table = 'etc_photometricfilter'

    def __str__(self):
        return self.name

class VPHSetup(models.Model):
    name = models.CharField(max_length=10)
    fwhm = models.FloatField()
    dispersion = models.FloatField()
    deltab = models.FloatField()
    lambdac = models.FloatField()
    relatedband = models.CharField(max_length=10)
    lambda_b = models.FloatField()
    lambda_e = models.FloatField()
    specconf = models.CharField(max_length=10)
    specconf2 = models.CharField(max_length=10)
    class Meta:
        managed = True
        db_table = 'etc_vphsetup'

    def __str__(self):
        return self.name

class SeeingTemplate(models.Model):
    name = models.FloatField()
    centermean = models.FloatField()
    ring1mean = models.FloatField()
    ring2mean = models.FloatField()
    total = models.FloatField()
    class Meta:
        managed = True
        db_table = 'etc_seeingtemplate'

    def __str__(self):
        return  str(self.name)

# class MyModel(models.Model):
#     # file will be uploaded to MEDIA_ROOT/uploads; MEDIA_ROOT e.g. "/var/www/example.com/media/"
#     myfile = models.FileField(upload_to='uploads/')
#     # mag = models.FloatField()
#     # filt = models.CharField(max_length=100)
#     # print 'uploaded'
#     #
#     # def __str__(self):
#     #     return  str(self.filename)
#
# class Document(models.Model):
#     description = models.CharField(max_length=255, blank=True)
#     document = models.FileField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)