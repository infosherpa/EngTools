from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=250)


class TunnelFrame(models.Model):
    """All dimension inputs in mm"""
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    roof_slab_thickness = models.DecimalField(max_digits=10, decimal_places=3)
    inverse_slab_thickness = models.DecimalField(max_digits=10, decimal_places=3)
    wall_slab_thickness = models.DecimalField(max_digits=10, decimal_places=3)
    frame_inner_height = models.DecimalField(max_digits=10, decimal_places=3)
    frame_outer_height = models.DecimalField(max_digits=10, decimal_places=3)
    frame_inner_width = models.DecimalField(max_digits=10, decimal_places=3)
    frame_outer_width = models.DecimalField(max_digits=10, decimal_places=3)
    haunch_depth = models.DecimalField(max_digits=10, decimal_places=3)
    haunch_width = models.DecimalField(max_digits=10, decimal_places=3)
    cracking_mod_compressive = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    cracking_mod_shear = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    cracking_mod_bending = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    frame_description = models.CharField(max_length=250)

    def __str__(self):
        return self.frame_description


class Material(models.Model):
    youngs_modulus = models.DecimalField(max_digits=10, decimal_places=4)
    compressive_strength = models.DecimalField(max_digits=10, decimal_places=4)


class SoilLayer(models.Model):
    soil_type = models.CharField(max_length=100)
    density = models.DecimalField(max_digits=10, decimal_places=4)
    SLS_bearing_strength = models.DecimalField(max_digits=10, decimal_places=3)
    ULS_bearing_strength = models.DecimalField(max_digits=10, decimal_places=3)
    #Kh
    hydraulic_conductivity_horizontal = models.DecimalField(max_digits=10, decimal_places=3)
    #Kv
    hydraulic_conductivity_vertical = models.DecimalField(max_digits=10, decimal_places=3)
    #Ko
    earth_pressure_at_rest = models.DecimalField(max_digits=10, decimal_places=3)
    layer_thinckness = models.DecimalField(max_digits=10, decimal_places=4)


class SeismicQualities(models.Model):
    free_shear_deformation = models.DecimalField(max_digits=10, decimal_places=4)
    soil_shear_modulus = models.DecimalField(max_digits=10, decimal_places=4)