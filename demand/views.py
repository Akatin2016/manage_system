import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from demand.models import Mission, Log, File
from django.db import connection, transaction

# Create your views here.
from demand.tools.check_login_status import login_check
from manage_system import settings


# @login_check
@transaction.atomic
def index(request):
    '''
        需求查询首页
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'demand/index.html')
    elif request.method == 'POST':
        dname = request.POST.get('dname')
        no = request.POST.get('no')
        type = request.POST.get('hidden1')
        state = request.POST.get('hidden2')
        level = request.POST.get('hidden3')
        cursor = connection.cursor()
        if no != "":
            # 用编号查询（唯一结果）
            sql = 'select id,missionname,(select words from code where value=missiontype and codetype=\'type\') ' \
                  'as missiontype,' \
                  '(select words from code where value=missionstate and codetype=\'state\') as missionstate,' \
                  'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel and ' \
                  'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission where id=%s;' % no
            cursor.execute(sql)
            rawdata = cursor.fetchall()
            if not rawdata:
                return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
            result = []
            col_names = [desc[0] for desc in cursor.description]
            for r in rawdata:
                objdict = {}
                for k, v in enumerate(r):
                    objdict[col_names[k]] = v
                result.append(objdict)
            return JsonResponse({"code": 200, "data": result})
        else:
            if dname != "" and type == "" and state == "" and level == "":
                # 用任务名称查询（可能有同名任务）
                sql = 'select id,missionname,(select words from code where value=missiontype and codetype=\'type\') ' \
                      'as missiontype,' \
                      '(select words from code where value=missionstate and codetype=\'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel and ' \
                      'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missionname="%s";' % dname
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname != "" and type != "" and state == "" and level == "":
                # 用任务名称和类型查询
                sql = 'select id,missionname,(select words from code where value="%s" and codetype=\'type\') ' \
                      'as missiontype,' \
                      '(select words from code where value=missionstate and codetype=\'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel and ' \
                      'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission where missiontype=' \
                      '(select value from code where codetype=\'type\' and value="%s") and missionname="%s";' % (
                          type, type, dname)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname != "" and type == "" and state != "" and level == "":
                # 用任务名称和状态查询
                sql = 'select id,missionname,(select words from code where value=missiontype and codetype=\'type\') ' \
                      'as missiontype,' \
                      '(select words from code where value="%s" and codetype=\'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel and ' \
                      'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission where missionstate=' \
                      '(select value from code where codetype=\'state\' and value="%s") and missionname="%s";' % (
                          state, state, dname)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname != "" and type == "" and state == "" and level != "":
                # 用任务名称和等级查询
                sql = 'select id,missionname,(select words from code where value=missiontype and codetype=\'type\') ' \
                      'as missiontype,' \
                      '(select words from code where value=missionstate and codetype=\'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value="%s" and ' \
                      'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission where missionlevel=' \
                      '(select value from code where codetype=\'level\' and value="%s") and missionname="%s";' % (
                          level, level, dname)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname != "" and type != "" and state != "" and level == "":
                # 用任务名称、类型、状态查询
                sql = 'select id,missionname,(select words from code where value="%s" and codetype=\'type\') ' \
                      'as missiontype,' \
                      '(select words from code where value="%s" and codetype=\'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel and ' \
                      'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission where missiontype=' \
                      '(select value from code where codetype=\'type\' and value="%s") and missionstate=(select value ' \
                      'from code where codetype=\'state\' and value="%s") and missionname="%s";' % (
                          type, state, type, state, dname)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname != "" and type != "" and state == "" and level != "":
                # 用任务名称、类型、等级查询
                sql = 'select id,missionname,(select words from code where value="%s" and codetype=\'type\') ' \
                      'as missiontype,' \
                      '(select words from code where value=missionstate and codetype=\'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value="%s" and ' \
                      'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission where missiontype=' \
                      '(select value from code where codetype=\'type\' and value="%s") and missionlevel=(select value ' \
                      'from code where codetype=\'level\' and value="%s") and missionname="%s";' % (
                          type, level, type, level, dname)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname != "" and type == "" and state != "" and level != "":
                # 用任务名称、状态、等级查询
                sql = 'select id,missionname,(select words from code where value=missiontype and codetype=\'type\') ' \
                      'as missiontype,' \
                      '(select words from code where value="%s" and codetype=\'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value="%s" and ' \
                      'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission where missionstate=' \
                      '(select value from code where codetype=\'state\' and value="%s") and missionlevel=(select ' \
                      'value from code where codetype=\'level\' and value="%s") and missionname="%s";' % (
                          state, level, state, level, dname)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname == "" and type == "" and state == "" and level == "":
                # （任务名称为空请求时返回全部结果）
                sql = 'select id,missionname,(select words from code where value=missiontype and codetype=\'type\') ' \
                      'as missiontype,' \
                      '(select words from code where value=missionstate and codetype=\'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel and ' \
                      'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission;'
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname == "" and type != "" and state == "" and level == "":
                # 用任务类型查询（多个结果）
                sql = 'select id,missionname,(select words from code where value = "%s" and codetype=\'type\')' \
                      'as missiontype,' \
                      '(select words from code where value = missionstate and codetype = \'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel and ' \
                      'codetype = \'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missiontype = ' \
                      '(select value from code where codetype=\'type\' and value="%s");' % (type, type)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname == "" and type == "" and state != "" and level == "":
                # 用任务状态查询（多个结果）
                sql = 'select id,missionname,(select words from code where value = missiontype and codetype=\'type\')' \
                      'as missiontype,' \
                      '(select words from code where value = "%s" and codetype = \'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel and ' \
                      'codetype = \'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missionstate = ' \
                      '(select value from code where codetype=\'state\' and value="%s");' % (state, state)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname == "" and type == "" and state == "" and level != "":
                # 用需求等级查询（多个结果）
                sql = 'select id,missionname,(select words from code where value = missiontype and codetype=\'type\')' \
                      'as missiontype,' \
                      '(select words from code where value = missionstate and codetype = \'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value="%s" and ' \
                      'codetype = \'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missionlevel = ' \
                      '(select value from code where codetype=\'level\' and value="%s");' % (level, level)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname == "" and type != "" and state != "" and level == "":
                # 用任务类型和任务状态查询（多个结果）
                sql = 'select id,missionname,(select words from code where value = "%s" and codetype=\'type\')' \
                      'as missiontype,' \
                      '(select words from code where value = "%s" and codetype = \'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value = missionlevel ' \
                      'and codetype = \'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missiontype = (select value from code where codetype=\'type\' and value = "%s") and ' \
                      'missionstate = (select value from code where codetype=\'state\' and value="%s");' % (
                          type, state, type, state)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname == "" and type != "" and state == "" and level != "":
                # 用任务类型和需求等级查询（多个结果）
                sql = 'select id,missionname,(select words from code where value = "%s" and codetype=\'type\')' \
                      'as missiontype,' \
                      '(select words from code where value = missionstate and codetype = \'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value = "%s" ' \
                      'and codetype = \'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missiontype = (select value from code where codetype=\'type\' and value = "%s") and ' \
                      'missionlevel = (select value from code where codetype=\'level\' and value="%s");' % (
                          type, level, type, level)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname == "" and type == "" and state != "" and level != "":
                # 用任务状态和需求等级查询（多个结果）
                sql = 'select id,missionname,(select words from code where value = missiontype and codetype=\'type\')' \
                      'as missiontype,' \
                      '(select words from code where value = "%s" and codetype = \'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value = "%s" ' \
                      'and codetype = \'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missionstate = (select value from code where codetype=\'state\' and value = "%s") and ' \
                      'missionlevel = (select value from code where codetype=\'level\' and value="%s");' % (
                          state, level, state, level)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname == "" and type != "" and state != "" and level != "":
                # 用任务类型、任务状态和需求等级查询（多个结果）
                sql = 'select id,missionname,(select words from code where value = "%s" and codetype=\'type\')' \
                      'as missiontype,' \
                      '(select words from code where value = "%s" and codetype = \'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value = "%s" ' \
                      'and codetype = \'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missiontype = (select value from code where codetype=\'type\' and value = "%s") and ' \
                      'missionstate = (select value from code where codetype=\'state\' and value="%s") and ' \
                      'missionlevel = (select value from code where codetype=\'level\' and value = "%s");' % (
                          type, state, level, type, state, level)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            elif dname != "" and type != "" and state != "" and level != "":
                # 用任务名称、类型、状态、等级查询
                sql = 'select id,missionname,(select words from code where value = "%s" and codetype=\'type\')' \
                      'as missiontype,' \
                      '(select words from code where value = "%s" and codetype = \'state\') as missionstate,' \
                      'usercompany,username,usertel,receivetime,(select words from code where value = "%s" ' \
                      'and codetype = \'level\') as missionlevel,remark,usertestdate,phdate from mission where ' \
                      'missiontype = (select value from code where codetype=\'type\' and value = "%s") and ' \
                      'missionstate = (select value from code where codetype=\'state\' and value="%s") and ' \
                      'missionlevel = (select value from code where codetype=\'level\' and value = "%s") and ' \
                      'missionname = "%s";' % (
                          type, state, level, type, state, level, dname)
                cursor.execute(sql)
                rawdata = cursor.fetchall()
                if not rawdata:
                    return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
                result = []
                col_names = [desc[0] for desc in cursor.description]
                for r in rawdata:
                    objdict = {}
                    for k, v in enumerate(r):
                        objdict[col_names[k]] = v
                    result.append(objdict)
                return JsonResponse({"code": 200, "data": result})
            else:
                return JsonResponse({"code": 1002, "data": {"message": "Lacking of necessary conditions!"}})

    elif request.method == 'DELETE':
        no = request.GET.get('no')
        cursor = connection.cursor()
        sql = 'select missionname from mission where id=%s;' % no
        cursor.execute(sql)
        rawdata = cursor.fetchall()
        if rawdata[0] == "0000":
            return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
        else:
            sql_update = 'update mission set missionstate="0000" where id=%s;' % no
            sql_query = 'select id,missionname,(select words from code where value=missiontype and ' \
                        'codetype=\'type\') ' \
                        'as missiontype,' \
                        '(select words from code where value=missionstate and codetype=\'state\') as missionstate,' \
                        'usercompany,username,usertel,receivetime,(select words from code where value=missionlevel ' \
                        'and ' \
                        'codetype=\'level\') as missionlevel,remark,usertestdate,phdate from mission;'
            cursor.execute(sql_update)
            cursor.execute(sql_query)
            rawdata = cursor.fetchall()
            result = []
            col_names = [desc[0] for desc in cursor.description]
            for r in rawdata:
                objdict = {}
                for k, v in enumerate(r):
                    objdict[col_names[k]] = v
                result.append(objdict)
            print(result)
            # 插入日志表
            # uid = request.session['uid']
            # Log.objects.create(missionid=int(no), missionstate="0000", logerid=uid)
            return JsonResponse({"code": 200, "data": result})
    else:
        return render(request, "demand/404NotFound.html")


# @login_check
def insert(request):
    '''
        需求录入
    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request, "demand/insert.html")
    elif request.method == "POST":
        dname = request.POST.get('dname')
        type = request.POST.get('hidden1')
        state = request.POST.get('hidden2')
        level = request.POST.get('hidden3')
        usercompany = request.POST.get('usercompany')
        username = request.POST.get('username')
        usertel = request.POST.get('usertel')
        remark = request.POST.get('remark')
        usertestdate = request.POST.get('usertestdate')
        phdate = request.POST.get('phdate')
        exist = Mission.objects.filter(missionname=dname)
        if exist[0].missionstate != "0000":
            return HttpResponse("<script>alert('Mission exists!');window.history.back(-1);</script>")
        else:
            if usertestdate == "" and phdate == "":
                m = Mission.objects.create(missionname=dname, missiontype=type, missionstate=state,
                                           missionlevel=level, usercompany=usercompany, username=username,
                                           usertel=usertel, remark=remark)
            elif usertestdate == "" and phdate != "":
                m = Mission.objects.create(missionname=dname, missiontype=type, missionstate=state,
                                           missionlevel=level, usercompany=usercompany, username=username,
                                           usertel=usertel, remark=remark, phdate=phdate)
            elif phdate == "" and usertestdate != "":
                m = Mission.objects.create(missionname=dname, missiontype=type, missionstate=state,
                                           missionlevel=level, usercompany=usercompany, username=username,
                                           usertel=usertel, remark=remark, usertestdate=usertestdate)
            else:
                m = Mission.objects.create(missionname=dname, missiontype=type, missionstate=state,
                                           missionlevel=level, usercompany=usercompany, username=username,
                                           usertel=usertel, remark=remark, usertestdate=usertestdate, phdate=phdate)
            # 插入日志表
            # uid = request.session['uid']
            # Log.objects.create(missionid=m.id, missionstate=m.missionstate, logerid=uid)
            return HttpResponse("<script>alert('Insert successfully!');window.history.back(-1);</script>")
    else:
        return render(request, "demand/404NotFound.html")


