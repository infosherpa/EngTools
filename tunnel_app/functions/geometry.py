from decimal import *
import math


def get_geometry(TunnelFrame):
    """Return the vertex co-ordinates of the TunnelFrame Object
    0-0 is by default designated at the bottom left co-ordinate
    left, right, center, top, bottom refer to reference location of vertexes around a
    central vertex (meeting of members).
    """
    tfi = TunnelFrame
    top_centerline_y = TunnelFrame.frame_outer_height-TunnelFrame.inverse_slab_thickness/2

    inverse_slab_l_vertex_l = (0, TunnelFrame.inverse_slab_thickness/2)
    inverse_slab_l_vertex_r = (TunnelFrame.wall_slab_thickness, TunnelFrame.inverse_slab_thickness/2)
    inverse_slab_l_vertex_c = (TunnelFrame.wall_slab_thickness/2, TunnelFrame.inverse_slab_thickness/2)
    inverse_slab_l_vertex_t = (TunnelFrame.wall_slab_thickness/2, TunnelFrame.inverse_slab_thickness)
    inverse_slab_l_vertex_b = (TunnelFrame.wall_slab_thickness/2, 0)

    inverse_slab_r_vertex_l = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness, TunnelFrame.inverse_slab_thickness / 2)
    inverse_slab_r_vertex_r = (TunnelFrame.frame_outer_width, TunnelFrame.inverse_slab_thickness / 2)
    inverse_slab_r_vertex_c = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness/2, TunnelFrame.inverse_slab_thickness / 2)
    inverse_slab_r_vertex_t = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness/2, TunnelFrame.inverse_slab_thickness)
    inverse_slab_r_vertex_b = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness/2, 0)

    roof_slab_l_vertex_l = (0,TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness/2)
    roof_slab_l_vertex_r = (TunnelFrame.wall_slab_thickness,TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness/2)
    roof_slab_l_vertex_c = (TunnelFrame.wall_slab_thickness/2,TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness/2)
    roof_slab_l_vertex_t = (TunnelFrame.wall_slab_thickness/2,TunnelFrame.frame_outer_height)
    roof_slab_l_vertex_b = (TunnelFrame.wall_slab_thickness/2,TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness)

    roof_slab_r_vertex_l = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness,TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness/2)
    roof_slab_r_vertex_r = (TunnelFrame.frame_outer_width,TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness/2)
    roof_slab_r_vertex_c = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness/2,TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness/2)
    roof_slab_r_vertex_t = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness/2,TunnelFrame.frame_outer_height)
    roof_slab_r_vertex_b = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness/2,TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness)

    left_haunch_bottom = (TunnelFrame.wall_slab_thickness/2,
                          TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness-TunnelFrame.haunch_depth)
    left_haunch_top = (TunnelFrame.wall_slab_thickness+TunnelFrame.haunch_width,
                       TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness/2)
    right_haunch_bottom = (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness/2,
                           TunnelFrame.frame_outer_height - TunnelFrame.roof_slab_thickness - TunnelFrame.haunch_depth)
    right_hauch_top = (TunnelFrame.wall_slab_thickness+TunnelFrame.frame_inner_width-TunnelFrame.haunch_width,
                       TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness/2)


    # Relevant vertexes for SAP2000-compatable xlxs format workbook export

    vertexes = {
        'inverse_slab_l_vertex_l': inverse_slab_l_vertex_l,
        'inverse_slab_l_vertex_r': inverse_slab_l_vertex_r,
        'inverse_slab_l_vertex_c': inverse_slab_l_vertex_c,
        'inverse_slab_l_vertex_t': inverse_slab_l_vertex_t,
        'inverse_slab_l_vertex_b': inverse_slab_l_vertex_b,

        'inverse_slab_r_vertex_l': inverse_slab_r_vertex_l,
        'inverse_slab_r_vertex_r': inverse_slab_r_vertex_r,
        'inverse_slab_r_vertex_c': inverse_slab_r_vertex_c,
        'inverse_slab_r_vertex_t': inverse_slab_r_vertex_t,
        'inverse_slab_r_vertex_b': inverse_slab_r_vertex_b,

        'roof_slab_l_vertex_l': roof_slab_l_vertex_l,
        'roof_slab_l_vertex_r': roof_slab_l_vertex_r,
        'roof_slab_l_vertex_c': roof_slab_l_vertex_c,
        'roof_slab_l_vertex_t': roof_slab_l_vertex_t,
        'roof_slab_l_vertex_b': roof_slab_l_vertex_b,

        'roof_slab_r_vertex_l': roof_slab_r_vertex_l,
        'roof_slab_r_vertex_r': roof_slab_r_vertex_r,
        'roof_slab_r_vertex_c': roof_slab_r_vertex_c,
        'roof_slab_r_vertex_t': roof_slab_r_vertex_t,
        'roof_slab_r_vertex_b': roof_slab_r_vertex_b,

    }
    if TunnelFrame.haunch_width:
        if TunnelFrame.haunch_width > 0 :
            vertexes['left_haunch_bottom'] = left_haunch_bottom
            vertexes['left_haunch_top'] = left_haunch_top
            vertexes['right_haunch_bottom'] = right_haunch_bottom
            vertexes['right_hauch_top'] = right_hauch_top

    if TunnelFrame.concourse_slab_thickness:

        # vertexes['concourse_slab_l_vertex_l'] = (0, tfi.concourse_slab_vertical_location)
        vertexes['concourse_slab_l_vertex_r'] = (tfi.wall_slab_thickness, tfi.concourse_slab_vertical_location)
        vertexes['concourse_slab_l_vertex_c'] = (tfi.wall_slab_thickness/2, tfi.concourse_slab_vertical_location)
        vertexes['concourse_slab_l_vertex_t'] = (tfi.wall_slab_thickness/2,
                                                 tfi.concourse_slab_vertical_location+tfi.concourse_slab_thickness/2)
        vertexes['concourse_slab_l_vertex_b'] = (tfi.wall_slab_thickness/2,
                                                 tfi.concourse_slab_vertical_location-tfi.concourse_slab_thickness/2)

        vertexes['concourse_slab_r_vertex_l'] = (tfi.frame_outer_width-tfi.wall_slab_thickness,
                                                 tfi.concourse_slab_vertical_location)
        # vertexes['concourse_slab_r_vertex_r'] = (tfi.frame_outer_width, tfi.concourse_slab_vertical_location)
        vertexes['concourse_slab_r_vertex_c'] = (tfi.frame_outer_width-tfi.wall_slab_thickness/2,
                                                 tfi.concourse_slab_vertical_location)
        vertexes['concourse_slab_r_vertex_t'] = (tfi.frame_outer_width - tfi.wall_slab_thickness/2,
                                                 tfi.concourse_slab_vertical_location+tfi.concourse_slab_thickness/2)
        vertexes['concourse_slab_r_vertex_b'] = (tfi.frame_outer_width - tfi.wall_slab_thickness/2,
                                                 tfi.concourse_slab_vertical_location-tfi.concourse_slab_thickness/2)

        if TunnelFrame.concourse_haunch_depth:
            vertexes['concourse_left_haunch_bottom'] = (tfi.wall_slab_thickness/2,
                                                        tfi.concourse_slab_vertical_location-tfi.concourse_slab_thickness/2-tfi.concourse_haunch_depth)
            vertexes['concourse_left_haunch_top'] = (tfi.wall_slab_thickness+tfi.concourse_haunch_width,
                                                     tfi.concourse_slab_vertical_location)
            vertexes['concourse_right_haunch_bottom'] = (tfi.frame_outer_width-tfi.wall_slab_thickness/2,
                                                      tfi.concourse_slab_vertical_location-tfi.concourse_slab_thickness/2-tfi.concourse_haunch_depth)
            vertexes['concourse_right_haunch_top'] = (tfi.frame_outer_width-tfi.wall_slab_thickness-tfi.concourse_haunch_width,
                                                      tfi.concourse_slab_vertical_location)


    if TunnelFrame.column_bays > 1:

        spacing = TunnelFrame.frame_inner_width / TunnelFrame.column_bays
        for y in range(TunnelFrame.column_bays-1):
            col_num = y + 1
            x = round(TunnelFrame.wall_slab_thickness+col_num*spacing, 2)
            vertexes[f'central_column_{col_num}_inverse_center'] = (x, tfi.inverse_slab_thickness/2)
            vertexes[f'central_column_{col_num}_inverse_top'] = (x, tfi.inverse_slab_thickness)
            vertexes[f'central_column_{col_num}_roof_slab_bottom'] = (x, tfi.frame_outer_height-tfi.roof_slab_thickness)
            vertexes[f'central_column_{col_num}_roof_slab_center'] = (x, tfi.frame_outer_height-tfi.roof_slab_thickness/2)
            if tfi.concourse_slab_thickness:
                if tfi.column_capital_height:
                    vertexes[f'central_column_{col_num}_capital_bottom'] = (x,
                                                                    tfi.concourse_slab_vertical_location - tfi.concourse_slab_thickness / 2 - tfi.column_capital_height)
                vertexes[f'central_column_{col_num}_concourse_slab_bottom'] = (x,
                                                                tfi.concourse_slab_vertical_location - tfi.concourse_slab_thickness / 2)
                vertexes[f'central_column_{col_num}_concourse_slab_middle'] = (x, tfi.concourse_slab_vertical_location)
                vertexes[f'central_column_{col_num}_concourse_slab_top'] = (
                    x, tfi.concourse_slab_vertical_location + tfi.concourse_slab_thickness / 2)
            if tfi.column_capital_width:
                vertexes[f'central_column_{col_num}_capital_left'] = (x-tfi.column_capital_width-tfi.column_width/2, tfi.concourse_slab_vertical_location)
                vertexes[f'central_column_{col_num}_capital_right'] = (x+tfi.column_capital_width+tfi.column_width/2, tfi.concourse_slab_vertical_location)

            if tfi.column_capital_roof_slab_width:
                vertexes[f'central_column_{col_num}_capital_left_roof_slab'] = (
                x - tfi.column_capital_roof_slab_width - tfi.column_width / 2, tfi.frame_outer_height-tfi.roof_slab_thickness/2)
                vertexes[f'central_column_{col_num}_capital_right_roof_slab'] = (
                x + tfi.column_capital_roof_slab_width + tfi.column_width / 2, tfi.frame_outer_height-tfi.roof_slab_thickness/2)
                vertexes[f'central_column_{col_num}_capital_bottom_roof_slab'] = (x,
                                                                        tfi.frame_outer_height-tfi.roof_slab_thickness - tfi.column_capital_roof_slab_height)

    outer_frame_points = {
        'outer_bottom_left': (0, 0),
        'outer_top_left': (0, TunnelFrame.frame_outer_height),
        'outer_top_right': (TunnelFrame.frame_outer_width, TunnelFrame.frame_outer_height),
        'outer_bottom_right': (TunnelFrame.frame_outer_width, 0),
    }

    inner_frame_points = {
        'inner_bot_left': (TunnelFrame.wall_slab_thickness, TunnelFrame.inverse_slab_thickness),
        'inner_left_haunch_bot': (TunnelFrame.wall_slab_thickness,
                                  TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness-TunnelFrame.haunch_depth),
        'inner_left_haunch_top': (TunnelFrame.wall_slab_thickness+TunnelFrame.haunch_width,
                                  TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness),
        'inner_right_haunch_top': (TunnelFrame.frame_outer_width-TunnelFrame.wall_slab_thickness-TunnelFrame.haunch_width,
                                   TunnelFrame.frame_outer_height - TunnelFrame.roof_slab_thickness),
        'inner_right_haunch_bot': (TunnelFrame.frame_outer_width - TunnelFrame.wall_slab_thickness,
                                   TunnelFrame.frame_outer_height-TunnelFrame.roof_slab_thickness-TunnelFrame.haunch_depth),
        'inner_bot_right': (TunnelFrame.wall_slab_thickness+TunnelFrame.frame_inner_width, TunnelFrame.inverse_slab_thickness),
    }

    # Label positioned at 6% and 9% of canvas containing 12.5% padding either side of frame
    # vertex a is the top/left vertex of the label , vertex b referes to the bottom/right vertex

    label_positions = {
        'frame_height_o': {
            'orientation': 'vertical',
            'vertex_a': (Decimal('0')-TunnelFrame.frame_outer_width* Decimal('0.06'), 0),
            'vertex_b': (Decimal('0') - TunnelFrame.frame_outer_width * Decimal('0.06'), TunnelFrame.frame_outer_height),
            'value': round(TunnelFrame.frame_outer_height),
            'rotation': -90
        },
        'frame_height_i': {
            'orientation': 'vertical',
            'vertex_b': ((Decimal('0') - TunnelFrame.frame_outer_width * Decimal('0.03')),
                          TunnelFrame.frame_inner_height + TunnelFrame.inverse_slab_thickness),
            'vertex_a': (Decimal('0') - TunnelFrame.frame_outer_width * Decimal('0.03'), TunnelFrame.inverse_slab_thickness),
            'value': round(TunnelFrame.frame_inner_height),
            'rotation': -90
        },
        'frame_width_o': {
            'orientation': 'horizontal',
            'vertex_a': (0, Decimal('0') - TunnelFrame.frame_outer_height* Decimal('0.06')),
            'vertex_b': (TunnelFrame.frame_outer_width, Decimal('0')- TunnelFrame.frame_outer_height * Decimal('0.06')),
            'value': round(TunnelFrame.frame_outer_width),
            'rotation': 0
        },
        'frame_width_i': {
            'orientation': 'horizontal',
            'vertex_a': (TunnelFrame.wall_slab_thickness, Decimal('0') - TunnelFrame.frame_outer_height * Decimal(
                '0.03')),
            'vertex_b': (TunnelFrame.frame_outer_width -TunnelFrame.wall_slab_thickness,
                         Decimal('0') - TunnelFrame.frame_outer_height * Decimal(
                '0.03')),
            'value': round(TunnelFrame.frame_inner_width),
            'rotation': 0
        },
        'haunch_depth': {
            'orientation': 'vertical',
            'vertex_b': (TunnelFrame.wall_slab_thickness + TunnelFrame.haunch_width + TunnelFrame.haunch_width*Decimal(0.05),
                         TunnelFrame.inverse_slab_thickness+TunnelFrame.frame_inner_height),
            'vertex_a': (TunnelFrame.wall_slab_thickness+ TunnelFrame.haunch_width+ TunnelFrame.haunch_width*Decimal(0.05),
                         TunnelFrame.inverse_slab_thickness + TunnelFrame.frame_inner_height-TunnelFrame.haunch_depth),
            'value': round(TunnelFrame.haunch_depth),
            'rotation': 0
        },
        'haunch_width': {
            'orientation': 'horizontal',
            'vertex_a': (TunnelFrame.wall_slab_thickness,
                         TunnelFrame.inverse_slab_thickness+TunnelFrame.frame_inner_height - TunnelFrame.haunch_depth*Decimal(1.05)),
            'vertex_b': (TunnelFrame.wall_slab_thickness + TunnelFrame.haunch_width,
                         TunnelFrame.inverse_slab_thickness + TunnelFrame.frame_inner_height - TunnelFrame.haunch_depth*Decimal(1.05)),
            'value': round(TunnelFrame.haunch_width),
            'rotation': 0
        },
    }

    key_x_axis = [TunnelFrame.wall_slab_thickness / 2]
    if TunnelFrame.column_bays > 1:
        spacing = tfi.frame_inner_width/tfi.column_bays
        i = 1
        for x in range(TunnelFrame.column_bays-1):
            key_x_axis.append(round(tfi.wall_slab_thickness+spacing*i, 2))
            i += 1
    key_x_axis.append(TunnelFrame.frame_outer_width-tfi.wall_slab_thickness/2)

    key_z_axis = [tfi.inverse_slab_thickness/2]
    if tfi.concourse_slab_thickness:
        key_z_axis.append(tfi.concourse_slab_vertical_location)
    key_z_axis.append(tfi.frame_outer_height-tfi.roof_slab_thickness/2)

    context = {
        'label_positions': label_positions,
        'vertexes': vertexes,
        'outer_frame_points': outer_frame_points,
        'inner_frame_points': inner_frame_points,
        'key_x_axis': key_x_axis,
        'key_z_axis': key_z_axis,
    }

    return context


