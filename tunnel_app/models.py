from django.db import models


class TunnelFrame(models.Model):
    """All dimension inputs in mm"""
    thickness = models.DecimalField(max_digits=10, decimal_places=4)
    inner_height = models.DecimalField(max_digits=10, decimal_places=4)
    outer_height = models.DecimalField(max_digits=10, decimal_places=4)
    inner_length = models.DecimalField(max_digits=10, decimal_places=4)
    outer_length = models.DecimalField(max_digits=10, decimal_places=4)
    haunch_depth = models.DecimalField(max_digits=10, decimal_places=4)
    haunch_width = models.DecimalField(max_digits=10, decimal_places=4)
    cracking_mod_compressive = models.DecimalField(max_digits=10, decimal_places=4)
    cracking_mod_shear = models.DecimalField(max_digits=10, decimal_places=4)
    cracking_mod_bending = models.DecimalField(max_digits=10, decimal_places=4)


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