import datetime

from django.db.models import Q, Value
from django.db.models.functions import Concat
from rest_framework.decorators import api_view

from .decorators import *
from .models import *
from .schema import *


@api_view(['POST'])
@validate_api_payload(LoginUserSchema)
def authenticate_user(**kwargs):
    """
    Authenticate the user
    :param request: get the email and password from request payload and generate JWT taken
    :return: JWT token
    """
    email = kwargs["email"]
    password = kwargs['password']
    data = Users.objects.filter(Q(email=email) & Q(password=encode_string(password)))
    if not data:
        return HttpResponse(json.dumps(HttpErrorHandler.invalid_authentication()), content_type="application/json")
    token = jwt.encode({
        'user': email,
        'password': password,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, os.environ.get("JWT_SECRET_KEY", "xyz")
    )
    return HttpResponse(json.dumps({'token': token}), content_type="application/json")


@api_view(['POST'])
@login_required
@validate_api_payload(RegisterUserSchema)
def create_user(**kwargs):
    """
    Create account of user
    :param request: get the user data from request payload
    :return: success message if user has created account otherwise throw error
    """
    first_name = kwargs['first_name']
    last_name = kwargs['last_name']
    email = kwargs['email']
    password = kwargs['password']

    if Users.objects.values("id").filter(email=email):
        return HttpResponse(json.dumps(HttpErrorHandler.user_already_exist()), content_type="application/json")

    instance = Users.objects.create(first_name=first_name, last_name=last_name, email=email,
                                    password=encode_string(password))
    user_account_created['user_id'] = instance.id
    return HttpResponse(json.dumps(user_account_created), content_type="application/json")


@api_view(["GET"])
@login_required
def user_details(request):
    """
    if we get user id in request payload, get the user details using user_id
    user can search or filter using email property
    :param request: get the pagination data (page and limit) from query string. if we don't receive any parameter then default users
    limit is 10
    :return: list of users based on pagination limit
    """
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    email = request.GET.get('email')
    id = request.data.get('id')
    try:
        if id:
            data = Users.objects.values("id", "email", full_name=Concat('first_name', Value(' '), 'last_name')).filter(
                id=id)
        elif email:
            data = Users.objects.values("id", "email", full_name=Concat('first_name', Value(' '), 'last_name')).filter(
                email__contains=email)
        else:
            data = Users.objects.values("id", "email", full_name=Concat('first_name', Value(' '), 'last_name')).filter(
                id__range=[page, page + limit]).order_by('id')[:limit]
        user_list_response['user_list'] = list(data)
        return HttpResponse(json.dumps(user_list_response), content_type="application/json")
    except:
        error = HttpErrorHandler.bad_request_error()
        error['message'] = "Please Enter valid details"
        return HttpResponse(json.dumps(error), content_type="application/json")


@api_view(["PUT"])
@login_required
@validate_api_payload(UpdateUserSchema)
def update_user(id, **kwargs):
    """
    Update the user account
    :param request: get the request payload
    :param id: user id
    :return: updated request payload if user id is in our system other wise throw user is not found exception
    """
    first_name = kwargs['first_name']
    last_name = kwargs['last_name']
    email = kwargs['email']
    user = Users.objects.filter(id=int(id))
    if not user:
        return HttpResponse(json.dumps(HttpErrorHandler.resource_not_found_error()), content_type="application/json")
    user.update(first_name=first_name, last_name=last_name, email=email)
    user_account_updated['first_name'] = first_name
    user_account_updated['last_name'] = last_name
    user_account_updated['email'] = email
    return HttpResponse(json.dumps(user_account_updated), content_type="application/json")
