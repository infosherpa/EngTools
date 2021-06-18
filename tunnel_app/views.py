from unicodedata import decimal
from django.shortcuts import render, reverse, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core import validators
from django.core.exceptions import ValidationError
import cairo
from .forms import TunnelInputForm
from .models import TunnelFrame
from django.views.generic.list import ListView
from .functions import get_geometry, cairo_draw_frame, create_workbook
import mimetypes
import os
from django.conf import settings


def index(request):
    """The Base index page for the entire site"""
    return render(request, 'base.html')


def tunnel_app_home(request):
    """Homepage for 2D Tunnel App & Tunnel Frame Information Form"""

    if request.method == "POST":
        form = TunnelInputForm(request.POST)
        if form.is_valid():
            
            tunnelframe = form.save(commit=False)
            tunnelframe.wall_slab_thickness = (form.cleaned_data['frame_outer_width'] -
                                               form.cleaned_data['frame_inner_width'])/2
            tunnelframe.inverse_slab_thickness = (
                    form.cleaned_data['frame_outer_height']-form.cleaned_data['frame_inner_height']
                    - form.cleaned_data['roof_slab_thickness']
            )
            if '_generate' in request.POST:
                cairo_draw_frame(tunnelframe)
                context = {
                    'form': form,
                    'image': "static/images/example.png",
                }
                return render(request, 'tunnel_app/tun_home.html', context)

            if '_excel' in request.POST:
                return create_workbook(tunnelframe)
            else:
                tunnelframe.save()
                return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(tunnelframe.id,)))
        return render(request, 'tunnel_app/tun_home.html', {'form': form})

    else:
        if request.user.is_authenticated:
            form = TunnelInputForm()
            return render(request, 'tunnel_app/auth_tun_home.html', {'form': form})
        else:
            form = TunnelInputForm()
            return render(request, 'tunnel_app/tun_home.html', {'form': form})


def auth_tunnel_frame_success(request, tunnelframe_id):
    """Renders a page with the Tunnelframe object"""

    tunnel_frame = get_object_or_404(TunnelFrame, pk=tunnelframe_id)

    dimensions = {
        'inner_frame_h': tunnel_frame.frame_inner_height,
        'outer_frame_h': tunnel_frame.frame_outer_height,
        'inner_frame_w': tunnel_frame.frame_inner_width,
        'haunch_depth': tunnel_frame.haunch_depth,
        'haunch_height': tunnel_frame.haunch_width,
        'side_thickness': tunnel_frame.wall_slab_thickness,
        'top_thickness': tunnel_frame.roof_slab_thickness,
    }
    vertexes = get_geometry(tunnel_frame)['vertexes']
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

    if request.method == "GET":
        form = TunnelInputForm()
        geometry = None

    context = {
        'form': form,
        'geometry': dimensions,
        'image': "static/images/example.png",
        'vertexes': vertexes,
    }

    return render(request, 'tunnel_app/tun_home.html', context)
    # return HttpResponseRedirect(reverse('tunnel_app:tunnel_home', args=context))


class UsersFramesListView(ListView):
    template_name = ""
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return TunnelFrame.objects.filter(creator=self.request.user)


def tunnel_frame_success(request, tunnelframe):
    """Renders a Tunnelframe based on the ID"""

    tunnel_frame = tunnelframe

    dimensions = {
        'inner_frame_h': tunnel_frame.frame_inner_height,
        'outer_frame_h': tunnel_frame.frame_outer_height,
        'inner_frame_w': tunnel_frame.frame_inner_width,
        'haunch_depth': tunnel_frame.haunch_depth,
        'haunch_height': tunnel_frame.haunch_width,
        'side_thickness': tunnel_frame.wall_slab_thickness,
        'top_thickness': tunnel_frame.roof_slab_thickness,
    }
    vertexes = get_geometry(tunnel_frame)
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

    form = TunnelInputForm()

    context = {
        'form': form,
        'geometry': dimensions,
        'image': "static/images/example.png",
        'vertexes': vertexes,
    }

    return render(request, 'tunnel_app/tun_home.html', context)


def download_file(request):
    # fill these variables with real values
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % file_path
        return response
    raise Http404
