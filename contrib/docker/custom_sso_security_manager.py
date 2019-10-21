#from superset.security import SupersetSecurityManager

#class CustomSsoSecurityManager(SupersetSecurityManager):

#    def oauth_user_info(self, provider, response=None):
        
#        return { 'email': 'luisa.gonzalez@rokk3rlabs.com', 'username': 'luisa.gonzalez@rokk3rlabs.com', 'first_name': 'Luisa', 'last_name': 'Gonzalez' }

from flask import redirect, g, flash, request
from flask_appbuilder.security.views import UserDBModelView,AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_login import login_user, logout_user, LoginManager, UserMixin
import logging
class CustomAuthDBView(AuthDBView):
    login_template = 'appbuilder/general/security/login_db.html'
    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        redirect_url = self.appbuilder.get_url_for_index
        if request.args.get('redirect') is not None:
            redirect_url = request.args.get('redirect') 

        if request.args.get('username') is not None:
            user = self.appbuilder.sm.find_user(username=request.args.get('username'))
            login_user(user, remember=False)
            return redirect(redirect_url)
        else:
            return super(CustomAuthDBView,self).login()

class User(UserMixin):
    def __init__(self, user):
        self.user = user
        self.roles = [{'name': 'Admin', 'id': 1}]

class CustomSecurityManager(SupersetSecurityManager):
    authdbview = CustomAuthDBView
    def load_user_from_request(self, header_val):  
        user = self.appbuilder.sm.find_user(username=header_val)
        return User({'username': 'Luisa' })
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)
        self.lm.header_loader(self.load_user_from_request)