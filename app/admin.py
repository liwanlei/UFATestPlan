from common import  xadmin
from app.models import *
from xadmin import views
class GlobalSetting(object):
    site_title = "app自动化后台管理系统"
    site_footer = "雷子"
class workAdmin(object):
    list_display = ('makedate', 'zhiwei')
    save_on_top = True
class ProjectAdmin(object):
    list_display = ('name', 'makedate','makeuser','change_time')
    save_on_top = True
class modelAdmin(object):
    list_display = ('name', 'makedate','status','makeuser','project')
    save_on_top = True
class FunctionalLoficadmin(object):
    list_display = ('project', 'mode', 'desc', 'functionname', 'user')
    save_on_top = True
class Function_elementadmin(object):
    list_display = ('function', 'element_api', 'element_ty', 'elemnet_by', 'caozuo')
    save_on_top = True
class Testxingadmin(object):
    list_display = ('testreport', 'cpu', 'neicun', 'shangxing', 'xiaxing','shebei','jihe','fix','xitongbanben')
    save_on_top = True
class Testreportadmin(object):
    list_display = ('project', 'mode', 'task', 'testeven', 'passnum','failnum','errornum','testlog','testrept')
    save_on_top = True
class TestcaseAdmin(object):
    list_display = ('luoji', 'project','data','asser')
    save_on_top = True
class TestevenAdmin(object):
    list_display = ('projetc', 'name','url_test','user')
    save_on_top = True
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(Work,workAdmin)
xadmin.site.register(Project,ProjectAdmin)
xadmin.site.register(Mode,modelAdmin)
xadmin.site.register(Timmingtask)
xadmin.site.register(Testeven,TestevenAdmin)
xadmin.site.register(Testcase,TestcaseAdmin)
xadmin.site.register(Testreport,Testreportadmin)
xadmin.site.register(FunctionalLofic,FunctionalLoficadmin)
xadmin.site.register(Casetestresult)
xadmin.site.register(Function_element,Function_elementadmin)
xadmin.site.register(Test_xing,Testxingadmin)