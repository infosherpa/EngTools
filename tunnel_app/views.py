from unicodedata import decimal
from django.shortcuts import render, reverse, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template.loader import render_to_string
from django.core import validators, serializers
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
import json
import cairo
from .forms import TunnelInputForm, TunnelForm, LoadDefinitionForm, TunnelFormGeometry, TunnelFormConcourseColumns, \
    TunnelFrameModifiers
from .models import TunnelFrame, LoadDefinition
from django.views.generic.list import ListView
from .functions.geometry import get_geometry
from .functions.excel import create_workbook
from .functions.cairo import cairo_draw_frame
import mimetypes
import os
from django.conf import settings
import secrets
from PIL import Image


class UsersFramesListView(ListView):
    template_name = ""
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return TunnelFrame.objects.filter(creator=self.request.user)


def download_file(request):
    # fill these variables with real values
    path = None
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % file_path
        return response
    raise Http404


def tunnel_app_home2(request):
    """Homepage for 2D Tunnel App & Tunnel Frame Information Form"""

    if request.method == "POST":

        if '_generate' in request.POST or '_excel' in request.POST or '_save' in request.POST:

            # Routine if request is for Tunnelframe Object

            form = TunnelForm(request.POST)

            if form.is_valid():

                tunnelframe = form.save(commit=False)
                tunnelframe.wall_slab_thickness = (form.cleaned_data['frame_outer_width'] -
                                                   form.cleaned_data['frame_inner_width']) / 2
                tunnelframe.inverse_slab_thickness = (
                    form.cleaned_data['frame_outer_height'] - form.cleaned_data['frame_inner_height']
                    - form.cleaned_data['roof_slab_thickness']
                )
                token_url = str(secrets.token_hex(6))[:8]
                tunnelframe.hash = token_url
                if request.user.is_authenticated:
                    tunnelframe.creator = request.user.id

                if '_generate' in request.POST:
                    tunnelframe.save()
                    return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(token_url,)))

                if '_excel' in request.POST:
                    tunnelframe.grid_lines()
                    tunnelframe.get_frame_geometry()
                    return create_workbook(tunnelframe)

                if '_save' in request.POST:
                    save_tunnelframe(request, tunnelframe)
                    # After saving the tunnelframe object we must save all associated defined loads for
                    # our tunnelframe

                    return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(tunnelframe.id,)))

            else:
                form = TunnelForm(request.POST)
                return render(request, 'tunnel_app/tun_home2.html', {'tunnel_form': form})

        form = TunnelForm()
        return render(request, 'tunnel_app/tun_home2.html', {'tunnel_form': form})

    else:
        tunnel_form_default_data = {
            'wall_stiffness_modifier': 0.7,
            'slab_stiffness_modifier': 0.5,
            'column_stiffness_modifier': 0.7
        }
        form = TunnelForm(initial=tunnel_form_default_data)
        return render(request, 'tunnel_app/tun_home2.html', {'tunnel_form': form})


@login_required()
def save_tunnelframe(request, tunnelframe):
    tunnelframe.creator = request.user
    tunnelframe.save()

    # After saving the tunnelframe object we must save all associated defined loads for
    # our tunnelframe


