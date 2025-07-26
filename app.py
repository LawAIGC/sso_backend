import os
import sys
import threading
from datetime import timedelta

from flask import Flask
from jwt.exceptions import ExpiredSignatureError, DecodeError
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, create_access_token
from flask_jwt_extended.exceptions import NoAuthorizationError

import api
import utils
import services
from exts import db, jwt_manager, migrate

app = Flask(__name__)

WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"

db_path = os.path.join(app.root_path, "data.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key-here"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

secret_key_filename = ".secret_key"
if not os.path.exists(secret_key_filename):
    with open(secret_key_filename, "w", encoding="utf8") as f:
        f.write(utils.random_secret_key())

with open(secret_key_filename, "r", encoding="utf8") as f:
    app.config["SECRET_KEY"] = f.read()

db.init_app(app)
jwt_manager.init_app(app)
migrate.init_app(app, db)

_initialized = False
_initialization_lock = threading.Lock()


@app.before_request
def before_first_request():
    global _initialized
    if not _initialized:
        with _initialization_lock:
            print("开始执行首次初始化")
            services.init_db()
            _initialized = True
            print("首次初始化完成")


@app.after_request
def after_request(resp):
    try:
        verify_jwt_in_request()
    except (NoAuthorizationError, ExpiredSignatureError, DecodeError):
        pass
    else:
        id_ = get_jwt_identity()
        token = create_access_token(identity=str(id_))
        resp.headers["Authorization"] = f"Bearer {token}"

    return resp


app.post("/api/v1/auth/login")(api.auth_login)  # 登录
# app.post("/api/v1/auth/refresh")(api.auth_refresh)  # 不需要 refresh_token
app.post("/api/v1/change_password")(api.api_change_password)
app.post("/api/v1/forgot_password")(api.api_forgot_password)
app.get("/api/v1/auth/verify")(api.get_user_info)

app.get("/api/permission/api/menu/list")(api.api_permission_api_menu_list)

# 角色
app.get("/api/permission/role/getlist")(api.api_permission_role_getlist)
app.get("/api/permission/role/detail")(api.api_permission_role_detail)
app.post("/api/permission/role/create")(api.api_permission_role_create)
app.post("/api/permission/role/update")(api.api_permission_role_update)
app.post("/api/permission/role/delete")(api.api_permission_role_delete)

# 用户
app.get("/api/permission/user/inner/list")(api.api_permission_user_inner_list)
app.get("/api/permission/user/detail")(api.api_permission_user_detail)
app.post("/api/permission/user/create")(api.api_permission_user_create)
app.post("/api/permission/user/update")(api.api_permission_user_update)
app.post("/api/permission/user/delete")(api.api_permission_user_delete)

# 能力
app.get("/api/permission/per/getlist")(api.api_permission_per_getlist)
app.get("/api/permission/per/detail")(api.api_permission_per_detail)
app.post("/api/permission/per/create")(api.api_permission_per_create)
app.post("/api/permission/per/update")(api.api_permission_per_update)
app.post("/api/permission/per/delete")(api.api_permission_per_delete)

app.post("/api/register_verification")(api.api_send_register_verification)
app.post("/api/register_user")(api.api_register_user)
app.post("/api/change_password_verification")(api.api_send_change_password_verification)  # noqa
app.post("/api/change_password_by_email")(api.api_change_password_by_email_verification)  # noqa


if __name__ == "__main__":
    app.run(port=9001, debug=False)
