from django.shortcuts import render,redirect
from django.views.generic import  View
from app.models import *
from django.contrib.auth import login,logout
from common.makemd5 import make_md5
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import json,os,datetime
from django.http import HttpResponse,FileResponse
def file_down(request,filename):
    bashPath=os.getcwd()+'//testreport//'
    file_name = bashPath + filename
    def file_iterator(file_name, buf_size=8192):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(buf_size)
                if c:
                    yield c
                else:
                    break
    response = FileResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response
def write_intef_log(user,useip,userheader,userjiekou):
    if user=='':
        new_detail = JiekouDeail(useip=useip, userheaders=userheader, userjiekou=userjiekou)
        new_detail.save()
    new_detail=JiekouDeail(useuser=user,useip=useip,userheaders=userheader,userjiekou=userjiekou)
    new_detail.save()
class LoginView(View):
    def get(self,request):
        return  render(request, 'page/login.html')
    def post(self,request):
        request.session['login_from'] = request.META.get('next', '/home/')
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username=='':
            return render(request, 'page/login.html', {'msg': '用户名必须存在'})
        if password=="":
            return render(request, 'page/login.html', {'msg': '密码必须输入'})
        user=Newusers.objects.filter(username=username).first()
        if not  user:
            return render(request, 'page/login.html', {'msg': '用户不存在'})
        if check_password(password,user.password):
            if  user.status == False:
                request.session['username'] =username
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect(request.session['login_from'])
            return render(request, 'page/login.html', {'msg': '用户被锁定'})
        return  render(request, 'page/login.html', {'msg': '密码错误'})
class LogoutView(View):
    def get(self,request):
        try:
            del request.session['username']
            logout(request)
            messages.add_message(request, messages.INFO, '用户退出成功')
            return  redirect('login')
        except Exception as e:
            return redirect('home')
class IndexView(View):
    def get(self,request):
        m=datetime.datetime.now()
        meth=m.month
        day_s=m.day
        year=m.year
        test_report=Testreport.objects.filter(makedate__month=meth,makedate__day=day_s,makedate__year=year,status=False).all()
        jiekou_diaoyong=JiekouDeail.objects.filter(usedate__month=meth,usedate__day=day_s,usedate__year=year).all()
        project=Project.objects.filter(status=False).all().count()
        gongneng=FunctionalLofic.objects.filter(status=False,project__status=False).all().count()
        testcase=Testcase.objects.filter(status=False,luoji__status=False,project__status=False).all().count()
        return  render(request, 'page/index.html', {'project':project,  'testcase':testcase,
                                                    'gongneng':gongneng,'test_report':test_report,
                                                    'rizhi':jiekou_diaoyong})
