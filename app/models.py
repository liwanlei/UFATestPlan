from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
class Work(models.Model):
    makedate = models.DateTimeField('创建时间', auto_now_add=True)
    zhiwei=models.CharField('职位',max_length=32)
    status=models.BooleanField('是否删除',default=False)
    class Meta:
        verbose_name = u'工作'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return self.zhiwei
class Newusers(AbstractUser):
    qq=models.IntegerField('qq',blank=True,null=True,unique=True)
    mobile=models.IntegerField('手机号',null=True,unique=True,blank=True)
    login_lock=models.BooleanField('是否锁定',default=False)
    status=models.BooleanField('状态',default=False)
    work=models.ForeignKey(Work,null=True,on_delete=models.CASCADE)
    token=models.CharField('token',max_length=252,null=True)
    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.username)
class Project(models.Model):
    type=(
    ('app','app'),
    ('web','web')
    )
    name=models.CharField('名称',max_length=32)
    desc=models.CharField('简介',max_length=255,null=True)
    makedate = models.DateTimeField('创建时间', auto_now_add=True)
    status=models.BooleanField('状态',default=False)
    fenlei=models.CharField('类型',choices=type,null=True,max_length=8)

    #项目类型，默认是安卓。也可以是ios 或者 web
    proeject=models.CharField('项目类型',null=True,max_length=8,default="android")

    change_time=models.DateTimeField('更新时间',auto_now_add=True)
    makeuser=models.ForeignKey(Newusers,null=True,on_delete=models.CASCADE)
    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return self.name
class Project_user(models.Model):
    username = models.ForeignKey(Newusers,on_delete=models.CASCADE)
    productname = models.ManyToManyField(Project,null=True)
    is_guanliyuan=models.BooleanField('项目管理员',default=False)
class Mode(models.Model):
    makedate = models.DateTimeField('创建时间',auto_now_add=True)
    name = models.CharField('名称', max_length=32)
    status = models.BooleanField('状态', default=False)
    makeuser = models.ForeignKey(Newusers,on_delete=models.CASCADE)
    project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.CASCADE)
    class Meta:
        verbose_name = u'模块'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return self.name
class FunctionalLofic(models.Model):
    makedatye=models.DateTimeField('创建时间',auto_now_add=True)
    user=models.ForeignKey(Newusers,on_delete=models.CASCADE)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    mode=models.ForeignKey(Mode,null=True,on_delete=models.CASCADE)
    desc=models.CharField('功能描述',max_length=252)
    functionname=models.CharField('功能名称',max_length=16,null=True)
    status=models.BooleanField('状态',default=False)
    update=models.CharField('更新人',null=True,max_length=8)
    update_time=models.DateTimeField('更新时间',default=datetime.datetime.now())
    class Meta:
        verbose_name = u'功能'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)
class Function_element(models.Model):
    S_CHOICES = (('click','click'),('sendkeys','sendkeys'))
    Element_Choice = (('id','id'),
                      ('name','name'),('css_selector','css selector'),
                      ('xpath','xpath'),('class_name','class name'),
                      ('tag_name','tag name'),
                      ('link_text','link text'),
                      ('portial_link_text','portial link text'))
    makedatye=models.DateTimeField('创建时间',auto_now_add=True)
    desc=models.CharField('步骤描述',max_length=252,null=True)
    user=models.ForeignKey(Newusers,null=True,on_delete=models.CASCADE)
    function=models.ForeignKey(FunctionalLofic,null=True,on_delete=models.CASCADE)
    element_api=models.CharField('定位api',max_length=8)
    index=models.IntegerField('索引',default=0,null=True)
    element_ty=models.CharField('定位的类型',choices=Element_Choice,max_length=32,null=True)
    elemnet_by=models.CharField('定位',max_length=252,null=True)
    caozuo=models.CharField('操作',choices=S_CHOICES,max_length=32,null=True)
    canshu=models.CharField('参数',null=True,max_length=252)
    is_asser=models.BooleanField('是否是断言',default=False)
    xianhoui=models.IntegerField('先后顺序',default=0)
    status=models.BooleanField('状态',default=False)
    class Meta:
        verbose_name = u'逻辑'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)