# @login_check
def update(request, no):
    '''
        需求更新
    :param request:
    :param no:
    :return:
    '''
    if request.method == "GET":
        no = int(no)
        try:
            query_demand = Mission.objects.filter(id=no)[0]  # 在数据库中查询地址栏传入的编号
        except Exception as e:
            print(e)
            return render(request, "demand/404NotFound.html")  # 如果不存在，说明编号错误，返回页面不存在
        else:
            if query_demand.missionstate != "0000":
                return render(request, "demand/update.html", locals())
            else:
                return render(request, "demand/404NotFound.html")  # 如果存在，但是已经被删除（非活跃状态），也返回错误页面
    elif request.method == "POST":
        dname = request.POST.get('dname')
        type = request.POST.get('hidden1')
        state = request.POST.get('hidden2')
        level = request.POST.get('hidden3')
        usercompany = request.POST.get('usercompany')
        username = request.POST.get('username')
        usertel = request.POST.get('usertel')
        remark = request.POST.get('remark')
        usertestdate = request.POST.get('usertestdate')
        phdate = request.POST.get('phdate')

        query_demand = Mission.objects.filter(id=no)[0]  # 从数据库中找出查询对象
        if not query_demand:
            return HttpResponse("<script>alert('Demand doesn\'t exist!');window.history.back(-1);</script>")
        if dname == query_demand.missionname and type == query_demand.missiontype and \
                level == query_demand.missionlevel and state == query_demand.missionstate and \
                usercompany == query_demand.usercompany and username == query_demand.username and \
                usertel == query_demand.usertel and remark == query_demand.remark and \
                usertestdate == query_demand.usertestdate and phdate == query_demand.phdate:
            return HttpResponse("<script>alert('No update!');window.history.back(-1);</script>")
        else:
            if dname != query_demand.missionname:
                query_demand.missionname = dname
            if type != query_demand.missiontype:
                query_demand.missiontype = type
            if level != query_demand.missionlevel:
                query_demand.missionlevel = level
            if state != query_demand.missionstate:
                query_demand.missionstate = state
            if usercompany != query_demand.usercompany:
                query_demand.usercompany = usercompany
            if username != query_demand.username:
                query_demand.username = username
            if usertel != query_demand.usertel:
                query_demand.usertel = usertel
            if remark != query_demand.remark:
                query_demand.remark = remark
            if usertestdate == "":
                query_demand.usertestdate = None
            if phdate == "":
                query_demand.phdate = None
            if usertestdate != "" and usertestdate != query_demand.usertestdate:
                query_demand.usertestdate = usertestdate
            if phdate != "" and phdate != query_demand.phdate:
                query_demand.phdate = phdate
            query_demand.save()
        # 插入日志表
        # uid = request.session['uid']
        # Log.objects.create(missionid=query_demand.id, missionstate=state, logerid=uid)
        return HttpResponse("<script>alert('Update successfully!');window.history.back(-1);</script>")
    else:
        return render(request, "demand/404NotFound.html")


