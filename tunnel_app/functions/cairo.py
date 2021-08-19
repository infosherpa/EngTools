import cairo
import math
from .geometry import get_geometry
from decimal import *


def cairo_draw_frame(tunnel_frame, custom_column_spacing=None):
    """Renders cairo drawing of frame"""

    WIDTH, HEIGHT = float(tunnel_frame.frame_outer_width)*1.25, float(tunnel_frame.frame_outer_height)*1.25
    HOR_PAD, VERT_PAD = WIDTH-float(tunnel_frame.frame_outer_width)*1.125, HEIGHT - float(
        tunnel_frame.frame_outer_height) * 1.125
    if WIDTH>HEIGHT:
        PIXEL_SCALE = 2000/WIDTH
    else:
        PIXEL_SCALE = 2000/HEIGHT

    context = get_geometry(tunnel_frame)

    with cairo.SVGSurface("static/images/example.svg", WIDTH*PIXEL_SCALE, HEIGHT*PIXEL_SCALE) as surface:

        ctx = cairo.Context(surface)

        ctx.scale(PIXEL_SCALE, PIXEL_SCALE)
        # pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
        # pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
        # pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity

        ctx.rectangle(0, 0, WIDTH, HEIGHT)
        # ctx.set_source(pat)

        ctx.set_source_rgb(255,255,255)
        ctx.fill()
        # Process the vertex locations into cairo co-ordinates
        # Y scale must be reversed due to cairo co-ordinates (0,0 top left of drawing)
        ctx.set_source_rgb(0, 0.596, 0.459)
        ctx.set_line_width(0.06)

        matrix = cairo.Matrix(x0=HOR_PAD, yy=-1, y0=HEIGHT-VERT_PAD)
        ctx.transform(matrix)
        ctx.set_font_size(tunnel_frame.frame_outer_width * Decimal(0.035))

        # Draw Joint Positions
        for key, values in tunnel_frame.joint_coordinates.items():
            # x = float(values[0])+HOR_PAD
            # y = HEIGHT-float(values[1])-VERT_PAD
            x = float(values[0])
            y = float(values[1])

            ctx.arc(x, y, 0.005*WIDTH, 0, 2*math.pi)
            ctx.fill()
            write_text(ctx, x+0.01*WIDTH, y-0.01*WIDTH, 0, str(key), matrix, HOR_PAD)

        # Draw members
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.002 * WIDTH)
        for memb_key, member in tunnel_frame.connectivity_frame.items():
            for point_key, point in tunnel_frame.joint_coordinates.items():
                if member[0] == point_key:
                    start_pos = (point[0], point[1])
                if member[1] == point_key:
                    end_pos = (point[0], point[1])
            # print(start_pos)
            # print(end_pos)
            ctx.move_to(float(start_pos[0]), float(start_pos[1]))
            ctx.line_to(float(end_pos[0]), float(end_pos[1]))
            ctx.stroke()

        i = 1
        for values in context['outer_frame_points'].values():
            length = len(context['outer_frame_points'])
            # x = float(values[0]) + HOR_PAD
            # y = HEIGHT - float(values[1]) - VERT_PAD
            # print(x,y)
            x = float(values[0])
            y = float(values[1])

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
            # x = float(values[0]) + HOR_PAD
            # y = HEIGHT - float(values[1]) - VERT_PAD
            x = float(values[0])
            y = float(values[1])

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

        if tunnel_frame.concourse_slab_thickness:
            x = tunnel_frame.wall_slab_thickness
            x2 = tunnel_frame.frame_outer_width - tunnel_frame.wall_slab_thickness
            y = tunnel_frame.concourse_slab_vertical_location-tunnel_frame.concourse_slab_thickness/2
            y2 = tunnel_frame.concourse_slab_vertical_location+tunnel_frame.concourse_slab_thickness/2

            # Draw the bottom of concourse slab

            if tunnel_frame.concourse_haunch_depth>0:
                haunch_y = y - tunnel_frame.concourse_haunch_depth
                haunch_x = x + tunnel_frame.concourse_haunch_width
                haunch_x2 = x2-tunnel_frame.concourse_haunch_width

                ctx.move_to(x, haunch_y)
                ctx.line_to(haunch_x, y)
                ctx.line_to(haunch_x2, y)
                ctx.line_to(x2, haunch_y)
                ctx.stroke()

            else:
                ctx.move_to(x, y)
                ctx.line_to(x2, y)
                ctx.stroke()

            # Draw the top of concourse slab
            ctx.move_to(x, y2)
            ctx.line_to(x2, y2)
            ctx.stroke()

        if tunnel_frame.column_bays > 1:
            tunnel_width = tunnel_frame.column_width
            spacing = tunnel_frame.frame_inner_width / (tunnel_frame.column_bays)
            i = 1

            if tunnel_frame.concourse_slab_thickness:

                while i < tunnel_frame.column_bays:

                    left_wall = tunnel_frame.wall_slab_thickness + i*spacing-tunnel_frame.column_width/2
                    right_wall = tunnel_frame.wall_slab_thickness + i*spacing+tunnel_frame.column_width/2

                    ctx.move_to(left_wall, tunnel_frame.inverse_slab_thickness)
                    ctx.line_to(left_wall, tunnel_frame.concourse_slab_vertical_location-tunnel_frame.concourse_slab_thickness/2)
                    ctx.stroke()
                    ctx.move_to(left_wall, tunnel_frame.concourse_slab_vertical_location+tunnel_frame.concourse_slab_thickness/2)
                    ctx.line_to(left_wall,
                                tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness)
                    ctx.stroke()

                    if tunnel_frame.column_capital_height:
                        ctx.move_to(left_wall, tunnel_frame.concourse_slab_vertical_location-tunnel_frame.concourse_slab_thickness/2-tunnel_frame.column_capital_height)
                        ctx.line_to(left_wall-tunnel_frame.column_capital_width,tunnel_frame.concourse_slab_vertical_location-tunnel_frame.concourse_slab_thickness/2)
                        ctx.stroke()

                        ctx.move_to(right_wall,
                                    tunnel_frame.concourse_slab_vertical_location - tunnel_frame.concourse_slab_thickness / 2 - tunnel_frame.column_capital_height)
                        ctx.line_to(right_wall + tunnel_frame.column_capital_width,
                                    tunnel_frame.concourse_slab_vertical_location - tunnel_frame.concourse_slab_thickness / 2)
                        ctx.stroke()

                    if tunnel_frame.column_capital_roof_slab_height:
                        ctx.move_to(left_wall, tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness-tunnel_frame.column_capital_roof_slab_height)
                        ctx.line_to(left_wall-tunnel_frame.column_capital_roof_slab_width,tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness)
                        ctx.stroke()

                        ctx.move_to(right_wall,
                                    tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness-tunnel_frame.column_capital_roof_slab_height)
                        ctx.line_to(right_wall + tunnel_frame.column_capital_roof_slab_width,
                                    tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness)
                        ctx.stroke()


                    ctx.move_to(right_wall, tunnel_frame.inverse_slab_thickness)
                    ctx.line_to(right_wall,
                                tunnel_frame.concourse_slab_vertical_location - tunnel_frame.concourse_slab_thickness / 2)
                    ctx.stroke()
                    ctx.move_to(right_wall,
                                tunnel_frame.concourse_slab_vertical_location + tunnel_frame.concourse_slab_thickness / 2)
                    ctx.line_to(right_wall,
                                tunnel_frame.frame_outer_height - tunnel_frame.roof_slab_thickness)
                    ctx.stroke()
                    i = i+1
            else:

                while i < tunnel_frame.column_bays:
                    left_wall = tunnel_frame.wall_slab_thickness + (i * spacing - tunnel_frame.column_width / 2)
                    right_wall = tunnel_frame.wall_slab_thickness + (i * spacing + tunnel_frame.column_width / 2)
                    ctx.move_to(left_wall, tunnel_frame.inverse_slab_thickness)
                    ctx.line_to(left_wall,
                                tunnel_frame.frame_outer_height - tunnel_frame.roof_slab_thickness)
                    ctx.stroke()
                    ctx.move_to(right_wall, tunnel_frame.inverse_slab_thickness)
                    ctx.line_to(right_wall,
                                tunnel_frame.frame_outer_height - tunnel_frame.roof_slab_thickness)
                    ctx.stroke()
                    i += 1

                    if tunnel_frame.column_capital_roof_slab_height:
                        ctx.move_to(left_wall, tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness-tunnel_frame.column_capital_roof_slab_height)
                        ctx.line_to(left_wall-tunnel_frame.column_capital_roof_slab_width,tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness)
                        ctx.stroke()

                        ctx.move_to(right_wall,
                                    tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness-tunnel_frame.column_capital_roof_slab_height)
                        ctx.line_to(right_wall + tunnel_frame.column_capital_roof_slab_width,
                                    tunnel_frame.frame_outer_height-tunnel_frame.roof_slab_thickness)
                        ctx.stroke()


        # Routine for drawing dimension labels
        ctx.set_source_rgb(0, 0, 0)
        arrow_length = float(context['label_positions']['frame_height_o']['value']/75)
        for key, dimension_instructions in context['label_positions'].items():
            # arrow_length = float(dimension_instructions['value']/60)
            if key == 'haunch_depth' or key == 'haunch_width':
                # arrow_length = float(dimension_instructions['value'] / 5)
                if key == 'haunch_depth':
                    offset = 'right'
                else:
                    offset = 'down'
            else:
                offset = None
            breakpoint_length = float(dimension_instructions['value']/2- dimension_instructions['value']*(0.10))
            # routine for top / left arrows
            xa, ya = dimension_instructions['vertex_a']
            xb, yb = dimension_instructions['vertex_b']
            # xa = float(xa) + HOR_PAD
            # ya = HEIGHT - float(ya) - VERT_PAD
            # xb = float(xb) + HOR_PAD
            # yb = HEIGHT - float(yb) - VERT_PAD
            xa, ya = float(xa), float(ya)
            xb, yb = float(xb), float(yb)

            if dimension_instructions['orientation'] == 'vertical':
                ctx.move_to(xa, ya)
                ctx.line_to(xa - arrow_length,
                            ya + arrow_length)
                ctx.line_to(xa + arrow_length,
                            ya + arrow_length)
                ctx.close_path()
                ctx.fill()
                ctx.move_to(xa, ya)
                ctx.line_to(xa,
                            ya + breakpoint_length)
                ctx.stroke()

                ctx.move_to(xb, yb)
                ctx.line_to(xb - arrow_length,
                            yb - arrow_length)
                ctx.line_to(xb + arrow_length,
                            yb - arrow_length)
                ctx.close_path()
                ctx.fill()
                ctx.move_to(xb, yb)
                ctx.line_to(xb, yb - breakpoint_length)
                ctx.stroke()

                write_text(ctx, (xa+xb)/2, (ya+yb)/2, dimension_instructions['rotation'],
                           str(round(dimension_instructions['value'])), matrix, HOR_PAD, offset)

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
                           str(round(dimension_instructions['value'])), matrix, HOR_PAD, offset)

        surface.write_to_png(f"static/images/frames/{tunnel_frame.hash}.png")


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


def write_text(ctx, x, y, rotation, text, matrix, HOR_PAD, offset=None):
    """Routine for writing text labels for pycairo Rectangular TunnelFrames"""
    ctx.save()
    ctx.set_source_rgb(0, 0, 0)
    ctx.select_font_face("Arial",
                         cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    xbearing, ybearing, width, height, dx, dy = ctx.text_extents(text)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    if offset == "down":
        y = y*0.95
        x = x*1.02
    if offset == 'right':
        x = x*1.18
        y = y*0.98
    if rotation != 0:
        nx = -width/2.0
        ny = fheight/2
        ctx.translate(x, y)
        ctx.rotate(rotation*math.pi/180)
        ctx.translate(nx, -ny)
        ctx.move_to(0,0)
        matrix = cairo.Matrix(yy=-1, y0=0)
        ctx.transform(matrix)
        ctx.show_text(text)
        ctx.restore()
    else:
        x = x - width/2
        ctx.move_to(x, y)
        matrix = cairo.Matrix(yy=-1, y0=0)
        ctx.transform(matrix)
        ctx.show_text(text)
        ctx.restore()