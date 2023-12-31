from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
import pickle

screenmanager = """

ScreenManager:
    SignUpScreen:
    LoginScreen:
    ProfileScreen:


<SignUpScreen>:
    name: 'sign'

    Label:
        text: 'Signup!'
        font_size: (self.height/15)*1
        pos_hint:{'center_x':0.48, 'center_y': 0.9}

    Label:
        text: 'Username'  
        font_size: (self.height/15)* 0.85
        pos_hint:{'center_x':0.25, 'center_y':0.7}

    TextInput:
        id: signupusername
        text: ''
        size_hint: 0.25, 0.05
        pos_hint:{'center_x':0.48,'center_y':0.7}    

    Label:
        text: 'password'
        font_size: (self.height/15)* 0.85
        pos_hint: {'center_x':0.25, 'center_y':0.6}  

    TextInput:
        id:signuppassword
        text: ''
        size_hint: 0.25, 0.05
        pos_hint: {'center_x': 0.48, 'center_y': 0.6}    
        password: True


    Button:
        text: 'Sign up'
        size_hint: .2,.1
        pos_hint:{'center_x': 0.48, 'center_y': 0.45}    
        on_press: root.signup()

    Label:
        text:'Signed Up?'    
        font_size: (self.height/15) * 0.85
        pos_hint: {'center_x': 0.25, 'center_y': 0.25}   

    Button:
        text: 'Login'
        size_hint: .2,.1
        pos_hint:{'center_x': 0.48, 'center_y': 0.25}    
        on_press: root.manager.current = 'Login'  

    Label:
        text:root.signuperror   
        font_size: (self.height/15) * 0.85
        pos_hint: {'center_x': 0.35, 'center_y': 0.15}     


<LoginScreen>:
    name: 'Login'

    Label:
        text: 'Login!'
        font_size: (self.height/15)*1
        pos_hint:{'center_x':0.48, 'center_y': 0.9}

    Label:
        text: 'Username'  
        font_size: (self.height/15)* 0.85
        pos_hint:{'center_x':0.25, 'center_y':0.7}

    TextInput:
        id: loginusername
        text: ''
        size_hint: 0.25, 0.05
        pos_hint:{'center_x':0.48,'center_y':0.7}    

    Label:
        text: 'password'
        font_size: (self.height/15)* 0.85
        pos_hint: {'center_x':0.25, 'center_y':0.6}  

    TextInput:
        id:loginpassword
        text: ''
        size_hint: 0.25, 0.05
        pos_hint: {'center_x': 0.48, 'center_y': 0.6}    
        password: True


    Button:
        text: 'Login'
        size_hint: .2,.1
        pos_hint:{'center_x': 0.48, 'center_y': 0.45}    
        on_press: root.login()

    Label:
        text:'Not Signed Up?'    
        font_size: (self.height/15) * 0.85
        pos_hint: {'center_x': 0.2, 'center_y': 0.25}   

    Button:
        text: 'Sign up'
        size_hint: .2,.1
        pos_hint:{'center_x': 0.48, 'center_y': 0.25}    
        on_press: root.manager.current = 'sign'  


    Label:
        text:root.loginerror   
        font_size: (self.height/15) * 0.85
        pos_hint: {'center_x': 0.35, 'center_y': 0.15}     

<ProfileScreen>:
    name: 'Profile'

    Label:
        text: 'Account Successfully Created Or Logged In'    
        font_size: (self.height/15)*1
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}

    Button:
        text: 'Sign Out'
        size_hint: .2,.1
        pos_hint:{'center_x': 0.48, 'center_y': 0.45}    
        on_press: root.manager.current = 'sign'   

"""


class ProfileCreate(App):

    def build(self):
        screen = Builder.load_string(screenmanager)
        return screen


class SignUpScreen(Screen):
    signuperror = StringProperty()

    def signup(self):
        sigingupusername = self.ids.signupusername.text
        siginguppassword = self.ids.signuppassword.text

        if (sigingupusername == '' and siginguppassword == ''):
            print('Text cant be empty')
            self.signuperror = str('Text Cant be empty')


        else:
            sigingupusername = pickle.dump(sigingupusername, open("Signupusername", "w"))
            siginguppassword = pickle.dump(siginguppassword, open("Signuppassword", "w"))

            sigingupusername = self.ids.signupusername.text = ''
            siginguppassword = self.ids.signuppassword.text = ''
            self.parent.current = 'Profile'
            self.signuperror = str()


class LoginScreen(Screen):
    loginerror = StringProperty()

    def login(self):
        createdusername = self.ids.loginusername.text
        createdpassword = self.ids.loginpassword.text
        signingupusername = pickle.load(open("Signupusername", "r"))
        signinguppassword = pickle.load(open("Signuppassword", "r"))

        if signingupusername == createdusername and signinguppassword == createdpassword:
            print('correct username and password')
            self.loginerror = str()

            self.parent.current = 'Profile'
        elif signingupusername != createdusername and signinguppassword != createdpassword:
            print('incorrect username and password')
            self.loginerror = str('Incorrect Username/Password')

        elif signingupusername == createdusername and signinguppassword != createdpassword:
            print('incorrect username and password')
            self.loginerror = str('Incorrect Username/Password')

        elif signingupusername != createdusername and signinguppassword == createdpassword:
            print('incorrect username and password')
            self.loginerror = str('Incorrect Username/Password')


class ProfileScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LoginScreen(name='Login'))
sm.add_widget(SignUpScreen(name='Sign'))
sm.add_widget(ProfileScreen(name='Profile'))

ProfileCreate().run()