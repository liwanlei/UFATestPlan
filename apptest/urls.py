"""apptest URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from app.views import *
from common import xadmin
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
urlpatterns = [
    url(r'xadmin/', (xadmin.site.urls)),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^$', login_required(IndexView.as_view())),
    url(r'^home/', login_required(IndexView.as_view()), name='home'),
    url(r'^project/', login_required(ProjectView.as_view()), name='project'),
    url(r'^model/', login_required(ModelView.as_view()), name='model'),
    url(r'^xingneng/', login_required(XingnengView.as_view()), name='xingneng'),
    url(r'^changepassword/', login_required(ChangepasswordView.as_view()), name='changepassword'),
    url(r'^useradmin/', login_required(UseradminView.as_view()), name='useradmin'),
    url(r'^testcase/', login_required(TestCaseView.as_view()), name='testcase'),
    url(r'^tingtask/', login_required(TingtaskViews.as_view()), name='tingtask'),
    url(r'^testreport/', login_required(TestReportView.as_view()), name='testreport'),
    url(r'^testfaution/', login_required(TestCaseLuojiView.as_view()), name='testfaution'),
    url(r'^testevent/', login_required(TestEvevtView.as_view()), name='testevent'),
    url(r'^edittiming/(?P<id>\d+)/', login_required(EdittaskView.as_view()), name='edittiming'),
    url(r'^resetuser/(?P<id>\d+)/', login_required(ResetUser.as_view()), name='resetuser'),
    url(r'^addfunction/', login_required(AddFuntionsView.as_view()), name='addfunction'),
    url(r'^addtestcase/', login_required(AddCaseView.as_view()), name='addtestcase'),
    url(r'^gettestevent/', login_required(Getevet.as_view()), name='gettestevent'),
    url(r'^gettestcase/', login_required(Getcase.as_view()), name='gettestcase'),
    url(r'^get_test_case/',login_required(Gettestcase.as_view()),name='get_test_case'),
    url(r'^addting/', login_required(AddtimgView.as_view()), name='addting'),
    url(r'^editfuntion/(?P<id>\d+)/', login_required(EditFuntionsView.as_view()), name='editfuntion'),
    url(r'^editcase/(?P<id>\d+)/', login_required(EditCaseView.as_view()), name='editcase'),
    url(r'^gettask/', GettaskView.as_view(), name='gettask'),
    url(r'^greatreport/', Greatreport.as_view(), name='greatreport'),
    url(r'^sendxing/', SendXing.as_view(), name='sendxing'),
    url(r'^file_down/(?P<filename>.*)$',file_down,name='file_down'),
    url(r'^yilaicase/',YiLaiLogin.as_view(),name='yilaicase'),
    url(r'^huoxingneng/',login_required(Huoqufun.as_view()),name='huoxingneng'),
]