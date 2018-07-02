# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newusers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', max_length=30, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('qq', models.IntegerField(verbose_name='qq', unique=True, blank=True, null=True)),
                ('mobile', models.IntegerField(verbose_name='手机号', unique=True, blank=True, null=True)),
                ('login_lock', models.BooleanField(verbose_name='是否锁定', default=False)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('token', models.CharField(verbose_name='token', max_length=252, null=True)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Casetestresult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('makedate', models.DateTimeField(verbose_name='时间', auto_now_add=True)),
                ('testreport', models.CharField(verbose_name='测试结果', max_length=252)),
            ],
            options={
                'verbose_name': '测试结果',
                'verbose_name_plural': '测试结果',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Function_element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('makedatye', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('desc', models.CharField(verbose_name='步骤描述', max_length=252, null=True)),
                ('element_api', models.CharField(verbose_name='定位api', max_length=8)),
                ('index', models.IntegerField(verbose_name='索引', null=True, default=0)),
                ('element_ty', models.CharField(verbose_name='定位的类型', max_length=32, null=True, choices=[('id', 'id'), ('name', 'name'), ('css_selector', 'css selector'), ('xpath', 'xpath'), ('class_name', 'class name'), ('tag_name', 'tag name'), ('link_text', 'link text'), ('portial_link_text', 'portial link text')])),
                ('elemnet_by', models.CharField(verbose_name='定位', max_length=252, null=True)),
                ('caozuo', models.CharField(verbose_name='操作', max_length=32, null=True, choices=[('click', 'click'), ('sendkeys', 'sendkeys')])),
                ('canshu', models.CharField(verbose_name='参数', max_length=252, null=True)),
                ('is_asser', models.BooleanField(verbose_name='是否是断言', default=False)),
                ('xianhoui', models.IntegerField(verbose_name='先后顺序', default=0)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('creat', models.CharField(verbose_name='创建人', max_length=16, null=True)),
                ('upade', models.CharField(verbose_name='更新人', max_length=16, null=True)),
                ('upadetime', models.DateTimeField(verbose_name='更新时间', default=datetime.datetime(2018, 5, 9, 20, 15, 50, 132215))),
            ],
            options={
                'verbose_name': '逻辑',
                'verbose_name_plural': '逻辑',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FunctionalLofic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('makedatye', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('desc', models.CharField(verbose_name='功能描述', max_length=252)),
                ('functionname', models.CharField(verbose_name='功能名称', max_length=16, null=True)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('update', models.CharField(verbose_name='更新人', max_length=8, null=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', default=datetime.datetime(2018, 5, 9, 20, 15, 50, 130215))),
            ],
            options={
                'verbose_name': '功能',
                'verbose_name_plural': '功能',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='JiekouDeail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('usedate', models.DateTimeField(verbose_name='调用时间', auto_now_add=True)),
                ('useip', models.CharField(verbose_name='调用者ip', max_length=252)),
                ('userheaders', models.CharField(verbose_name='调用者请求头', max_length=252)),
                ('userjiekou', models.CharField(verbose_name='调用接口', max_length=252)),
                ('useuser', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '接口调用',
                'verbose_name_plural': '接口调用',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('makedate', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('name', models.CharField(verbose_name='名称', max_length=32)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('makeuser', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '模块',
                'verbose_name_plural': '模块',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='名称', max_length=32)),
                ('makedate', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('fenlei', models.CharField(verbose_name='类型', max_length=8, null=True, choices=[('app', 'app'), ('web', 'web')])),
                ('change_time', models.DateTimeField(verbose_name='更新时间', auto_now_add=True)),
                ('makeuser', models.CharField(verbose_name='创建人', max_length=16, null=True)),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Project_user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_guanliyuan', models.BooleanField(verbose_name='项目管理员', default=False)),
                ('productname', models.ForeignKey(on_delete=None, to='app.Project')),
                ('username', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test_xing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('cpu', models.CharField(verbose_name='CPU', max_length=16, null=True)),
                ('neicun', models.CharField(verbose_name='内存', max_length=16, null=True)),
                ('shangxing', models.CharField(verbose_name='上传流量', max_length=16, null=True)),
                ('xiaxing', models.CharField(verbose_name='下行流量', max_length=16, null=True)),
                ('make_date', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('shebei', models.CharField(verbose_name='设备', max_length=16)),
                ('jihe', models.CharField(verbose_name='几核CPU', max_length=8, null=True)),
                ('fix', models.CharField(verbose_name='分辨率', max_length=8, null=True)),
                ('xitongbanben', models.CharField(verbose_name='系统版本', max_length=8, null=True)),
                ('xinghao', models.CharField(verbose_name='型号', max_length=8, null=True)),
                ('pinpai', models.CharField(verbose_name='品牌', max_length=8, null=True)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
            ],
            options={
                'verbose_name': '测试性能',
                'verbose_name_plural': '测试性能',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('makedate', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('casenum', models.CharField(verbose_name='测试用例编号', max_length=252, unique=True, default=1)),
                ('data', models.CharField(verbose_name='参数', max_length=252)),
                ('yilai', models.BooleanField(verbose_name='是否依赖', default=False)),
                ('pid', models.CharField(max_length=128, blank=True, null=True)),
                ('yi_case', models.CharField(verbose_name='依赖参数', max_length=32, null=True)),
                ('asser', models.CharField(verbose_name='预期', max_length=252)),
                ('savetest', models.BooleanField(verbose_name='是否保存测试结果', default=False)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
            ],
            options={
                'verbose_name': '测试用例',
                'verbose_name_plural': '测试用例',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Testeven',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('makedate', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('name', models.CharField(verbose_name='测试环境名字', max_length=252, default='开发环境')),
                ('url_test', models.CharField(verbose_name='url', max_length=252)),
                ('port_test', models.IntegerField(verbose_name='port', default=80)),
                ('projetc', models.ForeignKey(on_delete=None, to='app.Project')),
                ('user', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '测试环境',
                'verbose_name_plural': '测试环境',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Testreport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('testcallnum', models.CharField(verbose_name='测试报告编号', max_length=252)),
                ('tatal', models.IntegerField(verbose_name='总计')),
                ('passnum', models.IntegerField(verbose_name='通过', blank=True, null=True)),
                ('failnum', models.IntegerField(verbose_name='失败', blank=True, null=True)),
                ('errornum', models.IntegerField(verbose_name='错误', blank=True, null=True)),
                ('exceonum', models.IntegerField(verbose_name='异常', blank=True, null=True)),
                ('testhour', models.DateTimeField(verbose_name='测试耗时', blank=True, null=True)),
                ('makedate', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('testlog', models.FilePathField(verbose_name='测试日志', null=True, path='/testreport/')),
                ('testrept', models.FilePathField(verbose_name='测试报告', null=True, path='/testreport/')),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('mode', models.ForeignKey(null=True, on_delete=None, to='app.Mode')),
                ('project', models.ForeignKey(null=True, on_delete=None, to='app.Project')),
            ],
            options={
                'verbose_name': '测试报告',
                'verbose_name_plural': '测试报告',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Timmingtask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='定时任务名字', max_length=64)),
                ('taskstart', models.CharField(verbose_name='任务执行时间', max_length=64)),
                ('taskmakedate', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('status', models.BooleanField(verbose_name='任务状态', default=False)),
                ('yunxing_status', models.CharField(verbose_name='任务的运行状态，', max_length=16, default='创建')),
                ('case', models.ManyToManyField(to='app.Testcase')),
                ('makeuser', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
                ('prject', models.ForeignKey(on_delete=None, to='app.Project')),
                ('tesevent', models.ForeignKey(on_delete=None, to='app.Testeven')),
            ],
            options={
                'verbose_name': '定时任务',
                'verbose_name_plural': '定时任务',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('makedate', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('zhiwei', models.CharField(verbose_name='职位', max_length=32)),
                ('status', models.BooleanField(verbose_name='是否删除', default=False)),
            ],
            options={
                'verbose_name': '工作',
                'verbose_name_plural': '工作',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='testreport',
            name='task',
            field=models.ForeignKey(null=True, on_delete=None, to='app.Timmingtask'),
        ),
        migrations.AddField(
            model_name='testreport',
            name='testeven',
            field=models.ForeignKey(null=True, on_delete=None, to='app.Testeven'),
        ),
        migrations.AddField(
            model_name='testreport',
            name='testuser',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='testcase',
            name='events',
            field=models.ForeignKey(on_delete=None, to='app.Testeven'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='luoji',
            field=models.ForeignKey(on_delete=None, to='app.FunctionalLofic'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='mode',
            field=models.ForeignKey(null=True, on_delete=None, to='app.Mode'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='project',
            field=models.ForeignKey(null=True, on_delete=None, to='app.Project'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='user',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='test_xing',
            name='testreport',
            field=models.ForeignKey(on_delete=None, to='app.Testreport'),
        ),
        migrations.AddField(
            model_name='test_xing',
            name='user',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mode',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='app.Project'),
        ),
        migrations.AddField(
            model_name='functionallofic',
            name='mode',
            field=models.ForeignKey(null=True, on_delete=None, to='app.Mode'),
        ),
        migrations.AddField(
            model_name='functionallofic',
            name='project',
            field=models.ForeignKey(on_delete=None, to='app.Project'),
        ),
        migrations.AddField(
            model_name='functionallofic',
            name='user',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='function_element',
            name='function',
            field=models.ForeignKey(null=True, on_delete=None, to='app.FunctionalLofic'),
        ),
        migrations.AddField(
            model_name='function_element',
            name='user',
            field=models.ForeignKey(null=True, on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='casetestresult',
            name='case',
            field=models.ForeignKey(on_delete=None, to='app.Testcase'),
        ),
        migrations.AddField(
            model_name='casetestresult',
            name='events',
            field=models.ForeignKey(on_delete=None, to='app.Testeven'),
        ),
        migrations.AddField(
            model_name='casetestresult',
            name='user',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='newusers',
            name='work',
            field=models.ForeignKey(null=True, on_delete=None, to='app.Work'),
        ),
    ]