def auth_tunnel_frame_success(request, tunnelframe_hash):
    """Renders a page with the Tunnelframe object"""

    tunnelframe = get_object_or_404(TunnelFrame, hash=tunnelframe_hash)

    loads = LoadDefinition.objects.filter(parent_frame=tunnelframe.id)

    form_data = {
        'frame_description': tunnelframe.frame_description,
        'frame_inner_height': tunnelframe.frame_inner_height,
        'frame_outer_height':  tunnelframe.frame_outer_height,
        'frame_inner_width': tunnelframe.frame_inner_width,
        'frame_outer_width': tunnelframe.frame_outer_width,
        'haunch_depth': tunnelframe.haunch_depth,
        'haunch_width': tunnelframe.haunch_width,
        'roof_slab_thickness': tunnelframe.roof_slab_thickness,
        'concourse_slab_thickness':tunnelframe.concourse_slab_thickness,
        'concourse_slab_vertical_location':tunnelframe.concourse_slab_vertical_location,
        'column_capital_height':tunnelframe.column_capital_height,
        'column_capital_width':tunnelframe.column_capital_width,
        'concourse_haunch_width':tunnelframe.concourse_haunch_width,
        'concourse_haunch_depth':tunnelframe.concourse_haunch_depth,
        'column_bays': tunnelframe.column_bays,
        'column_width': tunnelframe.column_width,
        'wall_stiffness_modifier': tunnelframe.wall_stiffness_modifier,
        'slab_stiffness_modifier': tunnelframe.slab_stiffness_modifier,
        'column_stiffness_modifier': tunnelframe.column_stiffness_modifier,
        'column_capital_roof_slab_height': tunnelframe.column_capital_roof_slab_height,
        'column_capital_roof_slab_width': tunnelframe.column_capital_roof_slab_width,
        'concrete_strength_columns': tunnelframe.concrete_strength_columns,
        'concrete_strength_slabs': tunnelframe.concrete_strength_slabs,
        'concrete_strength_walls': tunnelframe.concrete_strength_walls,
    }

    form = TunnelForm(initial=form_data)

    if request.method == 'POST':

    # tunnelframe = request.session['tunnelframe']
    # tunnelframe = serializers.deserialize('json', tunnelframe)

    # form = request.session['tunnel_form']
    # form = serializers.deserialize('json', form)

        if '_load' in request.POST:

            load_form = LoadDefinitionForm(request.POST)

            if load_form.is_valid():
                load_definition = load_form.save(commit=False)
                load_definition.parent_frame = tunnelframe
                load_definition.parent_frame_description = tunnelframe.frame_description
                load_definition.save()

                print(loads)
                tunnelframe.grid_lines()
                tunnelframe.get_frame_geometry()
                img = Image.open(f"mediafiles/images/frames/{tunnelframe.hash}.png")
                img_w, img_h = img.size
                if img_w > img_h:
                    img_h = img_h / img_w * 636
                    img_w = 636
                else:
                    img_w = img_w / img_h * 636
                    img_h = 636

                context = {
                    'grid': [tunnelframe.grid_locations_x, tunnelframe.grid_locations_z],
                    'joints': tunnelframe.joint_coordinates,
                    'members': tunnelframe.connectivity_frame,
                    'tunnel_form': form,
                    'load_form': load_form,
                    'image': f"images/frames/{tunnelframe.hash}.png",
                    'loads_list': loads,
                    'tunnelframe': tunnelframe,
                    'img_w': img_w,
                    'img_h': img_h,
                }

                return render(request, 'tunnel_app/tun_home2.html', context)

            else:
                print('load_form_error')

        if '_excel' in request.POST:
            tunnelframe.grid_lines()
            tunnelframe.get_frame_geometry()
            return create_workbook(tunnelframe)

        if '_generate' in request.POST:

            form = TunnelForm(request.POST, instance=tunnelframe)
            print(request.POST)

            if form.is_valid():
                tunnelframe.wall_slab_thickness = (form.cleaned_data['frame_outer_width'] -
                                                   form.cleaned_data['frame_inner_width']) / 2
                tunnelframe.inverse_slab_thickness = (
                        form.cleaned_data['frame_outer_height'] - form.cleaned_data['frame_inner_height']
                        - form.cleaned_data['roof_slab_thickness']
                )
                form.save()
                print('redirect')
                return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(tunnelframe.hash,)))

            else:
                # raise flag for form error
                print('form_error')
                tunnelframe = get_object_or_404(TunnelFrame, hash=tunnelframe_hash)
                tunnelframe.grid_lines()
                tunnelframe.get_frame_geometry()
                load_form = LoadDefinitionForm()
                img = Image.open(f"mediafiles/images/frames/{tunnelframe.hash}.png")
                img_w, img_h = img.size
                if img_w > img_h:
                    img_h = img_h/img_w*636
                    img_w = 636
                else:
                    img_w = img_w / img_h * 636
                    img_h = 636

                context = {
                    'grid': [tunnelframe.grid_locations_x, tunnelframe.grid_locations_z],
                    'joints': tunnelframe.joint_coordinates,
                    'members': tunnelframe.connectivity_frame,
                    'tunnel_form': form,
                    'load_form': load_form,
                    'image': f"images/frames/{tunnelframe.hash}.png",
                    'loads_list': loads,
                    'tunnelframe': tunnelframe,
                    'img_w': img_w,
                    'img_h': img_h,
                }
                return render(request, 'tunnel_app/tun_home2.html', context)

        if '_del_load' in request.POST:
            pass

        print(request.method)

    if request.method == 'GET':

        load_form = LoadDefinitionForm()
        tunnelframe.grid_lines()
        tunnelframe.get_frame_geometry()
        cairo_draw_frame(tunnelframe)
        img = Image.open(f"mediafiles/images/frames/{tunnelframe.hash}.png")
        img_w, img_h = img.size
        if img_w > img_h:
            img_h = img_h / img_w * 636
            img_w = 636
        else:
            img_w = img_w / img_h * 636
            img_h = 636
        context = {
            'grid': [tunnelframe.grid_locations_x, tunnelframe.grid_locations_z],
            'joints': tunnelframe.joint_coordinates,
            'members': tunnelframe.connectivity_frame,
            'tunnel_form': form,
            'load_form': load_form,
            'image': f"images/frames/{tunnelframe.hash}.png",
            'loads_list': loads,
            'tunnelframe': tunnelframe,
            'img_w': img_w,
            'img_h': img_h,
        }
        return render(request, 'tunnel_app/tun_home2.html', context)


