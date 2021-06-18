from decimal import *
from openpyxl import Workbook
import cairo
import math
from django.conf.urls.static import static
from django.conf import settings
import os
from django.http import HttpResponse


def get_geometry(TunnelFrame):
    """Return the vertex co-ordinates of the TunnelFrame Object
    0-0 is by default designated at the bottom left co-ordinate
    left, right, center, top, bottom refer to reference location of vertexes around a
    central vertex (meeting of members).
    """

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

        'left_haunch_bottom': left_haunch_bottom,
        'left_haunch_top': left_haunch_top,
        'right_haunch_bottom': right_haunch_bottom,
        'right_hauch_top': right_hauch_top,
    }

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
            'value': TunnelFrame.frame_outer_height,
            'rotation': -90
        },
        'frame_height_i': {
            'orientation': 'vertical',
            'vertex_b': (Decimal('0') - TunnelFrame.frame_outer_width * Decimal('0.03'),
                          TunnelFrame.frame_inner_height + TunnelFrame.inverse_slab_thickness),
            'vertex_a': (Decimal('0') - TunnelFrame.frame_outer_width * Decimal('0.03'), TunnelFrame.inverse_slab_thickness),
            'value': TunnelFrame.frame_inner_height,
            'rotation': -90
        },
        'frame_width_o': {
            'orientation': 'horizontal',
            'vertex_a': (0, Decimal('0') - TunnelFrame.frame_outer_height* Decimal('0.06')),
            'vertex_b': (TunnelFrame.frame_outer_width, Decimal('0')- TunnelFrame.frame_outer_height * Decimal('0.06')),
            'value': TunnelFrame.frame_outer_width,
            'rotation': 0
        },
        'frame_width_i': {
            'orientation': 'horizontal',
            'vertex_a': (TunnelFrame.wall_slab_thickness, Decimal('0') - TunnelFrame.frame_outer_height * Decimal(
                '0.03')),
            'vertex_b': (TunnelFrame.frame_outer_width -TunnelFrame.wall_slab_thickness,
                         Decimal('0') - TunnelFrame.frame_outer_height * Decimal(
                '0.03')),
            'value': TunnelFrame.frame_inner_width,
            'rotation': 0
        },
        'haunch_depth': {
            'orientation': 'vertical',
            'vertex_b': (TunnelFrame.wall_slab_thickness + TunnelFrame.haunch_width + TunnelFrame.haunch_width*Decimal(0.05),
                         TunnelFrame.inverse_slab_thickness+TunnelFrame.frame_inner_height),
            'vertex_a': (TunnelFrame.wall_slab_thickness+ TunnelFrame.haunch_width+ TunnelFrame.haunch_width*Decimal(0.05),
                         TunnelFrame.inverse_slab_thickness + TunnelFrame.frame_inner_height-TunnelFrame.haunch_depth),
            'value': TunnelFrame.haunch_depth,
            'rotation': 0
        },
        'haunch_width': {
            'orientation': 'horizontal',
            'vertex_a': (TunnelFrame.wall_slab_thickness,
                         TunnelFrame.inverse_slab_thickness+TunnelFrame.frame_inner_height - TunnelFrame.haunch_depth*Decimal(1.05)),
            'vertex_b': (TunnelFrame.wall_slab_thickness + TunnelFrame.haunch_width,
                         TunnelFrame.inverse_slab_thickness + TunnelFrame.frame_inner_height - TunnelFrame.haunch_depth*Decimal(1.05)),
            'value': TunnelFrame.haunch_width,
            'rotation': 0
        },
    }

    context = {
        'label_positions': label_positions,
        'vertexes': vertexes,
        'outer_frame_points': outer_frame_points,
        'inner_frame_points': inner_frame_points,
    }
    return context


def get_members():
    pass


