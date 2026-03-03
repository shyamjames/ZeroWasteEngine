from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_dropdown(request):
    """HTMX endpoint fetching the actual list of notifications and marking them read."""
    notifications = Notification.objects.filter(user=request.user)[:5]
    
    # Fire and forget update marking them read so next time badge is 0
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'core/partials/notification_list.html', {'notifications': notifications})