def get_grid_lines(tfi):
    """Defines model Grid Lines for a Tunnel Frame instance (tfi)
    Grid Lines are present on the X and Z axis wherever a vertex is present"""

    # Definition of X-axis grid lines
    # CoordSys=GLOBAL AxisDir=X GridID="" XRYZCoord="" LineType=Primary LineColor=Gray8Dark Visible=Yes BubbleLoc=End
    # GRID-ID must be auto-incremented alphabetically
    # XRYZCoord is the value of the grid line along the axis

    grid_locations_x = []
    grid_locations_x.append(0)
    grid_locations_x.append(tfi.wall_slab_thickness/2)
    grid_locations_x.append(tfi.wall_slab_thickness)
    grid_locations_x.append(tfi.wall_slab_thickness+tfi.haunch_width)

    # If there are multiple bays, we will create grid lines along the columns

    if tfi.column_bays > 1:
        num_columns = tfi.column_bays - 1
        spacing = tfi.frame_outer_width/tfi.column_bays
        col_index = 1
        for column in range(num_columns):
            if tfi.column_capital_width:
                grid_locations_x.append(spacing*col_index - tfi.column_capital_width)
                grid_locations_x.append(spacing*col_index)
                grid_locations_x.append(spacing*col_index + tfi.column_capital_width)
                if tfi.column_capital_roof_slab_width:
                    if (spacing*col_index - tfi.column_capital_roof_slab_width) not in grid_locations_x:
                        grid_locations_x.append(spacing*col_index - tfi.column_capital_roof_slab_width)
                        grid_locations_x.append(spacing * col_index + tfi.column_capital_roof_slab_width)
            else:
                grid_locations_x.append(spacing*col_index)
            col_index +=1
        grid_locations_x.append(tfi.frame_outer_width - tfi.wall_slab_thickness - tfi.haunch_width)
        grid_locations_x.append(tfi.frame_outer_width - tfi.wall_slab_thickness / 2)
        grid_locations_x.append(tfi.frame_outer_width)
    else:
        grid_locations_x.append(tfi.frame_outer_width-tfi.wall_slab_thickness-tfi.haunch_width)
        grid_locations_x.append(tfi.frame_outer_width - tfi.wall_slab_thickness)
        grid_locations_x.append(tfi.frame_outer_width-tfi.wall_slab_thickness/2)
        grid_locations_x.append(tfi.frame_outer_width)

    # Grid locations on Z-Axis
    grid_locations_z = []
    grid_locations_z.append(0)
    grid_locations_z.append(tfi.inverse_slab_thickness/2)
    grid_locations_z.append(tfi.inverse_slab_thickness)

    if tfi.concourse_slab_thickness:
        if tfi.concourse_haunch_depth:
            grid_locations_z.append(tfi.concourse_slab_vertical_location-tfi.concourse_slab_thickness/2-tfi.concourse_haunch_depth)
            grid_locations_z.append(tfi.concourse_slab_vertical_location - tfi.concourse_slab_thickness/2)
            grid_locations_z.append(tfi.concourse_slab_vertical_location)
            grid_locations_z.append(tfi.concourse_slab_vertical_location + tfi.concourse_slab_thickness / 2)
            grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness-tfi.haunch_depth)
            grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness)
            grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness/2)
            grid_locations_z.append(tfi.frame_outer_height)
        else:
            grid_locations_z.append(tfi.concourse_slab_vertical_location - tfi.concourse_slab_thickness / 2)
            grid_locations_z.append(tfi.concourse_slab_vertical_location)
            grid_locations_z.append(tfi.concourse_slab_vertical_location + tfi.concourse_slab_thickness / 2)
            grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness - tfi.haunch_depth)
            grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness)
            grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness / 2)
            grid_locations_z.append(tfi.frame_outer_height)
    else:
        grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness - tfi.haunch_depth)
        grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness)
        grid_locations_z.append(tfi.frame_outer_height - tfi.roof_slab_thickness / 2)
        grid_locations_z.append(tfi.frame_outer_height)

    grid_locations_x = [float(x) for x in grid_locations_x]
    grid_locations_z = [float(x) for x in grid_locations_z]

    return grid_locations_x, grid_locations_z


    # tunnel frame instance
    # point a and point b to get member name

