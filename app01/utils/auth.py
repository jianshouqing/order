from django.middleware.common import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect

class Context:
    def __init__(self, role,id,name):
        self.role = role
        self.id = id
        self.name = name

class AuthMiddlewarePathInfo(MiddlewareMixin):

    def is_white_url_by_path_info(self,request):
        if request.path_info in settings.NB_WHITE_URL:
            return True

    # 还没有进行路由匹配前
    def process_request(self, request):

        # 设置白名单，无需登录就能访问，如：login、sms/login、send/sms
        if self.is_white_url_by_path_info(request):
            return

        # 读取session信息
        # 有一个问题就是第一次访问login时是没有登录的，是没有session的，这样会一直重定向到login，会报错重定向次数过多
        # 解决这个问题，设置白名单
        data_dict = request.session.get(settings.NB_SESSION_KEY)

        # session不存在，返回登录界面
        if not data_dict:
            return redirect(settings.NB_LOGIN_NAME)

        request.nb_user = Context(**data_dict)



# class AuthMiddleware(MiddlewareMixin):
#
#     def is_white_url_by_path_info(self,request):
#         if request.path_info in ["/login/", "/sms/login/", "/send/sms/"]:
#             return True
#
#     def is_white_url_by_name(self,request):
#         url_name = request.resolver_match.url_name
#         if url_name in settings.NB_WHITE_URL:
#             return True
#
#     # 还没有进行路由匹配前
#     def process_request(self, request):
#
#         # 设置白名单，无需登录就能访问，如：login、sms/login、send/sms
#         if self.is_white_url_by_path_info(request):
#             return
#
#         # 读取session信息
#         # 有一个问题就是第一次访问login时是没有登录的，是没有session的，这样会一直重定向到login，会报错重定向次数过多
#         # 解决这个问题，设置白名单
#         data_dict = request.session.get(settings.NB_SESSION_KEY)
#
#         # session不存在，返回登录界面
#         if not data_dict:
#             return redirect(settings.NB_LOGIN_NAME)
#
#         request.nb_user = Context(**data_dict)
#
#         return redirect(settings.HOME_URL)
#
#     # 路由匹配后
#     def process_view(self, request, callback, callback_args, callback_kwargs):
#
#         # 设置白名单，无需登录就能访问，如：login、sms/login、send/sms
#         # 这里用名称进行匹配
#         if self.is_white_url_by_name(request) in settings.NB_WHITE_URL:
#             return
#
#         # 读取session信息
#         # 有一个问题就是第一次访问login时是没有登录的，是没有session的，这样会一直重定向到login，会报错重定向次数过多
#         # 解决这个问题，设置白名单
#         data_dict = request.session.get(settings.NB_SESSION_KEY)
#
#         # session不存在，返回登录界面
#         if not data_dict:
#             return redirect(settings.NB_LOGIN_NAME)
#
#         request.nb_user = Context(**data_dict)
#




