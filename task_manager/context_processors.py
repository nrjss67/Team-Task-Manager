from django.utils.text import slugify


def get_slugify_team_name(request):
    if request.user.is_authenticated:
        team_name = slugify(request.user.team.name)
        return {"team_name": team_name}
    return {"team_name": ""}


def get_unread_messages_count(request):
    from task_manager.models import MessageNew

    if request.user.is_authenticated:
        unread_messages_count = MessageNew.objects.filter(
            to_worker=request.user, is_read=False, is_archieve=False
        ).count()
        return {"unread_messages_count": unread_messages_count}
    return {"unread_messages_count": 0}
