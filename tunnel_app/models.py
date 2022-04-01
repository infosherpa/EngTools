from django.db import models
from django.conf import settings
from .functions.geometry import get_grid_lines, get_geometry, get_member_name
from openpyxl import Workbook, load_workbook
from decimal import *


class TunnelFrame(models.Model):
    """
    The Core Tunnel-Frame object, consisting of the member dimensions, strength co-efficients and stiffness modifiers

    All dimension inputs in mm Frames are by default drawn on an X-Z axis (y=0),
    in relation to the SAP X-Y-Z 3D modelling system
    """
    dimension_system_choices = (
        ("Metric_Standard", "N mm C"),
    )
    plane_choice = [
        ("xz", "x-z"),
    ]

    column_depth_choices = [
        (1, "1000mm"),
        (2, "Column Width")
    ]

    dimension_system = models.CharField(max_length=15, choices=dimension_system_choices, default='Metric_Standard')
    plane = models.CharField(max_length=2, choices=plane_choice, default='xz')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    roof_slab_thickness = models.DecimalField(max_digits=10, decimal_places=2)
    inverse_slab_thickness = models.DecimalField(max_digits=10, decimal_places=2)
    wall_slab_thickness = models.DecimalField(max_digits=10, decimal_places=2)
    frame_inner_height = models.DecimalField(max_digits=10, decimal_places=2)
    frame_outer_height = models.DecimalField(max_digits=10, decimal_places=2)
    frame_inner_width = models.DecimalField(max_digits=10, decimal_places=2)
    frame_outer_width = models.DecimalField(max_digits=10, decimal_places=2)
    haunch_depth = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    haunch_width = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cracking_mod_compressive = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cracking_mod_shear = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cracking_mod_bending = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    frame_description = models.CharField(max_length=250)
    concourse_slab_thickness = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    concourse_haunch_depth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    concourse_haunch_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    concrete_strength = models.CharField(max_length=12, default="4000Psi")

    # The model explicitly deals with 1 or 2 bay tunnel-frames.

    column_bays = models.IntegerField(default=1)
    column_capital_height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    column_capital_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    column_capital_roof_slab_height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    column_capital_roof_slab_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    concourse_slab_vertical_location = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    column_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hash = models.SlugField(max_length=8, null=True)

    column_stiffness_modifier = models.FloatField(default=0.7, null=True)
    wall_stiffness_modifier = models.FloatField(default=0.7, null=True)
    slab_stiffness_modifier = models.FloatField(default=0.5, null=True)

    column_depth_for_analysis = models.FloatField(choices=column_depth_choices, default=1)

    concrete_strength_walls = models.IntegerField(default=5000)
    concrete_strength_slabs = models.IntegerField(default=5000)
    concrete_strength_columns = models.IntegerField(default=5000)

    frame_image = models.ImageField(null=True)
    base_restraint = models.BooleanField(default=False)

    inverse_slab_stiffness = models.IntegerField(default=55)
    wall_slab_stiffness = models.IntegerField(default=20)

    def __str__(self):
        return self.frame_description

    def get_absolute_url(self):
        pass

    def get_column_spacing(self, column_center_location):

        self.custom_column_spacing = None

    def concourse_default_height(self):
        """Returns the center value for the concourse position in a symmetrical frame"""
        if self.concourse_slab_thickness:
            height = self.frame_outer_height/Decimal(2)
            return height

    def grid_lines(self):
        """Grid Lines for the SAP2000 model occur on each plane where a key vertex exists
        This function calls a geometry function to assign the SAP grid lines to model objects"""
        self.grid_locations_x, self.grid_locations_z = get_grid_lines(self)

    def get_frame_geometry(self):
        """Defines the Object Members between adjacent Vertexes depending on Frame Geometry"""
        geometry_data = get_geometry(self)
        vertexes = geometry_data['vertexes']

        # Point#, X, Z
        points = {}

        members_list = {}

        # Frame#, JointI, JointJ

        i = 1
        for vertex in vertexes.values():
            points[i] = (vertex[0], vertex[1])
            i += 1
        self.joint_coordinates = points

        key_x_axis = geometry_data['key_x_axis']
        key_z_axis = geometry_data['key_z_axis']

        member_counter = 1
        for axis in key_x_axis:
            point_a = None
            x_points = {p: val for (p, val) in points.items() if points[p][0] == axis}
            x_points = dict(sorted(x_points.items(), key=lambda x: -(x[1][1])))
            # print(x_points)
            for point in x_points.keys():
                if point_a is not None:
                    name = get_member_name(self.joint_coordinates[point_a], self.joint_coordinates[point], self)
                    members_list[member_counter] = (point_a, point, name)
                    member_counter += 1
                point_a = point

        for axis in key_z_axis:
            point_a = None
            z_points = {p: val for (p, val) in points.items() if points[p][1] == axis}
            z_points = dict(sorted(z_points.items(), key=lambda x: x[1][0]))

            for point in z_points.keys():
                if point_a is not None:
                    name = get_member_name(self.joint_coordinates[point_a], self.joint_coordinates[point], self)
                    members_list[member_counter] = (point_a, point, name)
                    member_counter += 1
                point_a = point

        self.connectivity_frame = members_list


