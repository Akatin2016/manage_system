from django.shortcuts import render


def login_check(func):
    '''
        校验用户是否登录
    '''

    def wrap(request, *args, **kwargs):
        if not request.session.get('uid'):
            return render(request, "demand/404NotFound.html")
        uid = request.session['uid']
        request.uid = uid
        return func(request, *args, **kwargs)

    return wrap
