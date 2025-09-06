import json
from datetime import datetime, timedelta

from flask import Blueprint, request, session
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,

)

import const
import utils
import restful
from services import user as user_service
from services import menu as menu_service
from services import role as role_service
from services import ability as ability_service
from services import email as email_service

api = Blueprint("api", __name__)


def auth_login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not (username and password):
        return restful.error("请求数据验证失败"), 401

    return user_service.login(username, password)

@jwt_required()
def get_user_info():
    return user_service.find_by_id(get_jwt_identity())


# 不需要 auth_refresh 了
@jwt_required(refresh=True)
def auth_refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=str(user_id))
    return restful.success(new_access_token)


def get_args_page():
    page = request.args.get("pn", 1, type=int)
    per_page = request.args.get("size", 1000, type=int)
    return page, per_page


@jwt_required()
def api_permission_api_menu_list():
    return menu_service.menus(*get_args_page())


@jwt_required()
def api_permission_role_detail():
    role_id = request.args.get("role_id")
    return role_service.find_by_id(role_id)


@jwt_required()
def api_permission_role_create():
    permission_ids = request.json.get("permission_ids", "")
    permission_ids = permission_ids.split(",")
    role_name = request.json.get("role_name")
    description = request.json.get("description")
    return role_service.create(permission_ids, role_name, description)


@jwt_required()
def api_permission_role_delete():
    role_id = request.json.get("role_id")
    return role_service.delete_by_id(role_id)


@jwt_required()
def api_permission_role_update():
    role_id = request.json.get("role_id")
    permission_ids = request.json.get("permission_ids", "")
    permission_ids = permission_ids.split(",")
    role_name = request.json.get("role_name")
    description = request.json.get("description")
    return role_service.update(role_id, permission_ids, role_name, description)


@jwt_required()
def api_permission_role_getlist():
    name = request.args.get("name")
    return role_service.roles(name, *get_args_page())


@jwt_required()
def api_permission_user_inner_list():
    name = request.args.get("name")
    return user_service.users(name, *get_args_page())


def check_password(password):
    if 6 <= len(password) <= 50:
        return True

    return False


@jwt_required()
def api_permission_user_create():
    username = request.json.get("user_name")
    password = request.json.get("password", "")
    email = request.json.get("email")
    description = request.json.get("description")
    real_name = request.json.get("real_name")
    role_type = request.json.get("role_type")  # noqa
    role_infos = request.json.get("roleinfos")

    if not username:
        return restful.error("username required")
    elif not 3 <= len(username) <= 50:
        return restful.error("username length >= 3 and <= 50")

    if not check_password(password):
        return restful.error("invalid password")

    role_ids = []
    if role_infos:
        role_infos = json.loads(role_infos)
        for role in role_infos:
            role_ids.append(role["role_id"])

    return user_service.create(
        username=username,
        password=password,
        email=email,
        real_name=real_name,
        description=description,
        role_ids=role_ids
    )


@jwt_required()
def api_permission_user_detail():
    user_id = request.args.get("user_id")
    return user_service.find_by_id(user_id)


@jwt_required()
def api_permission_user_delete():
    user_id = request.json.get("user_id")
    return user_service.delete_by_id(user_id)


@jwt_required()
def api_permission_user_update():
    user_id = request.json.get("user_id")
    username = request.json.get("user_name")
    real_name = request.json.get("real_name")
    email = request.json.get("email")
    description = request.json.get("description")
    role_type = request.json.get("role_type")  # noqa
    role_infos = request.json.get("roleinfos")

    role_ids = []
    if role_infos:
        role_infos = json.loads(role_infos)
        for role in role_infos:
            role_ids.append(role["role_id"])

    return user_service.update(
        id_=user_id,
        username=username,
        email=email,
        real_name=real_name,
        description=description,
        role_ids=role_ids,
    )


@jwt_required()
def api_permission_per_detail():
    permission_id = request.args.get("permission_id")
    return ability_service.find_by_id(permission_id)


@jwt_required()
def api_permission_per_delete():
    permission_id = request.json.get("permission_id")
    return ability_service.delete_by_id(permission_id)


@jwt_required()
def api_permission_per_getlist():
    permission = request.args.get("permission")
    return ability_service.abilities(permission, *get_args_page())


@jwt_required()
def api_permission_per_update():
    id_ = request.json.get("id")
    name = request.json.get("name")
    menu_ids = request.json.get("menu_ids")

    if id_ and name and isinstance(menu_ids, list):
        return ability_service.update(id_, name, menu_ids)

    return restful.error("id, name, menu_ids required"), 400