class ProjectView(View):
    def get(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        return  render(request, 'page/project.html', {"projects":project_list})
    def post(self,request):
        project_one=request.body.decode('utf-8')
        project_one=json.loads(project_one)
        name=project_one['project']
        desc=project_one['desc']
        fenlei=project_one['fenlei']
        is_project = Project.objects.filter(name=name).first()
        if is_project:
            backe = {'code': 4, 'data': '项目不能重复'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        if len(desc) > 50:
            backe = {'code':5, 'data': '项目描述不要超过55个字'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        try:
            new_project = Project(name=name)
            new_project.makeuser = request.user
            new_project.fenlei = fenlei
            new_project.desc = desc
            new_project.save()
            backe = {'code': 2, 'data': '添加成功'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        except Exception as e:
            backe = {'code':3, 'data': '添加项目失败,原因是：%s'%e}
            return HttpResponse(json.dumps(backe), content_type="application/json")
    def put(self,request):
        project_one = request.body.decode('utf-8')
        project_one = json.loads(project_one)
        name = project_one['project']
        desc = project_one['desc']
        fenlei = project_one['fenlei']
        id=project_one['id']
        id_one=Project.objects.filter(id=id,status=False).first()
        if not id_one:
            addproecjt=Project(name=name,desc=desc,fenlei=fenlei)
            addproecjt.save()
            backe = {'code':2, 'data': '添加成功'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        else:
            id_one.name = name
            id_one.fenlei = fenlei
            id_one.desc = desc
            id_one.save()
            backe = {'code': 2, 'data': '编辑成功'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
    def delete(self,request):
        id=request.body.decode('utf-8')
        project = Project.objects.filter(id=id, status=False).first()
        if str(request.user.work) != '测试主管':
            backe={'code':1,'data':'权限不足'}
            return  HttpResponse(json.dumps(backe), content_type="application/json")
        if project:
            project.status = True
            project.save()
            backe = {'code': 2, 'data': '删除成功'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        backe = {'code': 3, 'data': '项目查询不到'}
        return HttpResponse(json.dumps(backe), content_type="application/json")
class ModelView(View):
    def get(self,request):
        models_list=Mode.objects.filter(status=False).all()
        return render(request,'page/model.html',{'models':models_list})
    def delete(self,request):
        id = request.body.decode('utf-8')
        model = Mode.objects.filter(id=id, status=False).first()
        if model:
            model.status = True
            model.save()
            back={'code':2,'data':'删除成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        back = {'code': 3, 'data': '删除失败，模块不存在'}
        return HttpResponse(json.dumps(back), content_type="application/json")
    def post(self,request):
        model_name = request.body.decode('utf-8')
        if len(model_name)<1:
            back = {'code':6, 'data': '添加模块失败,名称不能为空'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        is_model = Mode.objects.filter(name=model_name, status=False).first()
        if is_model:
            back = {'code': 5, 'data': '添加模块失败,模块已经存在'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        try:
            new_model = Mode(name=model_name)
            new_model.makeuser = request.user
            new_model.save()
            back = {'code':2, 'data': '添加模块成功' }
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code': 3, 'data': '添加模块失败，原因：%s'%e}
            return HttpResponse(json.dumps(back), content_type="application/json")
    def put(self,request):
        data=request.body.decode('utf-8')
        put_data=json.loads(data)
        id=put_data['id']
        name=put_data['name']
        id_is=Mode.objects.filter(id=id,status=False).first()
        if len(name)<=0:
            back = {'code': 4, 'data': '编辑模块名字不能为空'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        if not  id_is:
            new_mode=Mode(name=name)
            new_mode.save()
            back = {'code':3, 'data': '模块创建成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        id_is.name=name
        id_is.save()
        back = {'code': 2, 'data': '编辑模块成功'}
        return HttpResponse(json.dumps(back), content_type="application/json")
class TestEvevtView(View):
    def get(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        event_list=Testeven.objects.filter(status=False,projetc__status=False).all()
        return render(request,'page/testevent.html',{'events':event_list,'projects':project_list})
    def delete(self,request):
        id = request.body.decode('utf-8')
        try:
            delevent=Testeven.objects.get(status=False,id=id)
            delevent.status=True
            delevent.save()
            back = {'code': 2, 'data': '删除测试环境成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code': 1, 'data': '删除测试环境失败'}
            return HttpResponse(json.dumps(back), content_type="application/json")
    def post(self,request):
        data=request.body.decode('utf-8')
        testvent=json.loads(data)
        name=testvent['name']
        url=testvent['url']
        project=testvent['project']
        port=testvent['port']
        if not name:
            backe = {'code': 4, 'data': '添加测试环境失败，测试环境名称不能为空'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        if not url:
            backe = {'code': 4, 'data': '添加测试环境失败，没有测试环境地址'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        if not project or project =='':
            backe = {'code':4, 'data': '添加测试环境失败，没有选择项目'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        try:
            port=int(port)
        except:
            backe = {'code': 4, 'data': '添加测试环境失败，端口号必须是数字'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        try:
            prject=Project.objects.filter(name=project,status=False).first()
            testven=Testeven.objects.filter(projetc=prject,name=name,status=False,port_test=port).first()
            if testven:
                backe = {'code':6, 'data': '添加测试环境失败，测试环境存在'}
                return HttpResponse(json.dumps(backe), content_type="application/json")
            newtestevnt=Testeven(name=name,url_test=url,user=request.user,port_test=port)
            newtestevnt.projetc=prject
            newtestevnt.save()
            backe = {'code': 2, 'data': '添加测试环境成功'}
            return HttpResponse(json.dumps(backe), content_type="application/json")
        except Exception as e:
            backe = {'code':3, 'data': '添加测试环境出现异常，原因：%s'%e}
            return HttpResponse(json.dumps(backe), content_type="application/json")
    def put(self,request):
        data = request.body.decode('utf-8')
        testvent = json.loads(data)
        name = testvent['name']
        url = testvent['url']
        project = testvent['project']
        port = testvent['port']
        id=testvent['id']
        try:
            port=int(port)
        except:
            back = {'code':3, 'data': '端口号必须为数字'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        id_is=Testeven.objects.filter(id=id,status=False).first()
        projec=Project.objects.filter(name=project,status=False).first()
        if not  id_is:
            new=Testeven(user=request.user,name=name,url_test=url,port_test=port,projetc=projec)
            new.save()
            back = {'code': 2, 'data': '添加成功!'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        id_is.name=name
        id_is.url_test=url
        id_is.port_test=port
        id_is.projetc=projec
        id_is.user=request.user
        id_is.save()
        back = {'code':2, 'data': '编辑成功!'}
        return HttpResponse(json.dumps(back), content_type="application/json")
class UseradminView(View):
    def get(self,request):
        users=Newusers.objects.filter(status=False).all()
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        work=Work.objects.filter(status=False).all().order_by('id')
        return  render(request,'page/user.html',{'users':users,'works':work,"project_list":project_list})
    def delete(self,request):
        id = request.body.decode('utf-8')
        try:
            deluser=Newusers.objects.get(id=id,status=False)
            deluser.status=True
            deluser.save()
            back = {'code':2, 'data': '删除成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code': 3, 'data': '删除失败,原因：%s'%e}
            return HttpResponse(json.dumps(back), content_type="application/json")
    def post(self,request):
        data=request.body.decode('utf-8')
        json_data=json.loads(data)
        username=json_data['username']
        password=json_data['password']
        email=json_data['email']
        project=json_data['project']
        work=json_data['work']
        try:
            admin=json_data['admin']
            is_admin=True
        except:
            is_admin=False
        is_user = Newusers.objects.filter(username=username,status=False).first()
        work_is = Work.objects.filter(zhiwei=work).first()
        if not work_is:
            back = {'code':3, 'data': '添加失败,找不到选择的职位'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        if is_user:
            back = {'code': 3, 'data': '添加失败,用户已经存在'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        token = make_md5(username + work)
        try:
            user = Newusers(username=username)
            user.password = make_password(password)
            user.work = work_is
            user.email = email
            user.token = token
            user.save()
            for i in project:
                f = Project.objects.filter(name=i, status=False).first()
                user.project_user_set.create(username=user, is_guanliyuan=is_admin)
                m = Project_user.objects.filter(username=user).first()
                m.productname.add((f))
                m.save()
            back = {'code':2, 'data': '添加成功，请记住您的token:%s'%token}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code':3, 'data': '添加失败，原因:%s' %e}
            return HttpResponse(json.dumps(back), content_type="application/json")
    def put(self,request):
        data=(request.body.decode('utf-8'))
        json_data=json.loads(data)
        username = json_data['username']
        email = json_data['email']
        project = json_data['project']
        work = json_data['work']
        try:
            admin = json_data['admin']
            is_admin = True
        except:
            is_admin = False
        is_user = Newusers.objects.filter(username=username).first()
        work_is = Work.objects.filter(zhiwei=work).first()
        if not work_is:
            back = {'code': 3, 'data': '编辑失败,找不到选择的职位'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        try:
            is_user.work=work_is
            is_user.username = username
            is_user.email = email
            is_user.save()
            m = Project_user.objects.filter(username=is_user).first()
            m.productname.clear()
            for i in project:
                f = Project.objects.filter(name=i, status=False).first()
                is_user.project_user_set.update(username=is_user, is_guanliyuan=is_admin)
                m = Project_user.objects.filter(username=is_user).first()
                m.productname.add(f)
                m.save()
            back = {'code': 2, 'data': '编辑成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code':3, 'data': '编辑失败，原因:%s'%e}
            return HttpResponse(json.dumps(back), content_type="application/json")
class ResetUser(View):
    def get(self,request,id):
        user=Newusers.objects.filter(id=id,status=False).first()
        if not user:
            messages.add_message(request, messages.INFO, '你要重置的用户没有找到，请确认')
            return redirect('useradmin')
        try:
            user.password=make_password('111111')
            user.save()
            messages.add_message(request, messages.INFO, '密码重置成功，重置后的密码是：111111')
            return redirect('useradmin')
        except Exception as e:
            messages.add_message(request, messages.INFO, '重置密码失败！原因：%s'%e)
            return redirect('useradmin')
class TestCaseView(View):
    def get(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        return  render(request,'page/testyongli.html',{'projects':project_list})
    def post(self,request):
        project=request.body.decode('utf-8')
        allcase=Testcase.objects.filter(status=False,luoji__status=False,project__name=project,project__status=False).all()
        data_re=[]
        for i in allcase:
            if i.yilai == True:
                yilai='依赖'
            else:
                yilai='不依赖'
            data_re.append({'id':i.id,'casenum':i.casenum,'project':i.project.name,'yilai':yilai,
                            'data':i.data,'asser':i.asser,'functionname':i.luoji.functionname,'name':i.events.name,
                            'user':i.user.username})
        return_data={'code':1,'data':data_re}
        return  HttpResponse(json.dumps(return_data),content_type='application/json')
    def delete(self,request):
        id = request.body.decode('utf-8')
        case_is = Testcase.objects.filter(id=id, status=False).first()
        if not case_is:
            back = {'code': 1, 'data': '用例不存在，无法删除'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        try:
            case_is.status = True
            case_is.save()
            back = {'code': 2, 'data': '删除测试用例成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code':3, 'data': '删除测试用例失败，原因啊：%s'%e}
            return HttpResponse(json.dumps(back), content_type="application/json")
class TestCaseLuojiView(View):
    def get(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        return  render(request,'page/function.html',{'projects':project_list})
    def post(self,request):
        luoji_project=request.body.decode('utf-8')
        luoji=FunctionalLofic.objects.filter(project__name=luoji_project,status=False,project__status=False).all()
        data_return=[]
        for i in luoji:
            data_return.append({'project':i.project.name,'mode':i.mode.name,'functionname':i.functionname,
                                'desc':i.desc,'user':i.user.username,'id':i.id,'makedatye':str(i.makedatye.strftime("%Y-%m-%d"))})
        backe={'code':1,'data':data_return}
        return  HttpResponse(json.dumps(backe), content_type="application/json")
    def delete(self,request):
        id = request.body.decode('utf-8')
        try:
            is_function=FunctionalLofic.objects.get(id=id,status=False)
            is_function.status=True
            is_function.save()
            back = {'code': 2, 'data': '功能逻辑删除成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code': 3, 'data': '删除测试报告失败！原因：%s'%e}
            return HttpResponse(json.dumps(back), content_type="application/json")
class AddCaseView(View):
    def get(selfm,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        models=Mode.objects.filter(status=False).all()
        return  render(request,'add/addtescase.html',{'projects':project_list,'models':models})
    def post(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        models = Mode.objects.filter(status=False).all()
        project=request.POST.get('project')
        mode=request.POST.get('mode')
        testevent=request.POST.get('testevent')
        luoji=request.POST.get('luoji')
        case_num=request.POST.get('casenum')
        canshu=request.POST.get('canshu')
        yilai=request.POST.get('yilai')
        assertduan=request.POST.get('assert')
        result=request.POST.get('result')
        is_login=request.POST.get('login_is')
        if result=='on':
            result_is=True
        else:
            result_is=False
        if yilai=='on':
            yilai_is=True
        else:
            yilai_is=False
        if case_num=='':
            return render(request, 'add/addtescase.html', {'projects': project_list, 'models': models, "msg": '用例编号必须填写'})
        if canshu=='':
            return render(request, 'add/addtescase.html', {'projects': project_list, 'models': models, "msg": '用例参数必须填写'})
        if assertduan=="":
            return render(request, 'add/addtescase.html', {'projects': project_list, 'models': models, "msg": '用例断言必须填写'})
        project_one=Project.objects.filter(name=project,status=False).first()
        if not project_one:
            return render(request, 'add/addtescase.html', {'projects': project_list, 'models': models,"msg":'选择的项目不存在'})
        model_one=Mode.objects.filter(name=mode,status=False).first()
        if not model_one:
            return render(request, 'add/addtescase.html', {'projects': project_list, 'models': models, "msg": '选择的模块不存在'})
        luoji_one=FunctionalLofic.objects.filter(functionname=luoji,status=False).first()
        if not luoji_one:
            return render(request, 'add/addtescase.html', {'projects': project_list, 'models': models, "msg": '选择的逻辑不存在'})
        casenum=Testcase.objects.filter(casenum=case_num,project=project_one).first()
        if casenum:
            return render(request, 'add/addtescase.html', {'projects': project_list, 'models': models, "msg": '每个项目的用例编号应该是唯一的'})
        testevent_one=Testeven.objects.filter(name=testevent,projetc=project_one,status=False).first()
        if not  testevent_one:
            return render(request, 'add/addtescase.html',
                          {'projects': project_list, 'models': models, "msg": '请确定项目的测试环境是否真实存在'})
        if is_login=='on':
            is_log=True
            is_log_case = Testcase.objects.filter(project=project_one, events=testevent_one, is_yilai=True).first()
            if is_log_case:
                return render(request, 'add/addtescase.html',
                              {'projects': project_list, 'models': models, "msg": '一个测试项目的测试环境只能有一个作为登录的case'})
        else:
            is_log=False
        try:
            new_case=Testcase(project=project_one,mode=model_one,
                              user=request.user,casenum=case_num,
                              data=canshu,luoji=luoji_one,
                              yilai=yilai_is,asser=assertduan,
                              savetest=result_is,events=testevent_one,
                              is_yilai=is_log)
            new_case.save()
            messages.add_message(request, messages.INFO, '添加测试用例成功')
            return  redirect('testcase')
        except Exception as e:
            return render(request, 'add/addtescase.html', {'projects': project_list, 'models': models,'msg':'添加测试用例失败，原因：%s'%e})
class EditCaseView(View):
    def get(self,request,id):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        models = Mode.objects.filter(status=False).all()
        case_is=Testcase.objects.filter(id=id,status=False).first()
        if not  case_is:
            messages.add_message(request, messages.INFO, '编辑测试用例不存在')
            return  redirect('testcase')
        return render(request,'edit/edit_case.html',{'projects':project_list,'models':models,'case':case_is})
    def post(self,request,id):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        models = Mode.objects.filter(status=False).all()
        case_is = Testcase.objects.filter(id=id, status=False).first()
        project = request.POST.get('project')
        mode = request.POST.get('mode')
        testevent = request.POST.get('testevent')
        luoji = request.POST.get('luoji')
        case_num = request.POST.get('casenum')
        canshu = request.POST.get('canshu')
        yilai = request.POST.get('yilai')
        yi_is_login=request.POST.get('login_is')
        assertduan = request.POST.get('assert')
        result = request.POST.get('result')
        if yi_is_login=='on':
            yi_is_log=True
        else:
            yi_is_log=False
        if result == 'on':
            result_is = True
        else:
            result_is = False
        if yilai == 'on':
            yilai_is = True
        else:
            yilai_is = False
        if case_num == '':
            return render(request, 'edit/edit_case.html', {'projects': project_list, 'models': models, "msg": '用例编号必须填写','case':case_is})
        if canshu == '':
            return render(request, 'edit/edit_case.html', {'projects': project_list, 'models': models, "msg": '用例参数必须填写','case':case_is})
        if assertduan == "":
            return render(request, 'edit/edit_case.html', {'projects': project_list, 'models': models, "msg": '用例断言必须填写','case':case_is})
        project_one = Project.objects.filter(name=project, status=False).first()
        if not project_one:
            return render(request, 'edit/edit_case.html', {'projects': project_list, 'models': models, "msg": '选择的项目不存在','case':case_is})
        model_one = Mode.objects.filter(name=mode, status=False).first()
        if not model_one:
            return render(request, 'edit/edit_case.html', {'projects': project_list, 'models': models, "msg": '选择的模块不存在','case':case_is})
        luoji_one = FunctionalLofic.objects.filter(functionname=luoji, status=False).first()
        if not luoji_one:
            return render(request, 'edit/edit_case.html', {'projects': project_list, 'models': models, "msg": '选择的逻辑不存在','case':case_is})
        testevent_one = Testeven.objects.filter(name=testevent, projetc=project_one, status=False).first()
        if not testevent_one:
            return render(request, 'edit/edit_case.html',
                          {'projects': project_list, 'models': models, "msg": '请确定项目的测试环境是否真实存在','case':case_is})
        try:
            case_is.project=project_one
            case_is.mode=model_one
            case_is.casenum=case_num
            case_is.data=canshu
            case_is.luoji=luoji_one
            case_is.yilai=yilai_is
            case_is.is_yilai=yi_is_log
            case_is.asser=assertduan
            case_is.savetest=result_is
            case_is.events=testevent_one
            case_is.user=request.user
            case_is.save()
            messages.add_message(request, messages.INFO, '编辑测试用例成功')
            return redirect('testcase')
        except Exception as e:
            return render(request, 'edit/edit_case.html',
                          {'projects': project_list, 'models': models, 'msg': '编辑测试用例失败，原因：%s' % e,'case':case_is})
class AddFuntionsView(View):
    def get(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        models=Mode.objects.filter(status=False).all()
        return render(request,'add/addfuntions.html',{'projects':project_list,'models_list':models})
    def post(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        models = Mode.objects.filter(status=False).all()
        luojidesc=request.POST.get('desc')
        project=request.POST.get('projectid')
        name=request.POST.get('name')
        mode=request.POST.get('selmoduleid')
        buzhou_desc=request.POST.getlist('descr')
        elemnt_by=request.POST.getlist('keyword')
        dingwei=request.POST.getlist('autocomplete')
        index=request.POST.getlist('index')
        elsemt_id=request.POST.getlist('type')
        else_by_cao=request.POST.getlist('caozuo')
        danyan=request.POST.getlist('duanyan')
        canshu=request.POST.getlist('canshu')
        if name=='':
            return render(request, 'add/addfuntions.html',
                          {'projects': project_list, 'models_list': models, 'msg': '功能逻辑中的功能名称不能为空'})
        name_fun=FunctionalLofic.objects.filter(functionname=name,status=False).first()
        if name_fun:
            return render(request, 'add/addfuntions.html',
                          {'projects': project_list, 'models_list': models, 'msg': '功能名称必须唯一'})
        project_is=Project.objects.filter(name=project,status=False).first()
        if not project_is:
            return render(request, 'add/addfuntions.html', {'projects': project_list, 'models_list': models,'msg':'选择的项目不存在'})
        if mode!='所属模块':
            add_model=Mode.objects.filter(name=mode,status=False).first()
            if not  add_model:
                return render(request, 'add/addfuntions.html',
                              {'projects': project_list, 'models_list': models, 'msg': '选择的模块不存在'})
        else:
            add_model=None
        try:
            newfun=FunctionalLofic(project=project_is,mode=add_model)
            newfun.user=request.user
            newfun.desc=luojidesc
            newfun.functionname=name
            newfun.save()
            for i in range(len(else_by_cao)):
                if danyan[i]=='是':
                    duanyan=True
                else:
                    duanyan=False
                try:
                    index=int(index(i))
                except :
                    index=0
                esele=Function_element(desc=buzhou_desc[i],element_api=elsemt_id[i],function=newfun,element_ty=elemnt_by[i])
                esele.elemnet_by=dingwei[i]
                esele.caozuo=else_by_cao[i]
                esele.canshu=canshu[i]
                esele.is_asser=duanyan
                esele.index=index
                esele.xianhoui=i
                esele.user=request.user
                esele.save()
            messages.add_message(request, messages.INFO, '功能逻辑添加成功！')
            return redirect('testfaution')
        except Exception as e:
            return render(request, 'add/addfuntions.html', {'projects': project_list, 'models_list': models,'msg':'添加功能逻辑失败！原因：%s'%e})
class EditFuntionsView(View):
    def get(self,request,id):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        models = Mode.objects.filter(status=False).all()
        functions=FunctionalLofic.objects.filter(id=id,status=False).first()
        if not functions:
            messages.add_message(request, messages.INFO, '编辑功能逻辑不存在！')
            return  redirect('testfaution')
        function_luoji=Function_element.objects.filter(function=functions).all().order_by('id')
        return render(request,'edit/edit_funtion.html',{'functions':functions,'function_luoji':function_luoji,'projects':project_list,'models_list':models})
    def post(self,request,id):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        models = Mode.objects.filter(status=False).all()
        functions = FunctionalLofic.objects.filter(id=id, status=False).first()
        if not functions:
            messages.add_message(request, messages.INFO, '编辑功能逻辑不存在！')
            return redirect('testfaution')
        function_luoji = Function_element.objects.filter(function=functions).all().order_by('id')
        id_list=request.POST.getlist('id')
        luojidesc = request.POST.get('desc')
        project = request.POST.get('projectid')
        name = request.POST.get('name')
        mode = request.POST.get('selmoduleid')
        buzhou_desc = request.POST.getlist('descr')
        elemnt_by = request.POST.getlist('keyword')
        dingwei = request.POST.getlist('autocomplete')
        elsemt_id = request.POST.getlist('type')
        index=request.POST.getlist('index')
        else_by_cao = request.POST.getlist('caozuo')
        danyan = request.POST.getlist('duanyan')
        canshu = request.POST.getlist('canshu')
        if name == '':
            return render(request, 'edit/edit_funtion.html',
                          {'functions': functions, 'function_luoji': function_luoji, 'projects': project_list,
                           'models_list': models, 'msg': '编辑的逻辑的名字不能为空'})
        project_is = Project.objects.filter(name=project, status=False).first()
        if not project_is:
            return render(request, 'edit/edit_funtion.html',
                          {'functions': functions, 'function_luoji': function_luoji, 'projects': project_list,
                           'models_list': models, 'msg': '编辑的逻辑步骤选择的项目不存在'})
        if mode != '所属模块':
            add_model = Mode.objects.filter(name=mode, status=False).first()
            if not add_model:
                return render(request, 'edit/edit_funtion.html',
                              {'functions': functions, 'function_luoji': function_luoji, 'projects': project_list,
                               'models_list': models, 'msg': '选择的模块不存在'})
        else:
            add_model = None
        try:
            functions.project=project_is
            functions.mode=add_model
            functions.user = request.user
            functions.desc = luojidesc
            functions.functionname =name
            functions.save()
            for i in range(len(else_by_cao)):
                try:
                    indes=int(index[i])
                except:
                    indes=0
                if danyan[i]=='是':
                    duanyan=True
                else:
                    duanyan=False
                if id_list[i]==' ':
                    new=Function_element(desc=buzhou_desc[i],element_api=elsemt_id[i],
                                         function = functions,element_ty = elemnt_by[i],
                        elemnet_by = dingwei[i],caozuo = else_by_cao[i],canshu = canshu[i],
                     is_asser = duanyan,index = indes,xianhoui = i,user = request.user
                        )
                    new.save()
                else:
                    esele=Function_element.objects.filter(id=id_list[i],status=False).first()
                    if not  esele:
                        return render(request, 'edit/edit_funtion.html',
                                      {'functions': functions, 'function_luoji': function_luoji, 'projects': project_list,
                                       'models_list': models,'msg':'编辑的逻辑步骤不存在'})
                    esele.desc=buzhou_desc[i]
                    esele.element_api=elsemt_id[i]
                    esele.function=functions
                    esele.element_ty=elemnt_by[i]
                    esele.elemnet_by=dingwei[i]
                    esele.caozuo=else_by_cao[i]
                    esele.canshu=canshu[i]
                    esele.is_asser=duanyan
                    esele.index=indes
                    esele.xianhoui=i
                    esele.user=request.user
                    esele.save()
            messages.add_message(request, messages.INFO, '编辑成功！')
            return redirect('testfaution')
        except Exception as e:
            return render(request, 'edit/edit_funtion.html',
                          {'functions': functions, 'function_luoji': function_luoji, 'projects': project_list,
                           'models_list': models,'msg':'编辑失败！原因：%s'%e})
class TestReportView(View):
    def get(self, request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        return render(request, 'page/testreport.html', {'projects':project_list})
    def post(self,request):
        project_name=request.body.decode('utf-8')
        testreport=Testreport.objects.filter(project__name=project_name,status=False).all()
        data1=[]
        for i in testreport:
            data1.append({"project":i.project.name,'tatal':i.tatal,'passnum':i.passnum,'failnum':i.failnum,
                         'errornum':i.errornum,'testlog':i.testlog,'testrept':i.testrept,'testuser':i.testuser.username,
                         'id':i.id,'makedate':str(i.makedate.strftime("%Y-%m-%d"))})
        rebork_data={'code':1,'data':data1}
        return  HttpResponse(json.dumps(rebork_data), content_type="application/json")
    def delete(self,request):
        id = request.body.decode('utf-8')
        try:
            is_functi=Testreport.objects.filter(id=int(id),status=False).first()
            is_functi.status=True
            is_functi.save()
            back = {'code':2, 'data': '删除测试报告成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code': 3, 'data': '删除测试报告失败,原因：%s'%e}
            return HttpResponse(json.dumps(back), content_type="application/json")
class TingtaskViews(View):
    def get(self, request):
        testphons = Timmingtask.objects.filter(status=False).all()
        return render(request, 'page/timingtask.html', {'timingtasks': testphons})
    def delete(self,request):
        id = request.body.decode('utf-8')
        timing_is = Timmingtask.objects.filter(status=False, id=id).first()
        if not timing_is:
            back = {'code':3, 'data': '删除失败,定时任务找不到'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        try:
            timing_is.status = True
            timing_is.save()
            back = {'code': 2, 'data': '删除成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code': 4, 'data': '删除失败，原因：%s'%e}
            return HttpResponse(json.dumps(back), content_type="application/json")
class ChangepasswordView(View):
    def get(self,request):
        return  render(request,'changepassword.html')
    def post(self,request):
        yuanmami=request.POST.get('yuanmima')
        xinmima=request.POST.get('xinmima')
        quexinmima=request.POST.get('querenmima')
        if not  yuanmami:
            return render(request, 'changepassword.html',{'msg':'原密码不能为空'})
        if not xinmima:
            return render(request, 'changepassword.html', {'msg': '新密码不能为空'})
        if not  quexinmima:
            return render(request, 'changepassword.html', {'msg': '确认密码不能为空'})
        if xinmima!=quexinmima:
            return render(request, 'changepassword.html', {'msg': '新密码和确认密码不相等'})
        checkout=check_password(yuanmami,request.user.password,'utf-8')
        if checkout:
            if check_password(yuanmami,xinmima,'utf-8'):
                return render(request, 'changepassword.html', {'msg': '新密码不能和原密码一样'})
            try:
                user=Newusers.objects.get(username=request.user.username)
                user.password=make_password(xinmima)
                user.save()
                messages.add_message(request, messages.INFO, '密码修改成功')
                return redirect('login')
            except Exception as e:
                return render(request, 'changepassword.html', {'msg': '修改密码失败！原因：%s'%e})
        else:
            return  render(request,'changepassword.html',{'msg':'原密码错误'})
class Getevet(View):
    def post(self,request):
        proecj=request.body.decode('utf-8')
        proec_is=Project.objects.filter(name=proecj,status=False).first()
        if not proec_is:
            rquest={'code':100,'msg':'找不到请求的项目'}
            return HttpResponse(json.dumps(rquest), content_type="application/json")
        testevent=Testeven.objects.filter(projetc=proec_is,status=False).all()
        event=[]
        for i in range(len(testevent)):
            event.append({'testevent':testevent[i].name})
        luoji=FunctionalLofic.objects.filter(project=proec_is,status=False).all()
        luo_list=[]
        for luo in luoji:
            luo_list.append({'luoji':luo.functionname})
        event_luo=[]
        event_luo.append(event)
        event_luo.append(luo_list)
        rquest = {'code': 200, 'msg': '请求成功','data':event_luo}
        return HttpResponse(json.dumps(rquest), content_type="application/json")
class XingnengView(View):
    def get(self,request):
        xingnengs=Test_xing.objects.filter(testreport__status=False,status=False).all()
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        return render(request,'page/xingneng.html',{'xingnengs':xingnengs,'projects':project_list})
    def post(self,request):
        f=request.body.decode('utf-8')
        mdata=json.loads(f)
        project=mdata['project']
        funtions=mdata['funct']
        xingneng = Test_xing.objects.filter(status=False,testreport__project__name=project,functionluo__functionname=funtions,functionluo__status=False,functionluo__project__name=project,testreport__project__status=False,testreport__status=False).all()
        data = []
        for i in xingneng:
            data.append({'make_date': str(i.make_date.strftime("%Y-%m-%d")), 'user': i.user.username,
                         'testreport': i.testreport.testcallnum,
                         'cpu': i.cpu, 'neicun': i.neicun, 'shangxing': i.shangxing, 'xiaxing': i.xiaxing,
                         'shebei': i.shebei, 'fix': i.fix, 'xitongbanben': i.xitongbanben, 'pinpai': i.pinpai,
                         'xinghao': i.xinghao, 'id': i.id})
        rebckdata = {'code': 1, 'data': data}
        return  HttpResponse(json.dumps(rebckdata), content_type="application/json")
    def delete(self,request):
        id = request.body.decode('utf-8')
        xingneng_i = Test_xing.objects.filter(status=False, id=id).first()
        if not xingneng_i:
            back = {'code':1, 'data': '删除性能记录失败，因为性能记录不存在'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        try:
            xingneng_i.status = True
            xingneng_i.save()
            back = {'code': 2, 'data': '删除性能记录成功'}
            return HttpResponse(json.dumps(back), content_type="application/json")
        except Exception as e:
            back = {'code': 3, 'data': '删除性能记录失败，原因：%s'%e}
            return HttpResponse(json.dumps(back), content_type="application/json")
class Getcase(View):
    def post(self,request):
        proecj=request.body.decode('utf-8')
        proec_is=Project.objects.filter(name=proecj,status=False).first()
        if not proec_is:
            rquest={'code':100,'msg':'找不到请求的项目'}
            return HttpResponse(json.dumps(rquest), content_type="application/json")
        testevent=Testeven.objects.filter(projetc=proec_is,status=False).all()
        event=[]
        for i in range(len(testevent)):
            event.append({'testevent':testevent[i].name})
        rquest = {'code': 200, 'msg': '请求成功','data':event}
        return HttpResponse(json.dumps(rquest), content_type="application/json")
class Gettestcase(View):
    def post(self,request):
        post_data=request.body.decode('utf-8')
        project_name=json.loads(post_data)['project']
        venst_name=json.loads(post_data)['testvent']
        project=Project.objects.filter(name=str(project_name),status=False).first()
        if not project:
            rquest = {'code': 100, 'msg': '找不到请求的项目'}
            return HttpResponse(json.dumps(rquest), content_type="application/json")
        testevent=Testeven.objects.filter(name=venst_name,status=False).first()
        if not testevent:
            rquest = {'code': 100, 'msg': '找不到请求的测试环境'}
            return HttpResponse(json.dumps(rquest), content_type="application/json")
        case=Testcase.objects.filter(project=project,events=testevent,status=False).all()
        case_list = []
        for i in range(len(case)):
            case_list.append({'case': case[i].casenum})
        rquest = {'code': 200, 'msg': '请求成功', 'data': case_list}
        return HttpResponse(json.dumps(rquest), content_type="application/json")
class AddtimgView(View):
    def get(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        return render(request,'add/addtimgtask.html',{'projects':project_list})
    def post(self,request):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        project=request.POST.get('project')
        testvent=request.POST.get('testevent')
        cron=request.POST.get('cron')
        case=request.POST.getlist('case')
        name=request.POST.get('name')
        if name=='':
            return render(request, 'add/addtimgtask.html', {'projects': project_list, 'msg': '定时任务名称不能为空'})
        if cron=='':
            return render(request, 'add/addtimgtask.html', {'projects': project_list, 'msg': '定时任务cron表达式不能为空'})
        if len(case)<=0:
            return render(request, 'add/addtimgtask.html', {'projects': project_list,'msg':'定时任务必须有测试用例'})
        name_is=Timmingtask.objects.filter(name=name).first()
        if name_is:
            return render(request, 'add/addtimgtask.html', {'projects': project_list, 'msg': '定时任务名称不能重复'})
        pro_is=Project.objects.filter(name=project).first()
        testvent_is=Testeven.objects.filter(name=testvent).first()
        test_cas_list=[]
        for case_one in case:
            test_cas_list.append(Testcase.objects.filter(casenum=case_one).first())
        try:
            new_tim=Timmingtask(name=name,taskstart=cron,prject=pro_is,tesevent=testvent_is,makeuser=request.user,yunxing_status='创建')
            new_tim.save()
            new_tim.case.add(*test_cas_list)
            messages.add_message(request, messages.INFO, '添加定时任务成功' )
            return redirect('tingtask')
        except Exception as e:
            return render(request, 'add/addtimgtask.html', {'projects': project_list,'msg':'添加定时任务失败，原因:%s'%e})
class EdittaskView(View):
    def get(self,request,id):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        id_task=Timmingtask.objects.filter(id=id,status=False).first()
        if not id_task:
            messages.add_message(request,messages.INFO,'编辑的定时任务找不到')
            return  redirect('tingtask')
        return  render(request,'edit/edittiming.html',{'task':id_task,'projects':project_list})
    def post(self,request,id):
        if request.user.is_superuser is False:
            use=Newusers.objects.filter(username=request.user).first()
            m=use.project_user_set.all()
            project_list=[]
            for  i in m:
                project=i.productname.all()
                for j in project:
                    project_list.append(j)
        else:
            project_list = Project.objects.filter(status=False).all()
        id_task = Timmingtask.objects.filter(id=id, status=False).first()
        project = request.POST.get('project')
        testvent = request.POST.get('testevent')
        cron = request.POST.get('cron')
        case = request.POST.getlist('case')
        name = request.POST.get('name')
        if name == '':
            return render(request, 'edit/edittiming.html', {'task':id_task,'projects': project_list, 'msg': '定时任务名称不能为空'})
        if cron == '':
            return render(request, 'edit/edittiming.html', {'task':id_task,'projects': project_list, 'msg': '定时任务cron表达式不能为空'})
        pro_is = Project.objects.filter(name=project).first()
        testvent_is = Testeven.objects.filter(name=testvent).first()
        test_cas_list = []
        if len(case)<=0:
            for case_one in case:
                test_cas_list.append(Testcase.objects.filter(casenum=case_one).first())
        else:
            test_cas_list=[]
        try:
            id_task.name=name
            id_task.taskstart=cron
            id_task.prject=pro_is
            id_task.tesevent=testvent_is
            id_task.makeuser=request.user
            id_task.yunxing_status='创建'
            id_task.save()
            if len(test_cas_list)>=0:
                id_task.case.add(*test_cas_list)
            messages.add_message(request, messages.INFO, '编辑定时任务成功' )
            return redirect('tingtask')
        except Exception as e:
            return render(request, 'edit/edittiming.html', {'task': id_task, 'projects': project_list,'msg':'编辑定时任务失败！原因：%s'%e})
class GettaskView(View):
    def post(self,request):
        ipadder = (request.META.get('REMOTE_ADDR'))
        headers = (request.META.get('HTTP_USER_AGENT'))
        post_data=request.body.decode('utf-8')
        token=eval(post_data)['token']
        task = eval(post_data)['type']
        task_id=eval(post_data)['taskname']
        test_event=eval(post_data)['testevent']
        if task == ''  or token == '':
            write_intef_log(user=None, userjiekou='获取任务或项目的case相关数据', useip=ipadder, userheader=headers)
            rebckdata = {"code": 0, 'msg': '参数你都空着，验证当然失败', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        token_is=Newusers.objects.filter(token=token,status=False).first()
        if not token_is:
            write_intef_log(user=None, userjiekou='获取任务或项目的case相关数据', useip=ipadder, userheader=headers)
            rebckdata={"code":1,'msg':'您的权限校验失败，请检查token是否正确','data':''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        if task =='task':
            task_is = Timmingtask.objects.filter(name=task_id, status=False).first()
            if not task_is:
                write_intef_log(user=token_is, userjiekou='获取任务或项目的case相关数据', useip=ipadder, userheader=headers)
                rebckdata = {"code": 3, 'msg': '任务的名称查询不到', 'data': ''}
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            testcase = task_is.case.all()
            testevent = task_is.tesevent.name
            testprject = task_is.prject.name
        elif task =='project':
            project=Project.objects.filter(name=task_id,status=False).first()
            if not  project:
                rebckdata = {"code": 5, 'msg': '项目的名称查询不到', 'data': ''}
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            if test_event =="":
                write_intef_log(user=token_is, userjiekou='获取任务或项目的case相关数据', useip=ipadder, userheader=headers)
                rebckdata = {"code": 0, 'msg': '根据项目执行用例，但是你的测试环境不能为空', 'data': ''}
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            test_event_is=Testeven.objects.filter(name=test_event,status=False).first()
            if not test_event_is:
                write_intef_log(user=token_is, userjiekou='获取任务或项目的case相关数据', useip=ipadder, userheader=headers)
                rebckdata = {"code": 6, 'msg': '根据项目执行用例，但是你的测试环境查询不到', 'data': ''}
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            testprject=project.name
            testevent=test_event_is.name
            testcase=Testcase.objects.filter(project=project,events=test_event_is,status=False).all().order_by('id')
        else :
            write_intef_log(user=token_is, userjiekou='获取任务或项目的case相关数据', useip=ipadder, userheader=headers)
            rebckdata = {"code": 2, 'msg': '后台接口只针对任务,项目类型执行测试用例', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        casedetail=[]
        casedetail_is=[]
        casedetail_is.append({"project":testprject,'testevent':testevent})
        for case in testcase:
            function_luoji=[]
            function_name = FunctionalLofic.objects.filter(functionname=case.luoji.functionname, status=False).first()
            luoji = Function_element.objects.filter(function=function_name,status=False).all().order_by('id')
            for i in luoji:
                function_luoji.append({'element_api':i.element_api,'element_ty':i.element_ty,'elemnet_by':i.elemnet_by,
                                       'caozuo':i.caozuo,'canshu':i.canshu,'is_asser':i.is_asser,'index':i.index})
            case_detial={}
            case_detial['casenum']=case.casenum
            case_detial['data']=case.data
            case_detial['asser']=case.asser
            case_detial['yilai']=case.yilai
            case_detial['luoji']=function_luoji
            casedetail.append(case_detial)
        casedetail_is.append({'case':casedetail})
        rebckdata = {"code": 4, 'msg': '查询成功', 'data': casedetail_is}
        write_intef_log(user=token_is,userjiekou='获取任务或项目的case相关数据',useip=ipadder,userheader=headers)
        return HttpResponse(json.dumps(rebckdata), content_type="application/json")
class  Greatreport(View):
    def post(self,request):
        ipadder = (request.META.get('REMOTE_ADDR'))
        headers = (request.META.get('HTTP_USER_AGENT'))
        post_data = request.POST
        token = post_data.get('token')
        type_crea =post_data.get('type')
        task_id = post_data.get('taskname')
        test_event =post_data.get('testevent')
        testcallnum=post_data.get('testcallnum')
        passnum=post_data.get('passnum')
        failnum=post_data.get('failnum')
        errornum=post_data.get('errornum')
        if token =='':
            write_intef_log(user=None, userjiekou='创建测试报告接口', useip=ipadder, userheader=headers)
            rebckdata = {"code": 7, 'msg': 'token不能为空', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        if type_crea =='':
            write_intef_log(user=None, userjiekou='测试报告接口', useip=ipadder, userheader=headers)
            rebckdata = {"code":8, 'msg': '类型不能为空', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        token_is = Newusers.objects.filter(token=token, status=False).first()
        if not token_is:
            write_intef_log(user=token_is, userjiekou='测试报告接口', useip=ipadder, userheader=headers)
            rebckdata = {"code": 1, 'msg': '您的权限校验失败，请检查token是否正确', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        if type_crea=='task':
            task_is=Timmingtask.objects.filter(name=task_id,status=False).first()
            if not task_is:
                write_intef_log(user=token_is, userjiekou='测试报告接口', useip=ipadder, userheader=headers)
                rebckdata = {"code": 3, 'msg': '任务的名称查询不到', 'data': ''}
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            project=task_is.prject
            test_event_is=task_is.tesevent
        elif type_crea=='project':
            project = Project.objects.filter(name=task_id, status=False).first()
            if not project:
                write_intef_log(user=token_is, userjiekou='测试报告接口', useip=ipadder, userheader=headers)
                rebckdata = {"code": 5, 'msg': '项目的名称查询不到', 'data': ''}
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            if test_event == "":
                write_intef_log(user=token_is, userjiekou='测试报告接口', useip=ipadder, userheader=headers)
                rebckdata = {"code": 0, 'msg': '根据项目执行用例，但是你的测试环境不能为空', 'data': ''}
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            test_event_is = Testeven.objects.filter(name=test_event,status=False).first()
            if not test_event_is:
                write_intef_log(user=token_is, userjiekou='测试报告接口', useip=ipadder, userheader=headers)
                rebckdata = {"code": 6, 'msg': '根据项目执行用例，但是你的测试环境查询不到', 'data': ''}
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            task_is=None
        else:
            write_intef_log(user=token_is, userjiekou='测试报告接口', useip=ipadder, userheader=headers)
            rebckdata = {"code": 2, 'msg': '后台接口只针对任务,项目类型执行测试用例', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        if len(request.FILES )>0:
            testlog= request.FILES.get('testlog')
            testrept=request.FILES.get('testrept')
            file = os.getcwd() + '//testreport//' + testlog.name
            f = open(file, 'wb')
            if testlog.multiple_chunks() == False:
                for m in testlog.readlines():
                    f.write(m)
            else:
                for i in testlog.multiple_chunks():
                    f.write(i)
            f.close()
            fil = os.getcwd() + '//testreport//' + testrept.name
            wt = open(fil, 'wb')
            if testrept.multiple_chunks() == False:
                for m in testrept.readlines():
                    wt.write(m)
            else:
                for i in testrept.multiple_chunks():
                    wt.write(i)
            wt.close()
        else :
            testlog=None
            testrept=None
        try:
            passnum = int(passnum)
            failnum = int(failnum)
            errornum = int(errornum)
            total=passnum+failnum+errornum
        except:
            total=None
            passnum=None
            failnum=None
            errornum=None
        testcallnum_is=Testreport.objects.filter(testcallnum=testcallnum,project=project).first()
        if testcallnum_is:
            testcallnum_is.passnum=passnum
            testcallnum_is.failnum=failnum
            testcallnum_is.errornum=errornum
            testcallnum_is.testlog=testlog
            testcallnum_is.testrept=testrept
            testcallnum_is.tatal=total
            testcallnum_is.save()
            write_intef_log(user=token_is, userjiekou='测试报告接口', useip=ipadder, userheader=headers)
            rebckdata = {"code": 12, 'msg': '测试结果更新完毕', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        try:
            new_tes=Testreport(testcallnum=testcallnum,testuser=token_is,
                               project=project,testeven=test_event_is,
                               task=task_is,passnum=passnum,
                               failnum=failnum,errornum=errornum,
                               testhour=datetime.datetime.now(),
                               testlog=testlog,testrept=testrept,
                               tatal=total)
            new_tes.save()
            rebckdata = {"code": 4, 'msg': '创建成功!', 'data':testcallnum}
            write_intef_log(user=token_is, userjiekou='创建测试报告接口', useip=ipadder, userheader=headers)
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        except Exception as e:
            write_intef_log(user=token_is, userjiekou='创建测试报告接口', useip=ipadder, userheader=headers)
            rebckdata = {"code": 10, 'msg': '测试报告创建失败！原因:%s'%e, 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
class SendXing(View):
    def post(self,request):
        ipadder=(request.META.get('REMOTE_ADDR'))
        headers=(request.META.get('HTTP_USER_AGENT'))
        post_data = request.POST
        token = post_data.get('token')
        testcallnum=(post_data).get('testcallnum')
        cpulist=(post_data).getlist('cpulist')
        neicunlist=post_data.getlist('neicunlist')
        casenumlist=post_data.getlist('casenum')
        shangchhuan=post_data.getlist('shangchhuan')
        xiazailist=post_data.getlist('xiazailist')
        shebei=(post_data).get('shebei')
        jihe=(post_data).get('jihe')
        fix=(post_data).get('fix')
        xitongbanben=(post_data).get('xitongbanben')
        xinghao=(post_data).get('xinghao')
        pinpai=(post_data).get('pinpai')
        token_is = Newusers.objects.filter(token=token, status=False).first()
        if not token_is:
            write_intef_log(user=token_is, userjiekou='写入性能结果接口', useip=ipadder, userheader=headers)
            rebckdata = {"code": 1, 'msg': '您的权限校验失败，请检查token是否正确', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        testcallnum_i=Testreport.objects.filter(testcallnum=testcallnum).first()
        if not testcallnum_i:
            write_intef_log(user=token_is, userjiekou='写入性能结果接口', useip=ipadder, userheader=headers)
            rebckdata = {"code": 10, 'msg': '请确认你的测试报告编号是否存在或者以及删除', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        cpulist=list(cpulist)
        neicunlist=list(neicunlist)
        shangchhuan=list(shangchhuan)
        xiazailist=list(xiazailist)
        casenum_lis=list(casenumlist)
        try:
            if len(cpulist)<=0:
                new_testxing = Test_xing(testreport=testcallnum_i, user=token_is, shebei=shebei,
                                         jihe=jihe, fix=fix, xitongbanben=xitongbanben, xinghao=xinghao,
                                         pinpai=pinpai)
                new_testxing.save()
                rebckdata = {"code": 5, 'msg': '写入性能结果,没有记录性能数据，没有收集到', 'data': ''}
                write_intef_log(user=token_is, userjiekou='写入性能结果接口', useip=ipadder, userheader=headers)
                return HttpResponse(json.dumps(rebckdata), content_type="application/json")
            for i in range(len(cpulist)):
                function_one=FunctionalLofic.objects.filter(testcase__casenum=casenum_lis[i],status=False).first()
                new_testxing=Test_xing(testreport=testcallnum_i,user=token_is,shebei=shebei,
                                       jihe=jihe,fix=fix,xitongbanben=xitongbanben,xinghao=xinghao,
                                       pinpai=pinpai,cpu=cpulist[i],neicun=neicunlist[i],shangxing=shangchhuan[i],
                                       xiaxing=xiazailist[i],functionluo=function_one)
                new_testxing.save()
            rebckdata = {"code": 4, 'msg': '写入性能结果', 'data':''}
            write_intef_log(user=token_is, userjiekou='写入性能结果接口', useip=ipadder, userheader=headers)
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        except Exception as  e:
            rebckdata = {"code": 12, 'msg': '写入性能结果！原因：%s'%e, 'data': ''}
            write_intef_log(user=token_is, userjiekou='写入性能结果接口', useip=ipadder, userheader=headers)
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
class YiLaiLogin(View):
    def post(self,request):
        ipadder = (request.META.get('REMOTE_ADDR'))
        headers = (request.META.get('HTTP_USER_AGENT'))
        post_data = request.body.decode('utf-8')
        testcallnum = eval(post_data)['testcallnum']
        project=eval(post_data)['project']
        testevnt=eval(post_data)['testevet']
        token = eval(post_data)['token']
        token_is=Newusers.objects.filter(token=token,status=False).first()
        project_is=Project.objects.filter(name=project,status=False).first()
        function_de=FunctionalLofic.objects.filter(functionname='登录',project=project_is,status=False).first()
        testevnt_is=Testeven.objects.filter(name=testevnt,projetc=project_is,status=False).first()
        testcae_is=Testcase.objects.filter(project=project_is,events=testevnt_is,is_yilai=True).first()
        if not testcae_is:
            write_intef_log(user=None, userjiekou='获取任务或项目的case依赖登录相关数据', useip=ipadder, userheader=headers)
            rebckdata = {"code": 12, 'msg': '没有找到你项目中可以依赖的登录case相关逻辑', 'data': ''}
            return HttpResponse(json.dumps(rebckdata), content_type="application/json")
        function_luoji = []
        function_name = FunctionalLofic.objects.filter(functionname=testcae_is.luoji.functionname, status=False).first()
        luoji = Function_element.objects.filter(function=function_name, status=False).all().order_by('id')
        for i in luoji:
            function_luoji.append({'element_api': i.element_api, 'element_ty': i.element_ty, 'elemnet_by': i.elemnet_by,
                                   'caozuo': i.caozuo, 'canshu': i.canshu, 'is_asser': i.is_asser, 'index': i.index})
        case_detial = {}
        casedetail = []
        case_detial['casenum'] = testcae_is.casenum
        case_detial['data'] = testcae_is.data
        case_detial['asser'] = testcae_is.asser
        case_detial['yilai'] = testcae_is.yilai
        case_detial['luoji'] = function_luoji
        casedetail.append(case_detial)
        rebckdata = {"code": 4, 'msg': '查询成功', 'data': casedetail}
        write_intef_log(user=token_is, userjiekou='获取任务或项目的case相关数据', useip=ipadder, userheader=headers)
        return HttpResponse(json.dumps(rebckdata), content_type="application/json")
class Huoqufun(View):
    def post(self,request):
        projetc=request.body.decode('utf-8')
        function_all=FunctionalLofic.objects.filter(project__name=projetc,status=False).all()
        data=[]
        for fun in function_all:
            data.append({'funtioname':fun.functionname})
        rebckdata = {'code': 1, 'data': data}
        return HttpResponse(json.dumps(rebckdata), content_type="application/json")