class Testeven(models.Model):
    projetc=models.ForeignKey(Project,on_delete=models.CASCADE)
    user=models.ForeignKey(Newusers,on_delete=models.CASCADE)
    makedate = models.DateTimeField('创建时间', auto_now_add=True)
    status=models.BooleanField('状态',default=False)
    name=models.CharField('测试环境名字',max_length=252,default='开发环境')
    url_test=models.CharField('url',max_length=252)
    port_test=models.IntegerField('port',default=80)
    class Meta:
        verbose_name = u'测试环境'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)
class Testcase(models.Model):
    makedate = models.DateTimeField('创建时间', auto_now_add=True)
    project=models.ForeignKey(Project,null=True,on_delete=models.CASCADE)
    mode=models.ForeignKey(Mode,null=True,on_delete=models.CASCADE)
    user=models.ForeignKey(Newusers,on_delete=models.CASCADE)
    casenum=models.CharField('测试用例编号',default=1,unique=True,max_length=252)
    data=models.CharField('参数',max_length=252)
    yilai=models.BooleanField('是否依赖登录',default=False)
    is_yilai=models.BooleanField('是否作为项目登录的依赖',default=False)
    asser=models.CharField('预期',max_length=252)
    luoji=models.ForeignKey(FunctionalLofic,on_delete=models.CASCADE)
    savetest=models.BooleanField('是否保存测试结果',default=False)
    events=models.ForeignKey(Testeven,on_delete=models.CASCADE)
    status = models.BooleanField('状态', default=False)
    class Meta:
        verbose_name = u'测试用例'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)
class Timmingtask(models.Model):
    name=models.CharField('定时任务名字',max_length=64)
    makeuser = models.ForeignKey(Newusers,on_delete=models.CASCADE) # 创建者
    taskstart = models.CharField('任务执行时间',max_length=64)  # 任务执行时间
    tasktyped=models.CharField("任务类型",max_length=32,default='一次性任务')
    casetype=models.CharField("用例类型",max_length=32,default="UIcase")
    taskmakedate = models.DateTimeField('创建时间', auto_now_add=True)  # 任务的创建时间
    tesevent=models.ForeignKey(Testeven,on_delete=models.CASCADE)
    apkfilepath=models.CharField("测试apk路径",max_length=32)
    taskiphonetype = models.CharField('任务设备类型', default="android", max_length=8)
    taskiphonenum = models.IntegerField('任务设备的数量',  max_length=8,default=1)
    status = models.BooleanField('任务状态', default=False)  # 任务状态，默认正常状态
    yunxing_status = models.CharField('任务的运行状态，',max_length=16, default=u'创建')  # 任务的运行状态，默认是创建
    prject = models.ForeignKey(Project,on_delete=models.CASCADE)  # 任务所属的项目
    case=models.ManyToManyField('Testcase')
    class Meta:
        verbose_name = u'定时任务'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)
class Casetestresult(models.Model):
    user = models.ForeignKey(Newusers,on_delete=models.CASCADE)
    events = models.ForeignKey(Testeven,on_delete=models.CASCADE)
    case=models.ForeignKey(Testcase,on_delete=models.CASCADE)
    status=models.BooleanField('状态',default=False)
    makedate = models.DateTimeField('时间', auto_now_add=True)
    testreport=models.CharField('测试结果',max_length=252)
    class Meta:
        verbose_name = u'测试结果'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)
