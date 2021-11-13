
from otree.api import *
c = cu

doc = ''
class Constants(BaseConstants):
    name_in_url = 'Privacy_Initialization'
    players_per_group = None
    num_rounds = 1

def Update_Player_Ranking(subsession):
    pass

class Subsession(BaseSubsession):
    pass

def displayQuestion(group):
    session = group.session
    import random
    random.shuffle(session.quesstion_bank)
    group.current_question = session.quesstion_bank[0]
    
def getTotalYes(group):
    pass

def calculateRewards(group):
    pass

class Group(BaseGroup):
    current_question = models.StringField()

def enterQuestion(player):
    session = player.session
    session.quesstion_bank = ["question1","question2","question3","question 4","question 5","question 6","question 7","question8","question9"]
    session.used_questions=[" "]
    session.quesstion_bank.append(player.enter_question)

class Player(BasePlayer):
    id_InGroup = models.IntegerField()
    name = models.StringField()
    host = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], initial=False, label=' ')
    host_Id = models.IntegerField()
    enter_question = models.LongStringField(label='Ask a question for everyone to answer.')

class Welcome_Page(Page):
    form_model = 'player'
    form_fields = ['host']
    @staticmethod
    def before_next_page(player, timeout_happened):
        import random
        num = random.randint(0,189753)
        player.host_Id = num

class Host_Session(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.host==True

class Join_session(Page):
    form_model = 'player'
    form_fields = ['id_InGroup']
    @staticmethod
    def is_displayed(player):
        return player.host==False

class WaitPage1(WaitPage):
    body_text = 'Waiting for all the players to join'

class Advertisement(Page):
    form_model = 'player'

class Write_Question(Page):
    form_model = 'player'
    form_fields = ['enter_question']
    @staticmethod
    def before_next_page(player, timeout_happened):
        enterQuestion(player)
page_sequence = [Welcome_Page, Host_Session, Join_session, WaitPage1, Advertisement, Write_Question]