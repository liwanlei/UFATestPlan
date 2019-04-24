# APPTest 自动化测试平台
## 通过python 3.6+django 1.8+xadmin 实现的APP  UI自动化测试平台
## 使用说明：
### git  clone XXX  下载代码，
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
  <http://127.0.0.1:8000/xadmin>
  ###  本系统没有开放注册地址，用户需要在后台添加.
 ### pc端需要 pc_clicent的代码，配置config.py,(备注：pc端没有开源，可以联系作者购买。源码：800一份，可以定制开发，联系qq：952943386
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
 