class LoadDefinition(models.Model):
    """Load Definition - Load Surface and Load Type
    Variable load with depth for Soil Loadings"""
    loading = [
        ("LL_RS", "Live Load Roof Slab"),
        ("LL_CS", "Live Load Concourse Slab"),
        ("H_L", "Soil Load Left Side Frame"),
        ("R_L", "Soil Load Right Side Frame"),
    ]
    load_direction_choices = [
        ("Gravity", "Gravity"),
        ("X", "Horizontal (X-Plane)")
    ]
    live_load_locations = [
        ("RS", "Roof Slab"),
        ("FS", "Floor Slab"),
        ("CS", "Concourse Slab"),
        ("LW", "Left Wall"),
        ("RW", "Right Wall")
    ]

    parent_frame = models.ForeignKey(TunnelFrame, on_delete=models.CASCADE)
    parent_frame_description = models.CharField(max_length=100, null=True)
    load_id = models.AutoField(primary_key=True)
    load_pattern_description = models.CharField(choices=loading, max_length=20)
    load_direction = models.CharField(choices=load_direction_choices, max_length=20)
    start_force = models.FloatField()
    end_force = models.FloatField()
    load_location = models.CharField(choices=live_load_locations, max_length=2)
    force_start_depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    force_end_depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def str(self):
        return self.loading


class FrameMember(models.Model):
    plane_choice = [
        ("GLOBAL", "GLOBAL"),
    ]
    line_object = [
        ("str_fr", "Straight Frame"),
    ]

    parent_frame = models.ForeignKey(TunnelFrame, on_delete=models.CASCADE)
    member_id = models.IntegerField(primary_key=True)
    co_ordinate_system = models.CharField(choices=plane_choice, default=plane_choice[0], max_length=20)
    line_object_type = models.CharField(choices=line_object, max_length=20)
    start_joint = models.IntegerField()
    end_joint = models.IntegerField()


class FrameJoint(models.Model):
    """Frame Joint Object"""
    parent_frame = models.ForeignKey(TunnelFrame, on_delete=models.CASCADE)
    joint_id = models.IntegerField(primary_key=True)
    x_coordinate = models.FloatField(max_length=5)
    y_coordinate = models.FloatField(max_length=5)
    z_coordinate = models.FloatField(max_length=5)


class Material(models.Model):
    """Material Class with material characteristics"""
    youngs_modulus = models.DecimalField(max_digits=10, decimal_places=4)
    compressive_strength = models.DecimalField(max_digits=10, decimal_places=4)


class SoilLayer(models.Model):
    soil_type = models.CharField(max_length=100)
    density = models.DecimalField(max_digits=10, decimal_places=4)
    SLS_bearing_strength = models.DecimalField(max_digits=10, decimal_places=3)
    ULS_bearing_strength = models.DecimalField(max_digits=10, decimal_places=3)
    # Kh
    hydraulic_conductivity_horizontal = models.DecimalField(max_digits=10, decimal_places=3)
    # Kv
    hydraulic_conductivity_vertical = models.DecimalField(max_digits=10, decimal_places=3)
    # Ko
    earth_pressure_at_rest = models.DecimalField(max_digits=10, decimal_places=3)
    layer_thinckness = models.DecimalField(max_digits=10, decimal_places=4)


class SeismicQualities(models.Model):
    free_shear_deformation = models.DecimalField(max_digits=10, decimal_places=4)
    soil_shear_modulus = models.DecimalField(max_digits=10, decimal_places=4)
