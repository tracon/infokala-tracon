from django.core.management.base import BaseCommand, CommandError


def setup_basic_workflow(event_slug):
    from infokala.models import Workflow, State, MessageType, Message

    basic_workflow, unused = Workflow.objects.get_or_create(
        name='Perustyönkulku',
        slug='basic'
    )

    lost_and_found_workflow, unused = Workflow.objects.get_or_create(
        name='Löytötavaratyönkulku',
        slug='lost-and-found'
    )

    simple_workflow, unused = Workflow.objects.get_or_create(
        name='Yksinkertainen työnkulku',
        slug='simple'
    )

    order = 0
    for workflow, name, slug, initial, label_class, active in [
        (basic_workflow, 'Avoinna', 'open', True, 'label-primary', True),
        (basic_workflow, 'Hoidettu', 'resolved', False, 'label-success', False),

        (lost_and_found_workflow, 'Kateissa', 'missing', True, 'label-primary', True),
        (lost_and_found_workflow, 'Tuotu Infoon', 'found', False, 'label-info', True),
        (lost_and_found_workflow, 'Palautettu omistajalle', 'returned', False, 'label-success', False),

        (simple_workflow, 'Kirjattu', 'recorded', True, 'label-primary', True),
    ]:
        state, created = State.objects.get_or_create(
            workflow=workflow,
            slug=slug,
            defaults=dict(
                name=name,
                order=order,
                initial=initial,
            ),
        )

        state.label_class = label_class
        state.active = active
        state.save()

        order += 10

    for name, slug, workflow in [
        ('Löytötavarat', 'lost-and-found', lost_and_found_workflow),
        ('Tehtävä', 'task', basic_workflow),
        ('Lokikirja', 'event', simple_workflow),
    ]:
        message_type, unused = MessageType.objects.get_or_create(
            event_slug=event_slug,
            slug=slug,
            defaults=dict(
                name=name,
                workflow=workflow,
            ),
        )

    # make 'event' default
    message_type.default = True
    message_type.save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('event_slugs', nargs='+', type=str)

    def handle(self, *args, **opts):
        for event_slug in opts['event_slugs']:
            print('Setting up basic workflow for event', event_slug)
            setup_basic_workflow(event_slug)
