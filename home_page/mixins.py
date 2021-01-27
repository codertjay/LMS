from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages


class InstructorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organisor."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.profile.user_type == 'Instructor':
            messages.info(request, 'You are not an instructor and also not authenticated')
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)
