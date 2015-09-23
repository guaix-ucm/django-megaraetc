from django.db import models

class SpectralTemplate(models.Model):
    name = models.CharField(max_length=10)
    path = models.CharField(max_length=100)

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


    def __str__(self):
        return self.name