def tunnel_delete_load(request, tunnelframe_hash, load_num):
    LoadDefinition.objects.filter(load_id=load_num).delete()
    return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(tunnelframe_hash,)))


def get_form_ajax(request, tunnelframe_hash, form_num):

    print(tunnelframe_hash)

    form_data = {
        'hash': f'{tunnelframe_hash}',
    }
    print(form_num)
    if form_num == 2:
        form = TunnelFormConcourseColumns(initial=form_data)
    elif form_num == 3:
        form = TunnelFrameModifiers(initial=form_data)

    context = {
        "form": form,
    }
    context.update(csrf(request))
    template = render_to_string('forms/form.html', context=context)
    return JsonResponse({"form": template, "success": True})


def ajax_post_view(request):
    if request.method == 'POST':

        context_dict = {}

        if 'geo_form' in request.POST['form']:

            tunnel_geo_form = TunnelFormGeometry(request.POST)

            if tunnel_geo_form.is_valid():
                # do the stuff to save to database
                print('data valid')

                tunnelframe = tunnel_geo_form.save(commit=False)
                tunnelframe.wall_slab_thickness = (tunnel_geo_form.cleaned_data['frame_outer_width'] -
                                                   tunnel_geo_form.cleaned_data['frame_inner_width']) / 2
                tunnelframe.inverse_slab_thickness = (
                        tunnel_geo_form.cleaned_data['frame_outer_height'] - tunnel_geo_form.cleaned_data['frame_inner_height']
                        - tunnel_geo_form.cleaned_data['roof_slab_thickness']
                )
                token_url = str(secrets.token_hex(6))[:8]
                tunnelframe.hash = token_url
                if request.user.is_authenticated:
                    tunnelframe.creator = request.user.id
                tunnelframe.save()
                print(tunnelframe.hash)
                print('tunnelframe saved')
                form_num = 2

                return HttpResponseRedirect(reverse('tunnel_app:get_form_ajax', args=(token_url, form_num)))

            else:
                ctx = {}
                ctx.update(csrf(request))
                ctx['errors'] = tunnel_geo_form.errors
                print('invalid form')
                print(tunnel_geo_form.errors)
                form_html = render_crispy_form(tunnel_geo_form, context=ctx)
                return JsonResponse({'success': False, 'form_html': form_html})

        if 'concourse_col_form' in request.POST['form']:

            tunnelframe_hash = request.POST['hash']
            tunnelframe = get_object_or_404(TunnelFrame, hash=tunnelframe_hash)
            concourse_columns_form = TunnelFormConcourseColumns(request.POST, instance=tunnelframe)

            if concourse_columns_form.is_valid():
                print('concourse_form_valid')

                tunnelframe = concourse_columns_form.save(commit=False)
                print(tunnelframe.hash)
                tunnelframe.save()
                form_num = 3

                return HttpResponseRedirect(reverse('tunnel_app:get_form_ajax', args=(tunnelframe.hash, form_num)))

        if 'conc_mod_form' in request.POST['form']:

            print('form in form')
            tunnelframe_hash = request.POST['hash']
            tunnelframe = get_object_or_404(TunnelFrame, hash=tunnelframe_hash)
            concourse_columns_form = TunnelFrameModifiers(request.POST, instance=tunnelframe)

            if concourse_columns_form.is_valid():
                print('modifiers valid')
                tunnelframe = concourse_columns_form.save(commit=False)
                tunnelframe.save()
                return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(tunnelframe.hash,)))

        else:
            # form not valid, return false with the rendered form
            context_dict['success'] = False

            return JsonResponse(context_dict)

    return None


