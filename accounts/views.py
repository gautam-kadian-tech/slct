"""Accounts view module."""
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from accounts.models import User, UserLoginDetail
from accounts.serializers import LoginSerializer
from accounts.user_role_choices import UserActionChoices
from analytical_data.utils import Responses


class LoginAPIView(GenericAPIView):
    """
    Login API, takes data post request authenticates is user
    with associated email-password combination is correct, and logs in.
    """

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"session": request.session}
        )
        if serializer.is_valid():
            login_action = UserLoginDetail(
                user=User.objects.filter(email=serializer.data.get("email")).first(),
                activity_type=UserActionChoices.LOGIN.value,
            )
            login_action.save()
            return Responses.success_response(
                "Successfully logged in.", data=serializer.data
            )
        return Responses.error_response("Login failure.", data=serializer.errors)


class LogoutAPIView(GenericAPIView):
    """Logout API class to delete a logged in user's token."""

    def delete(self, request, *args, **kwargs):
        """Logout a user."""
        UserLoginDetail.objects.create(
            user=request.user, activity_type=UserActionChoices.LOGOUT
        )
        request.user.auth_token.delete()
        # for key in request.session.keys():
        #     del request.session[key]
        request.session.flush()
        return Responses.success_response(
            "User logged out.", status.HTTP_204_NO_CONTENT
        )