# @login_check
@transaction.atomic
def upload(request):
    if request.method == "GET":
        return render(request, 'demand/upload.html')
    elif request.method == "PUT":
        cursor = connection.cursor()
        no = request.GET.get('no')
        print(no)
        if no == "":
            sql = 'select missionid_id,filename,uploader,uploaddate from file;'
            cursor.execute(sql)
            rawdata = cursor.fetchall()
            if not rawdata:
                return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
            result = []
            col_names = [desc[0] for desc in cursor.description]
            for r in rawdata:
                objdict = {}
                for k, v in enumerate(r):
                    objdict[col_names[k]] = v
                result.append(objdict)
            return JsonResponse({"code": 200, "data": result})
        elif no != "":
            sql = 'select missionid_id,filename,uploader,uploaddate from file where missionid_id=%s;' % no
            cursor.execute(sql)
            rawdata = cursor.fetchall()
            if not rawdata:
                return JsonResponse({"code": 1001, "data": {"message": "No such query result!"}})
            result = []
            col_names = [desc[0] for desc in cursor.description]
            for r in rawdata:
                objdict = {}
                for k, v in enumerate(r):
                    objdict[col_names[k]] = v
                result.append(objdict)
            return JsonResponse({"code": 200, "data": result})
    elif request.method == "POST":
        uploader = 1
        no = request.POST.get('no')
        print("no", no)
        # 处理用户上传的文件
        my_file = request.FILES['myfile']
        # 生成文件路径
        filename = os.path.join(settings.MEDIA_ROOT, my_file.name)
        with open(filename, 'wb') as f:
            data = my_file.file.read()
            f.write(data)
        try:
            m = Mission.objects.get(id=no)
            print("Query", m)
            File.objects.create(missionid_id=m.id, file=filename, filename=my_file.name, uploader=uploader)
        except Exception as e:
            print(e)
            return JsonResponse({"code": 1002, "data": {"message": "Failed to upload!"}})
        return HttpResponse(
            "<script>alert('Uploaded successfully! Filename: %s');window.history.back(-1);</script>" % my_file)
    else:
        return render(request, "demand/404NotFound.html")