def tunnel_app_home_w_java(request, tunnelframe_hash=None):
    """Homepage for 2D Tunnel App & Tunnel Frame Information Form"""

    if request.method == "POST":

        if '_generate' in request.POST or '_excel' in request.POST or '_save' in request.POST:

            # Routine if request is for Tunnelframe Object

            form = TunnelFormGeometry(request.POST)

            if 'conc_mod_form' in request.POST['form']:

                print('form in form')
                tunnelframe_hash = request.POST['hash']
                tunnelframe = get_object_or_404(TunnelFrame, hash=tunnelframe_hash)
                concourse_columns_form = TunnelFrameModifiers(request.POST, instance=tunnelframe)

                if concourse_columns_form.is_valid():
                    print('modifiers valid')
                    tunnelframe = concourse_columns_form.save(commit=False)
                    tunnelframe.save()
                    return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(tunnelframe.hash,)))

                if '_generate' in request.POST:
                    tunnelframe.save()
                    return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(tunnelframe.hash,)))

                if '_excel' in request.POST:
                    tunnelframe.grid_lines()
                    tunnelframe.get_frame_geometry()
                    return create_workbook(tunnelframe)

                if '_save' in request.POST:
                    save_tunnelframe(request, tunnelframe)
                    # After saving the tunnelframe object we must save all associated defined loads for
                    # our tunnelframe

                    return HttpResponseRedirect(reverse('tunnel_app:auth_results', args=(tunnelframe.id,)))

            else:
                form = TunnelForm(request.POST)
                return render(request, 'tunnel_app/tun_home2.html', {'tunnel_form': form})

        if 'concourse_col_form' in request.POST['form']:

            tunnelframe_hash = request.POST['hash']
            tunnelframe = get_object_or_404(TunnelFrame, hash=tunnelframe_hash)
            concourse_columns_form = TunnelFormConcourseColumns(request.POST, instance=tunnelframe)

            if concourse_columns_form.is_valid():
                print('concourse_form_valid')

                tunnelframe = concourse_columns_form.save(commit=False)
                print(tunnelframe.hash)
                tunnelframe.save()
                form_num = 3

                return HttpResponseRedirect(reverse('tunnel_app:get_form_ajax', args=(tunnelframe.hash, form_num)))

        print('unnamed post request')
        print(request)
        print(request.POST)
        form = TunnelFormGeometry()
        return render(request, 'tunnel_app/tun_home2.html', {'tunnel_form': form})

    else:
        form = TunnelFormGeometry()
        return render(request, 'tunnel_app/tun_home2.html', {'tunnel_form': form})


def bugreport(request):
    context = {"success": True}
    return JsonResponse(context)