class Testreport(models.Model):
    project=models.ForeignKey(Project,null=True,on_delete=models.CASCADE)
    mode=models.ForeignKey(Mode,null=True,on_delete=models.CASCADE)
    task=models.ForeignKey(Timmingtask,null=True,on_delete=models.CASCADE)
    testeven=models.ForeignKey(Testeven,null=True,on_delete=models.CASCADE)
    testcallnum=models.CharField('测试报告编号',max_length=252)
    tatal=models.IntegerField('总计')
    passnum=models.IntegerField('通过',null=True,blank=True)
    failnum=models.IntegerField('失败',null=True,blank=True)
    errornum=models.IntegerField('错误',null=True,blank=True)
    testhour=models.DateTimeField('测试耗时',null=True,blank=True)
    testuser=models.ForeignKey(Newusers,on_delete=models.CASCADE)
    makedate = models.DateTimeField('创建时间',auto_now_add=True)
    testlog=models.FilePathField('测试日志',path='/testreport/',null=True)
    testrept=models.FilePathField('测试报告',path='/testreport/',null=True)
    status=models.BooleanField('状态',default=False)
    class Meta:
        verbose_name = u'测试报告'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)
class Test_xing(models.Model):
    testreport=models.ForeignKey(Testreport,on_delete=models.CASCADE)
    cpu=models.CharField('CPU',null=True,max_length=16)
    neicun=models.CharField('内存',null=True,max_length=16)
    shangxing=models.CharField('上传流量',null=True,max_length=16)
    xiaxing=models.CharField('下行流量',null=True,max_length=16)
    user=models.ForeignKey(Newusers,on_delete=models.CASCADE)
    functionluo=models.ForeignKey(FunctionalLofic,on_delete=models.CASCADE,null=True)
    make_date=models.DateTimeField('创建时间',auto_now_add=True)
    shebei=models.CharField('设备',max_length=16)
    jihe=models.CharField('几核CPU',max_length=8,null=True)
    fix=models.CharField('分辨率',max_length=8,null=True)
    xitongbanben=models.CharField('系统版本',max_length=8,null=True)
    xinghao=models.CharField('型号',max_length=8,null=True)
    pinpai=models.CharField('品牌',max_length=8,null=True)
    status=models.BooleanField('状态',default=False)
    class Meta:
        verbose_name = u'测试性能'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)
class JiekouDeail(models.Model):
    useuser=models.CharField('使用',null=True,max_length=64)
    usedate=models.DateTimeField('调用时间',auto_now_add=True)
    useip=models.CharField('调用者ip',max_length=252)
    userheaders=models.CharField('调用者请求头',max_length=252)
    userjiekou=models.CharField('调用接口',max_length=252)
    class Meta:
        verbose_name = u'接口调用'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __str__(self):
        return str(self.id)

#任务列表
class TaskList(models.Model):
    '''待做任务列表
    1.多用例
    2.定时任务
    '''
    #ture 删除 False 正常
    status = models.BooleanField('状态', default=False)

    #默认状态0 创建，1执行中，2执行失败，3执行完毕 4.暂停
    tasktype=models.IntegerField('任务状态',null=True,blank=True,default=0)

    #任务的类型 默认andoid
    taskiphonetype=models.CharField('任务设备',default="android",max_length=8)

    #所属项目
    project = models.IntegerField('所属项目', null=False, blank=True)

    #执行设备数
    runphonenum = models.IntegerField('执行设备数', null=True, blank=True, default=1)

    #是否收集性能数据
    iscollectperformncedata=models.BooleanField('是否收集性能数据', default=True)


    #任务的类型  0 定时任务 1 测试用例
    tasklisttype= models.IntegerField('任务列表的类型', null=False, blank=True,default=0)

    class Meta:
        verbose_name = u'任务列表'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return str(self.id)


#任务的case表格
class  TasklistCase(models.Model):
    status = models.BooleanField('状态', default=False)
    task = models.IntegerField('执行任务', null=True, blank=True)
    caserun = models.IntegerField('执行caseID', null=True, blank=True)


    class Meta:
            verbose_name = u'任务用例表'
            verbose_name_plural = verbose_name
            ordering = ['-id']

    def __str__(self):
        return str(self.id)


#任务的定时任务关系表
class  TasklistTask(models.Model):

    #状态
    status = models.BooleanField('状态', default=False)

    #任务id
    task=models.IntegerField('执行任务', null=True, blank=True)

    #要执行的定时任务
    taskrun = models.IntegerField('执行任务ID', null=True, blank=True)

    class Meta:
        verbose_name = u'任务定时任务表'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return str(self.id)