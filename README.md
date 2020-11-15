# APPTest 自动化测试平台
## 通过python 3.6+django 1.8+xadmin 实现的APP  UI自动化测试平台
## 使用说明：
### git  clone https://github.com/liwanlei/UFATestPlan.git  下载代码，设计的部分文档见doc文件夹下
### 进入目录，安装
        pip install -r requirements.txt
### 数据库配置(目前我使用的是sqlite数据库)
        DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            #'ENGINE':'django.db.backends.mysql',
            #'NAME':'liwanleiapptest',
            #'USER':'root',
            #'PASSWORD':'liwanlei',
            #'HOST':'127.0.0.1',
            #'PORT':'3306'
        }
    }
 ### 同步数据库操作
        python manage.py makemigrations
        python manage.py migrate
 ### 运行下面命令，可以启动我们的服务
    python manage.py runserver
 ### 使用下面命令去创建我们的超级管理员账户
    python manage.py createsuperuser
 ### 使用下面地址去访问我们的平台
  <http://127.0.0.1:8000>
  ### 使用下面地址去访问我们的管理后台
  超级管理员：admin 密码:testqwer
  <http://127.0.0.1:8000/xadmin>
  ###  本系统没有开放注册地址，用户需要在后台添加.
 ###  对于现有版本的系统，进行升级维护，平台实时任务，后台根据任务实时、或者定时执行。
 ###  部署后，PC端做一个轮训，实时查收后台任务。并定时对任务的状态进行上报
 ###  待做:1.目前定时任务还无法区分是ios或者安卓，测试用例也无法区分，可以在项目创建的时候区分IOS或者安卓
 ###       2.目前执行设备默认是1个。需要根据在添加任务的时候，增加一个入口，选择执行的设备数
 ###       3.pc端进行优化升级。支持IOS应用测试，PC端升级成为任务分发执行中心。
  
 ### pc端需要 pc_clicent的代码，配置config.py,(备注：pc端没有开源，可以联系作者购买。可以定制开发，联系qq：952943386
 ### pc端需要配置appium测试环境，测试需要连接测试设备。
 ### 启动appium服务，启动测试设备，安装好测试包，就可以run进行测试，测试完成后，测试报告自动上传后台，性能测试自动上传
 ### 平台运行，pc端可以和平台进行交互，通过接口，目前平台提供三个接口供pc端进行使用。
 ### 目前功能有限，后续继续优化。
 ### 运行效果展示：
  ![Alt text](https://github.com/liwanlei/UFATestPlan/blob/master/img/11.gif)
 ### 效果图展示：
 ![Alt text](https://github.com/liwanlei/UFATestPlan/blob/master/img/项目.png)
  ![Alt text](https://github.com/liwanlei/UFATestPlan/blob/master/img/测试用例.png)
  ![Alt text](https://github.com/liwanlei/UFATestPlan/blob/master/img/testreport.png)
  ![Alt text](https://github.com/liwanlei/UFATestPlan/blob/master/img/xingneng.png)
  ![Alt text](https://github.com/liwanlei/UFATestPlan/blob/master/img/QQ截图20180508161822.png)
  ![Alt text](https://github.com/liwanlei/UFATestPlan/blob/master/img/pc.png)
 ![Alt text](https://github.com/liwanlei/UFATestPlan/blob/master/img/pczhixing.png)
 
