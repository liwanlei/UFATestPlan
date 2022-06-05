# APPTest 自动化测试平台
## 通过python 3.6+django 1.8+xadmin 实现的APP  UI自动化测试平台
### 1.2.0版本更新
```
1.任务调整为普通任务和定时任务，普通任务默认执行一次，定时任务按时执行 (服务端实现完毕)
2.普通任务执行通过消息队列(服务端实现完毕)
3.定时任务redis队列下发(服务端实现完毕)
4.任务执行完毕，更新任务状态(服务端实现完毕)
```

## 使用说明：
### git  clone https://github.com/liwanlei/UFATestPlan.git  下载代码，设计的部分文档见doc文件夹下
### 进入目录，安装
        pip install -r requirements.txt
### 需要安装redis，可以在common/config.py 配置redis等相关信息
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
  超级管理员：admin 密码:admin
  <http://127.0.0.1:8000/xadmin>
  ###  本系统没有开放注册地址，用户需要在后台添加.
 ###  对于现有版本的系统，进行升级维护，平台实时任务，后台根据任务实时、或者定时执行。
 ###  部署后，pc端动态解析获取测试用例任务动态执行
 ### pc端需要 pc_clicent的代码升级到了pc_agent，减少配置化，动态化执行。(备注：pc端没有开源，可以联系作者购买。可以定制开发，联系qq：952943386）
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
 
