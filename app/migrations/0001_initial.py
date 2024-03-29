# Generated by Django 3.2.6 on 2021-08-21 07:35

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newusers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('qq', models.IntegerField(blank=True, null=True, unique=True, verbose_name='qq')),
                ('mobile', models.IntegerField(blank=True, null=True, unique=True, verbose_name='手机号')),
                ('login_lock', models.BooleanField(default=False, verbose_name='是否锁定')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('token', models.CharField(max_length=252, null=True, verbose_name='token')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
            name='FunctionalLofic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('makedatye', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('desc', models.CharField(max_length=252, verbose_name='功能描述')),
                ('functionname', models.CharField(max_length=16, null=True, verbose_name='功能名称')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('update', models.CharField(max_length=8, null=True, verbose_name='更新人')),
                ('update_time', models.DateTimeField(default=datetime.datetime(2021, 8, 21, 15, 35, 13, 70128), verbose_name='更新时间')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('useuser', models.CharField(max_length=64, null=True, verbose_name='使用')),
                ('usedate', models.DateTimeField(auto_now_add=True, verbose_name='调用时间')),
                ('useip', models.CharField(max_length=252, verbose_name='调用者ip')),
                ('userheaders', models.CharField(max_length=252, verbose_name='调用者请求头')),
                ('userjiekou', models.CharField(max_length=252, verbose_name='调用接口')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('makedate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('makeuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('desc', models.CharField(max_length=255, null=True, verbose_name='简介')),
                ('makedate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('fenlei', models.CharField(choices=[('app', 'app'), ('web', 'web')], max_length=8, null=True, verbose_name='类型')),
                ('proeject', models.CharField(default='android', max_length=8, null=True, verbose_name='项目类型')),
                ('change_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('makeuser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('tasktype', models.IntegerField(blank=True, default=0, null=True, verbose_name='任务状态')),
                ('taskiphonetype', models.CharField(default='android', max_length=8, verbose_name='任务设备')),
                ('project', models.IntegerField(blank=True, verbose_name='所属项目')),
                ('runphonenum', models.IntegerField(blank=True, default=1, null=True, verbose_name='执行设备数')),
                ('iscollectperformncedata', models.BooleanField(default=True, verbose_name='是否收集性能数据')),
                ('tasklisttype', models.IntegerField(blank=True, default=0, verbose_name='任务列表的类型')),
            ],
            options={
                'verbose_name': '任务列表',
                'verbose_name_plural': '任务列表',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TasklistCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('task', models.IntegerField(blank=True, null=True, verbose_name='执行任务')),
                ('caserun', models.IntegerField(blank=True, null=True, verbose_name='执行caseID')),
            ],
            options={
                'verbose_name': '任务用例表',
                'verbose_name_plural': '任务用例表',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TasklistTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('task', models.IntegerField(blank=True, null=True, verbose_name='执行任务')),
                ('taskrun', models.IntegerField(blank=True, null=True, verbose_name='执行任务ID')),
            ],
            options={
                'verbose_name': '任务定时任务表',
                'verbose_name_plural': '任务定时任务表',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('makedate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('casenum', models.CharField(default=1, max_length=252, unique=True, verbose_name='测试用例编号')),
                ('data', models.CharField(max_length=252, verbose_name='参数')),
                ('yilai', models.BooleanField(default=False, verbose_name='是否依赖登录')),
                ('is_yilai', models.BooleanField(default=False, verbose_name='是否作为项目登录的依赖')),
                ('asser', models.CharField(max_length=252, verbose_name='预期')),
                ('savetest', models.BooleanField(default=False, verbose_name='是否保存测试结果')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('makedate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('name', models.CharField(default='开发环境', max_length=252, verbose_name='测试环境名字')),
                ('url_test', models.CharField(max_length=252, verbose_name='url')),
                ('port_test', models.IntegerField(default=80, verbose_name='port')),
                ('projetc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '测试环境',
                'verbose_name_plural': '测试环境',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('makedate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('zhiwei', models.CharField(max_length=32, verbose_name='职位')),
                ('status', models.BooleanField(default=False, verbose_name='是否删除')),
            ],
            options={
                'verbose_name': '工作',
                'verbose_name_plural': '工作',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Timmingtask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='定时任务名字')),
                ('taskstart', models.CharField(max_length=64, verbose_name='任务执行时间')),
                ('taskmakedate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('taskiphonetype', models.CharField(default='android', max_length=8, verbose_name='任务设备类型')),
                ('taskiphonenum', models.IntegerField(default=1, max_length=8, verbose_name='任务设备的数量')),
                ('status', models.BooleanField(default=False, verbose_name='任务状态')),
                ('yunxing_status', models.CharField(default='创建', max_length=16, verbose_name='任务的运行状态，')),
                ('case', models.ManyToManyField(to='app.Testcase')),
                ('makeuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('prject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
                ('tesevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.testeven')),
            ],
            options={
                'verbose_name': '定时任务',
                'verbose_name_plural': '定时任务',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Testreport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcallnum', models.CharField(max_length=252, verbose_name='测试报告编号')),
                ('tatal', models.IntegerField(verbose_name='总计')),
                ('passnum', models.IntegerField(blank=True, null=True, verbose_name='通过')),
                ('failnum', models.IntegerField(blank=True, null=True, verbose_name='失败')),
                ('errornum', models.IntegerField(blank=True, null=True, verbose_name='错误')),
                ('testhour', models.DateTimeField(blank=True, null=True, verbose_name='测试耗时')),
                ('makedate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('testlog', models.FilePathField(null=True, path='/testreport/', verbose_name='测试日志')),
                ('testrept', models.FilePathField(null=True, path='/testreport/', verbose_name='测试报告')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.mode')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.project')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.timmingtask')),
                ('testeven', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.testeven')),
                ('testuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '测试报告',
                'verbose_name_plural': '测试报告',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='testcase',
            name='events',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.testeven'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='luoji',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.functionallofic'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='mode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.mode'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.project'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Test_xing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.CharField(max_length=16, null=True, verbose_name='CPU')),
                ('neicun', models.CharField(max_length=16, null=True, verbose_name='内存')),
                ('shangxing', models.CharField(max_length=16, null=True, verbose_name='上传流量')),
                ('xiaxing', models.CharField(max_length=16, null=True, verbose_name='下行流量')),
                ('make_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('shebei', models.CharField(max_length=16, verbose_name='设备')),
                ('jihe', models.CharField(max_length=8, null=True, verbose_name='几核CPU')),
                ('fix', models.CharField(max_length=8, null=True, verbose_name='分辨率')),
                ('xitongbanben', models.CharField(max_length=8, null=True, verbose_name='系统版本')),
                ('xinghao', models.CharField(max_length=8, null=True, verbose_name='型号')),
                ('pinpai', models.CharField(max_length=8, null=True, verbose_name='品牌')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('functionluo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.functionallofic')),
                ('testreport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.testreport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '测试性能',
                'verbose_name_plural': '测试性能',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Project_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_guanliyuan', models.BooleanField(default=False, verbose_name='项目管理员')),
                ('productname', models.ManyToManyField(null=True, to='app.Project')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mode',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.project'),
        ),
        migrations.AddField(
            model_name='functionallofic',
            name='mode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.mode'),
        ),
        migrations.AddField(
            model_name='functionallofic',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project'),
        ),
        migrations.AddField(
            model_name='functionallofic',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Function_element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('makedatye', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('desc', models.CharField(max_length=252, null=True, verbose_name='步骤描述')),
                ('element_api', models.CharField(max_length=8, verbose_name='定位api')),
                ('index', models.IntegerField(default=0, null=True, verbose_name='索引')),
                ('element_ty', models.CharField(choices=[('id', 'id'), ('name', 'name'), ('css_selector', 'css selector'), ('xpath', 'xpath'), ('class_name', 'class name'), ('tag_name', 'tag name'), ('link_text', 'link text'), ('portial_link_text', 'portial link text')], max_length=32, null=True, verbose_name='定位的类型')),
                ('elemnet_by', models.CharField(max_length=252, null=True, verbose_name='定位')),
                ('caozuo', models.CharField(choices=[('click', 'click'), ('sendkeys', 'sendkeys')], max_length=32, null=True, verbose_name='操作')),
                ('canshu', models.CharField(max_length=252, null=True, verbose_name='参数')),
                ('is_asser', models.BooleanField(default=False, verbose_name='是否是断言')),
                ('xianhoui', models.IntegerField(default=0, verbose_name='先后顺序')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('function', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.functionallofic')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '逻辑',
                'verbose_name_plural': '逻辑',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Casetestresult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('makedate', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('testreport', models.CharField(max_length=252, verbose_name='测试结果')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.testcase')),
                ('events', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.testeven')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '测试结果',
                'verbose_name_plural': '测试结果',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='newusers',
            name='work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.work'),
        ),
    ]
