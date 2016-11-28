import time

from django.conf.urls import include, url
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView
from wagtail.wagtailcore import hooks

from personalisation import admin_urls
from personalisation.models import Segment, PersonalisablePage
from personalisation.utils import impersonate_other_page


@hooks.register('register_admin_urls')
def register_admin_urls():
    """Adds the administration urls for the personalisation apps."""
    return [
        url(r'^personalisation/', include(
            admin_urls,
            app_name='personalisation',
            namespace='personalisation')),
    ]


class SegmentModelAdmin(ModelAdmin):
    """The base model for the Segments administration interface."""
    model = Segment
    menu_icon = 'group'
    add_to_settings_menu = False
    list_display = ('status', 'name', 'create_date', 'edit_date')
    index_view_extra_css = ['personalisation/segment/index.css']
    form_view_extra_css = ['personalisation/segment/form.css']
    inspect_view_enabled = True

modeladmin_register(SegmentModelAdmin)


@hooks.register('before_serve_page')
def set_visit_count(page, request, serve_args, serve_kwargs):
    """Update the users visit count before each page visit."""
    # Update the segment visit count
    for seg in request.session['segments']:
        segment = Segment.objects.get(pk=seg['id'])
        segment.visit_count = segment.visit_count + 1
        segment.save()

    # Update the page visit count
    def create_new_counter(page):
        """Create a new counter dict and place it in session storage."""
        countdict = {
            "slug": page.slug,
            "id": page.pk,
            "path": page.url,
            "count": 1,
        }
        request.session['visit_count'].append(countdict)

    if len(request.session['visit_count']) > 0:
        for index, counter in enumerate(request.session['visit_count']):
            if counter['id'] == page.pk:
                # Counter already exists. Increase the count value by 1.
                newcount = counter['count'] + 1
                request.session['visit_count'][index]['count'] = newcount
                request.session.modified = True
            else:
                # Counter doesn't exist. Create a new counter with count value 1.
                create_new_counter(page)
    else:
        # No counters exist. Create a new counter with count value 1.
        create_new_counter(page)

@hooks.register('before_serve_page')
def serve_variation(page, request, serve_args, serve_kwargs):
    user_segments = []

    for segment in request.session['segments']:
        try:
            user_segment = Segment.objects.get(pk=segment['id'], status='enabled')
        except Segment.DoesNotExist:
            user_segment = None
        if user_segment:
            user_segments.append(user_segment)

    if len(user_segments) > 0:
        variations = _check_for_variations(user_segments, page)

        if variations:
            variation = variations[0]

            impersonate_other_page(variation, page)

            return variation.serve(request, *serve_args, **serve_kwargs)

def _check_for_variations(segments, page):
    for segment in segments:
        variation = PersonalisablePage.objects.filter(canonical_page=page, segment=segment)

        if variation:

            return variation

    return None
