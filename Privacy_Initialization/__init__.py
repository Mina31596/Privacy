
from otree.api import *
c = cu

doc = ''
class Constants(BaseConstants):
    name_in_url = 'Privacy_Initialization'
    players_per_group = None
    num_rounds = 1
    questions = ('Are you attracted to anyone in the room?', 'Have you ever been arrested?', 'Can you imagine pursuing a political career?')
def Update_Player_Ranking(subsession):
    pass
class Subsession(BaseSubsession):
    pass
def displayQuestion(group):
    import random
    import copy
    
    questions = copy.deepcopy(Constants.question_stack)
    #now append the players questions here
    
    #then suffle
    random.shuffle(questions)
    #group.current_question = questions[0]
    
def getTotalYes(group):
    pass
def calculateRewards(group):
    pass
class Group(BaseGroup):
    answer_yeses = models.IntegerField(initial=0)
    number_of_players = models.IntegerField(initial=0)
def enterQuestion(player):
    session = player.session
    group = player.group
    import random
    
    random.shuffle(session.quesstion_bank)
    group.current_question = session.quesstion_bank[0]
    
    session.quesstion_bank = ["question1","question2","question3","question 4","question 5","question 6","question 7","question8","question9"]
    session.used_questions=[" "]
    session.quesstion_bank.append(player.enter_question)
def determine_valid_id(player):
    session = player.session
    group = player.group
    participant = player.participant
    p_host= group.get_player_by_id(1)
    session.invalid_Ids =[]
    if(participant.id_in_session ==1):
        participant.is_dropout = False
    elif player.id_InGroup != p_host.host_Id:
        session.invalid_Ids.append(player.id_in_group)
        participant.is_dropout= True
    else:
        participant.is_dropout=False
class Player(BasePlayer):
    id_InGroup = models.IntegerField()
    name = models.StringField()
    host = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], initial=False, label=' ')
    host_Id = models.IntegerField()
    enter_question = models.LongStringField(blank=True, label='Enter a question you would like to ask the group here:')
    is_dropout = models.BooleanField(initial=False)
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
    @staticmethod
    def before_next_page(player, timeout_happened):
        determine_valid_id(player)
class Join_session(Page):
    form_model = 'player'
    form_fields = ['id_InGroup']
    @staticmethod
    def is_displayed(player):
        return player.host==False
    @staticmethod
    def before_next_page(player, timeout_happened):
        determine_valid_id(player)
class Invalid_id(Page):
    form_model = 'player'
    form_fields = ['id_InGroup']
    @staticmethod
    def is_displayed(player):
        session = player.session
        group = player.group
        check = player.id_in_group in session.invalid_Ids
        return check
    @staticmethod
    def before_next_page(player, timeout_happened):
        determine_valid_id(player)
class Invalid_ID_dropout(Page):
    form_model = 'player'
    timeout_seconds = 10
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        return participant.is_dropout
class WaitPage1(WaitPage):
    body_text = 'Waiting for all the players to join'
class Write_Questions(Page):
    form_model = 'player'
    form_fields = ['enter_question']
    @staticmethod
    def is_displayed(player):
        group = player.group
        participant = player.participant
        return participant.is_dropout==False
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.vars["added_questions"] = player.enter_question
        
        
page_sequence = [Welcome_Page, Host_Session, Join_session, Invalid_id, Invalid_ID_dropout, WaitPage1, Write_Questions]
