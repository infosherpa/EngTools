from unicodedata import decimal
from django.shortcuts import render, reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core import validators
import cairo

def index(request):
    return render(request, 'base.html')


def tunnel_home(request):
    return render(request, 'home.html')


def tunnel_frame_input_form(request):
    """Frame measurements"""
    if request.method == 'POST':
        inner_frame_h = float(request.POST['IFH'])
        outer_frame_h = float(request.POST['OFH'])
        inner_frame_w = float(request.POST['IFW'])
        outer_frame_w = float(request.POST['OFW'])
        haunch_depth = float(request.POST['HAD'])
        haunch_height = float(request.POST['HAW'])
        side_thickness = outer_frame_w - inner_frame_w
        top_thickness = outer_frame_h - inner_frame_h


    dimensions = {
        'inner_frame_h': inner_frame_h,
        'outer_frame_h': outer_frame_h,
        'inner_frame_w': inner_frame_w,
        'haunch_depth': haunch_depth,
        'haunch_height': haunch_height,
        'side_thickness': side_thickness,
        'top_thickness': top_thickness,
    }

    image = None

    WIDTH, HEIGHT = 3, 3
    PIXEL_SCALE = 100
    with cairo.SVGSurface("example.svg", WIDTH*PIXEL_SCALE, HEIGHT*PIXEL_SCALE) as surface:

        ctx = cairo.Context(surface)

        ctx.scale(PIXEL_SCALE, PIXEL_SCALE)
        pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
        pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
        pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity
        ctx.rectangle(0, 0, WIDTH, HEIGHT)
        ctx.set_source(pat)
        ctx.fill()

        ctx.move_to(1, 1)
        ctx.line_to(2.5, 1.5)

        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(0.06)
        ctx.stroke()

        surface.write_to_png("static/images/example.png")


    context = {
        'geometry': dimensions,
        'image': "static/images/example.png",
    }
    return render(request, 'home.html', context)
    # return HttpResponseRedirect(reverse('tunnel_app:tunnel_home', args=context))
