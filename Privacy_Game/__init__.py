
from otree.api import *
c = cu


class Constants(BaseConstants):
    name_in_url = 'Privacy_Game'
    players_per_group = None
    num_rounds = 10
    instructions_template = 'Privacy_Game/instructions.html'

class Subsession(BaseSubsession):
    player_ranking = models.IntegerField()

def display_question(group):
    session = group.session
    import random
    random.shuffle(session.quesstion_bank)
    while(session.quesstion_bank[0] in session.used_questions):
        random.shuffle(session.quesstion_bank)
    group.current_question = session.quesstion_bank[0]
    session.used_questions.append(session.quesstion_bank[0])
    print(group.current_question)

#functions still needed to be complete
def calculate_rewards(group):
    pass
def get_total_yes(group):
    pass
def update_player_ranking(group):
    pass


class Group(BaseGroup):
    current_question = models.StringField()
    total_yeses = models.IntegerField()

class Player(BasePlayer):
    id_inGroup = models.IntegerField(label='Please enter the ID given by the host')
    answer = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='')
    rewards = models.IntegerField()
    name = models.StringField()
    host = models.BooleanField()
    my_field = models.StringField()
    enter_question = models.LongStringField(blank=True, label='Enter question you would like to ask the group')
    guess = models.IntegerField(label='')

class Wait_page_1(WaitPage):
    after_all_players_arrive = display_question

class Answer_Question_Page(Page):
    form_model = 'player'
    form_fields = ['answer']

class Wait_page_2(WaitPage):
    after_all_players_arrive = get_total_yes

class Guess_page(Page):
    form_model = 'player'
    form_fields = ['guess']

class Wait_page_3(WaitPage):
    after_all_players_arrive = calculate_rewards

class Round_results(Page):
    form_model = 'player'

class Final_results(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        session = player.session
        subsession = player.subsession
        return subsession.round_number==10


page_sequence = [Wait_page_1, Answer_Question_Page, Wait_page_2, Guess_page, Wait_page_3, Round_results, Final_results]