def get_member_name(a, b, tfi):
    member_name = ""
    if a[0] == b[0]:
        # member is on the vertical axis.
        # vertical value yields naming convention based on location
        if b[0] <= tfi.wall_slab_thickness:
            if a[1] > tfi.frame_outer_height-tfi.roof_slab_thickness:
                member_name=f"WS{math.floor(tfi.wall_slab_thickness+tfi.haunch_width/2)}_S"
            elif a[1] == tfi.frame_outer_height-tfi.roof_slab_thickness and b[1] == tfi.frame_outer_height-tfi.roof_slab_thickness-tfi.haunch_depth:
                member_name=f"WS{math.floor(tfi.wall_slab_thickness+tfi.haunch_width/2)}"
            elif b[1] < tfi.inverse_slab_thickness:
                member_name = f"WS{math.floor(tfi.wall_slab_thickness)}_S"
            else:
                if tfi.concourse_slab_thickness:
                    if tfi.concourse_slab_vertical_location-tfi.concourse_slab_thickness/2 < a[1] <= tfi.concourse_slab_vertical_location+tfi.concourse_slab_thickness/2:
                        member_name = f"WS{math.floor(tfi.wall_slab_thickness+tfi.concourse_haunch_width/2)}_S"
                    elif tfi.concourse_haunch_depth:
                        if a[1]==tfi.concourse_slab_vertical_location-tfi.concourse_slab_thickness/2 and b[1]==tfi.concourse_slab_vertical_location-tfi.concourse_slab_thickness/2-tfi.concourse_haunch_depth:
                            member_name = f"WS{math.floor(tfi.wall_slab_thickness+tfi.concourse_haunch_width/2)}"
                        else:
                            member_name = f"WS{math.floor(tfi.wall_slab_thickness)}"
                    else:
                        member_name = f"WS{math.floor(tfi.wall_slab_thickness)}"
                else:
                    member_name = f"WS{math.floor(tfi.wall_slab_thickness)}"

        elif b[0] < tfi.frame_outer_width-tfi.wall_slab_thickness:
            #
            if b[1] <= tfi.inverse_slab_thickness:
                member_name = f"COL{math.floor(tfi.column_width)}_S"
            elif b[1] <= tfi.frame_outer_height-tfi.roof_slab_thickness:
                member_name = f"COL{math.floor(tfi.column_width)}"
            else:
                member_name = f"COL{math.floor(tfi.column_width)}_S"

        elif b[0] > tfi.frame_outer_width-tfi.wall_slab_thickness:
            if a[1] > tfi.frame_outer_height - tfi.roof_slab_thickness:
                member_name = f"WS{math.floor(tfi.wall_slab_thickness + tfi.haunch_width / 2)}_S"
            elif a[1] == tfi.frame_outer_height - tfi.roof_slab_thickness and b[
                1] == tfi.frame_outer_height - tfi.roof_slab_thickness - tfi.haunch_depth:
                member_name = f"WS{math.floor(tfi.wall_slab_thickness + tfi.haunch_width / 2)}"
            elif b[1] < tfi.inverse_slab_thickness:
                member_name = f"WS{math.floor(tfi.wall_slab_thickness)}_S"
            else:
                if tfi.concourse_slab_thickness:
                    if tfi.concourse_slab_vertical_location - tfi.concourse_slab_thickness / 2 < a[
                        1] <= tfi.concourse_slab_vertical_location + tfi.concourse_slab_thickness / 2:
                        member_name = f"WS{math.floor(tfi.wall_slab_thickness + tfi.concourse_haunch_width / 2)}_S"
                    elif tfi.concourse_haunch_depth:
                        if a[1] == tfi.concourse_slab_vertical_location - tfi.concourse_slab_thickness / 2 and b[
                            1] == tfi.concourse_slab_vertical_location - tfi.concourse_slab_thickness / 2 - tfi.concourse_haunch_depth:
                            member_name = f"WS{math.floor(tfi.wall_slab_thickness + tfi.concourse_haunch_width / 2)}"
                        else:
                            member_name = f"WS{math.floor(tfi.wall_slab_thickness)}"
                    else:
                        member_name = f"WS{math.floor(tfi.wall_slab_thickness)}"
                else:
                    member_name = f"WS{math.floor(tfi.wall_slab_thickness)}"
    elif a[1] == b[1]:
        # member is on the x axis
        if b[1] <= tfi.inverse_slab_thickness:
            if b[0] <= tfi.wall_slab_thickness or a[0] >= (tfi.frame_outer_width-tfi.wall_slab_thickness):
                member_name = f"IS{math.floor(tfi.inverse_slab_thickness)}_S"
            else:
                member_name = f"IS{math.floor(tfi.inverse_slab_thickness)}"

        elif b[1] == tfi.concourse_slab_vertical_location:
            if b[0] <= tfi.wall_slab_thickness or a[0] >= (tfi.frame_outer_width - tfi.wall_slab_thickness):
                if tfi.concourse_haunch_depth:
                    member_name = f"CS{math.floor(tfi.concourse_slab_thickness+tfi.concourse_haunch_depth/2)}_S"
                else:
                    member_name = f"CS{math.floor(tfi.concourse_slab_thickness)}_S"
            else:
                if tfi.concourse_haunch_depth:
                    if b[0]==tfi.wall_slab_thickness+tfi.concourse_haunch_width or a[0]==tfi.frame_outer_width-tfi.wall_slab_thickness-tfi.concourse_haunch_width:
                        member_name = f"CS{math.floor(tfi.concourse_slab_thickness+tfi.concourse_haunch_depth/2)}"
                    else:
                        member_name = f"CS{math.floor(tfi.concourse_slab_thickness)}"
                else:
                    member_name = f"CS{math.floor(tfi.concourse_slab_thickness)}"

        elif b[1] > tfi.frame_outer_height-tfi.roof_slab_thickness:
            if b[0] <= tfi.wall_slab_thickness:
                if tfi.haunch_depth:
                    member_name = f"RS{math.floor(tfi.roof_slab_thickness+tfi.haunch_depth/2)}_S"
                else:
                    member_name = f"RS{math.floor(tfi.roof_slab_thickness)}_S"
            elif b[0]>tfi.frame_outer_width-tfi.wall_slab_thickness:
                if tfi.haunch_depth:
                    member_name = f"RS{math.floor(tfi.roof_slab_thickness + tfi.haunch_depth / 2)}_S"
                else:
                    member_name = f"RS{math.floor(tfi.roof_slab_thickness)}_S"
            else:
                if tfi.haunch_width:
                    if b[0] == tfi.wall_slab_thickness + tfi.haunch_width or a[0] == tfi.frame_outer_width - tfi.wall_slab_thickness - tfi.haunch_width:
                        member_name = f"RS{math.floor(tfi.roof_slab_thickness+ tfi.haunch_depth / 2)}"
                    else:
                        member_name = f"RS{math.floor(tfi.roof_slab_thickness)}"
                else:
                    member_name = f"RS{math.floor(tfi.roof_slab_thickness)}"

    return member_name