def cairo_draw_frame(tunnel_frame):
    """Renders cairo drawing of frame"""

    WIDTH, HEIGHT = float(tunnel_frame.frame_outer_width)*1.25, float(tunnel_frame.frame_outer_height)*1.25
    HOR_PAD, VERT_PAD = WIDTH-float(tunnel_frame.frame_outer_width)*1.125, HEIGHT - float(
        tunnel_frame.frame_outer_height) * 1.125
    if WIDTH>HEIGHT:
        PIXEL_SCALE = 1000/WIDTH
    else:
        PIXEL_SCALE = 1000/HEIGHT

    context = get_geometry(tunnel_frame)

    with cairo.SVGSurface("example.svg", WIDTH*PIXEL_SCALE, HEIGHT*PIXEL_SCALE) as surface:

        ctx = cairo.Context(surface)

        ctx.scale(PIXEL_SCALE, PIXEL_SCALE)
        pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
        pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
        pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity
        ctx.rectangle(0, 0, WIDTH, HEIGHT)
        ctx.set_source(pat)
        ctx.fill()
        # Process the vertex locations into cairo co-ordinates
        # Y scale must be reversed due to cairo co-ordinates (0,0 top left of drawing)
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(0.06)

        for values in context['vertexes'].values():
            x = float(values[0])+HOR_PAD
            y = HEIGHT-float(values[1])-VERT_PAD
            ctx.arc(x, y, 0.005*WIDTH, 0, 2*math.pi)
            ctx.fill()
        i = 1
        for values in context['outer_frame_points'].values():
            length = len(context['outer_frame_points'])
            x = float(values[0]) + HOR_PAD
            y = HEIGHT - float(values[1]) - VERT_PAD
            # print(x,y)
            if i == 1:
                ctx.move_to(x, y)
            elif i == length:
                ctx.line_to(x, y)
                ctx.close_path()
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(0.002 * WIDTH)
                ctx.stroke()
            else:
                ctx.line_to(x, y)
            i += 1
        i = 1
        for values in context['inner_frame_points'].values():
            length = len(context['inner_frame_points'])
            x = float(values[0]) + HOR_PAD
            y = HEIGHT - float(values[1]) - VERT_PAD
            if i == 1:
                ctx.move_to(x, y)
            elif i == length:
                ctx.line_to(x, y)
                ctx.close_path()
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(0.002 * WIDTH)
                ctx.stroke()
            else:
                ctx.line_to(x, y)
            i += 1

        # Routine for drawing dimension labels
        ctx.set_source_rgb(0, 0, 0.5)

        for key, dimension_instructions in context['label_positions'].items():
            arrow_length = float(dimension_instructions['value']/60)
            if key == 'haunch_depth' or key == 'haunch_width':
                arrow_length = float(dimension_instructions['value'] / 5)
                if key == 'haunch_depth':
                    offset = 'right'
                else:
                    offset = 'down'
            else:
                offset = None
            breakpoint_length = float(dimension_instructions['value']/2- dimension_instructions['value']*Decimal(0.10))
            # routine for top / left arrows
            xa, ya = dimension_instructions['vertex_a']
            xb, yb = dimension_instructions['vertex_b']
            xa = float(xa) + HOR_PAD
            ya = HEIGHT - float(ya) - VERT_PAD
            xb = float(xb) + HOR_PAD
            yb = HEIGHT - float(yb) - VERT_PAD

            ctx.set_font_size(tunnel_frame.frame_outer_width*Decimal(0.035))

            if dimension_instructions['orientation'] == 'vertical':
                ctx.move_to(xa, ya)
                ctx.line_to(xa - arrow_length,
                            ya - arrow_length)
                ctx.line_to(xa + arrow_length,
                            ya - arrow_length)
                ctx.close_path()
                ctx.fill()
                ctx.move_to(xa,ya)
                ctx.line_to(xa,
                            ya - breakpoint_length)
                ctx.stroke()

                ctx.move_to(xb, yb)
                ctx.line_to(xb - arrow_length,
                            yb + arrow_length)
                ctx.line_to(xb + arrow_length,
                            yb + arrow_length)
                ctx.close_path()
                ctx.fill()
                ctx.move_to(xb, yb)
                ctx.line_to(xb, yb + breakpoint_length)
                ctx.stroke()

                write_text(ctx, (xa+xb)/2, (ya+yb)/2, dimension_instructions['rotation'],
                           str(dimension_instructions['value']), offset)

            if dimension_instructions['orientation'] == 'horizontal':
                ctx.move_to(xa, ya)
                ctx.line_to(xa + arrow_length,
                            ya - arrow_length)
                ctx.line_to(xa + arrow_length,
                            ya + arrow_length)
                ctx.close_path()
                ctx.fill()
                ctx.move_to(xa, ya)
                ctx.line_to(xa + breakpoint_length,
                            ya)
                ctx.stroke()

                ctx.move_to(xb, yb)
                ctx.line_to(xb - arrow_length,
                            yb - arrow_length)
                ctx.line_to(xb - arrow_length,
                            yb + arrow_length)
                ctx.close_path()
                ctx.fill()
                ctx.move_to(xb, yb)
                ctx.line_to(xb - breakpoint_length,
                            yb)
                ctx.stroke()
                write_text(ctx, (xa + xb) / 2, (ya + yb) / 2, dimension_instructions['rotation'],
                           str(dimension_instructions['value']), offset)

        surface.write_to_png("static/images/example.png")