@jwt_required()
def api_permission_per_create():
    name = request.json.get("name")
    menu_ids = request.json.get("menu_ids")

    if name and isinstance(menu_ids, list):
        return ability_service.create(name, menu_ids)

    return restful.error("name, menu_ids required"), 400


@jwt_required()
def api_change_password():
    user_id = request.json.get("user_id")
    password = request.json.get("password", "")

    if not check_password(password):
        return restful.error("invalid password"), 400

    if user_id and password:
        return user_service.change_password(user_id, password=password)

    return restful.error("user_id, password required"), 400


def api_forgot_password():
    username = request.json.get("username")

    if not username:
        return restful.error("username required"), 400

    return user_service.forgot_password(username)


def api_send_register_verification():
    email = request.json.get("email")
    if not email:
        return restful.error("email required"), 400

    if not utils.is_valid_email(email):
        return restful.error("invalid email"), 400

    if user_service.has_email(email):
        return restful.error("invalid email"), 400

    code = utils.random_code()
    session[const.SESSION_KEY_REGISTER_VERIFICATION_CODE] = code
    session[const.SESSION_KEY_REGISTER_VERIFICATION_EMAIL] = email
    session[const.SESSION_KEY_REGISTER_VERIFICATION_TIMESTAMP] = (
        datetime.now() + timedelta(minutes=5)
    ).timestamp()

    if email_service.send(email, "【wenhuatech】注册验证码", f"你的注册验证码是：{code}，5分钟内有效。"):
        return restful.success("successfully")

    return restful.error("服务器开小差了，请稍后再试")


def api_register_user():
    username = request.json.get("username")
    if not username:
        return restful.error("username required")
    if user_service.has_username(username):
        return restful.error("invalid username"), 400

    email = request.json.get("email")
    if not email:
        return restful.error("email required"), 400
    if not utils.is_valid_email(email):
        return restful.error("invalid email"), 400

    dept = request.json.get("dept")
    if not dept:
        return restful.error("dept required"), 400

    code = request.json.get("code")
    if not code:
        return restful.error("code required"), 400

    try:
        if (
            session[const.SESSION_KEY_REGISTER_VERIFICATION_EMAIL] != email or
            session[const.SESSION_KEY_REGISTER_VERIFICATION_CODE] != code or
            datetime.now().timestamp() > session[const.SESSION_KEY_REGISTER_VERIFICATION_TIMESTAMP]  # noqa
        ):
            raise KeyError
    except KeyError:
        return restful.error("无效验证码"), 400

    session.pop(const.SESSION_KEY_REGISTER_VERIFICATION_EMAIL)
    session.pop(const.SESSION_KEY_REGISTER_VERIFICATION_CODE)
    session.pop(const.SESSION_KEY_REGISTER_VERIFICATION_TIMESTAMP)

    return user_service.register(username, email, dept)


def api_send_change_password_verification():
    username = request.json.get("username")
    if not username:
        return restful.error("username required"), 400

    email = request.json.get("email")
    if not email:
        return restful.error("email required"), 400
    if not utils.is_valid_email(email):
        return restful.error("invalid email"), 400

    if not user_service.has_username_email(username, email):
        return restful.error("invalid username or email"), 400

    code = utils.random_code()
    session[const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_NAME] = username
    session[const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_CODE] = code
    session[const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_EMAIL] = email
    session[const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_TIMESTAMP] = (
        datetime.now() + timedelta(minutes=3)
    ).timestamp()

    if email_service.send(email, "修改密码验证码", f"您的验证码是: {code}"):
        return restful.success("successfully")

    return restful.error("服务器开小差了，请稍后再试")


def api_change_password_by_email_verification():
    username = request.json.get("username")
    if not username:
        return restful.error("username required"), 400

    email = request.json.get("email")
    if not email:
        return restful.error("email required"), 400

    password = request.json.get("password")
    if not password:
        return restful.error("password required"), 400
    if not check_password(password):
        return restful.error("invalid password"), 400

    code = request.json.get("code")
    if not code:
        return restful.error("code required"), 400

    try:
        if (
            session[const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_NAME] != username or  # noqa
            session[const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_EMAIL] != email or  # noqa
            session[const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_CODE] != code or  # noqa
            datetime.now().timestamp() > session[const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_TIMESTAMP]  # noqa
        ):
            raise KeyError
    except KeyError:
        return restful.error("无效验证码"), 400

    session.pop(const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_NAME)
    session.pop(const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_EMAIL)
    session.pop(const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_CODE)
    session.pop(const.SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_TIMESTAMP)

    return user_service.change_password_by_username_email(username, email, password)