def arrow(ctx, x, y, width, height, a, b, rotate=None):
    """Produces right facing arrowhead =>"""
    ctx.move_to(x, y + b)
    ctx.line_to(x, y + height - b)
    ctx.line_to(x + a, y + height - b)
    ctx.line_to(x + a, y + height)
    ctx.line_to(x + width, y + height / 2)
    ctx.line_to(x + a, y)
    ctx.line_to(x + a, y + b)
    ctx.close_path()


def write_text(ctx, x, y, rotation, text, offset=None):
    """Routine for writing text labels for pycairo Rectangular TunnelFrames"""
    ctx.save()
    ctx.set_source_rgb(0, 0, 0)
    ctx.select_font_face("Arial",
                         cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    xbearing, ybearing, width, height, dx, dy = ctx.text_extents(text)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    if offset == "down":
        y = y*1.10
    if offset == 'right':
        x = x*1.10
    if rotation != 0:
        nx = -width/2.0
        ny = fheight/2
        ctx.translate(x, y)
        ctx.rotate(rotation*math.pi/180)
        ctx.translate(nx, ny)
        ctx.move_to(0,0)
        ctx.show_text(text)
        ctx.restore()
    else:
        x = x - width/2
        ctx.move_to(x, y)
        ctx.show_text(text)
        ctx.restore()


def create_workbook(tunnel_frame, dimension_system=None, auth=False):
    """Create excel workbook of relevant data for import into SAP2000"""
    wb = Workbook()

    # Table definition for SAP2000 Compatibility and system variables ie. Dimension system (mm, m, in)
    dest_filename = f"{tunnel_frame.frame_description}.xlsx"

    ws1 = wb.active
    ws1.title = "Coordinate Systems"
    ws1['A1'] = "TABLE:  Coordinate Systems"
    co_ordinate_headings = [
        ["Name", "Type", "X", "Y", "Z", "AboutZ", "AboutY", "AboutX"],
        ["Text", "Text", "mm", "mm", "mm", "Degrees", "Degrees", "Degrees"]
    ]
    for row in co_ordinate_headings:
        ws1.append(row)

    # Worksheet 2
    # Worksheet for vertex positions

    ws2 = wb.create_sheet(title="Joint Coordinates")
    ws2['A1'] = "TABLE:  Joint Coordinates"
    joint_coord_headings = [
        ["Joint", "CoordSys", "CoordType", "XorR", "Y", "Z", "SpecialJT", "GlobalX", "GlobalY", "GlobalZ", "GUID"],
        ["Text", "Text", "Text", "mm", "mm", "mm", "Yes/No", "mm", "mm", "mm", "Text"]
    ]
    for row in joint_coord_headings:
        ws2.append(row)

    vertexes = get_geometry(tunnel_frame)['vertexes']
    point_increment = 1
    for vertex in vertexes.values():
        ws2.append(
            [point_increment, "GLOBAL", "Cartesian", vertex[0], vertex[1], 0, "No", vertex[0], vertex[1], "0"]
        )
        point_increment += 1

    if auth is False:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename={dest_filename}'
        wb.save(response)
        return response

    target = os.path.join(settings.STATIC_DIR, "XLXS")
    wb.save(target+f"/{dest_filename}")
    wb_location = os.path.join(target, dest_filename)
    return wb_location
