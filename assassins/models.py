from django.db import models
from django.utils.timezone import now
from django.core.mail import send_mail

from assassins.settings import ADMIN_EMAILS, HOME_PAGE_URL

class Player(models.Model):
    sunetid = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    target = models.OneToOneField('self', null=True, blank=True)
    assign_time = models.DateTimeField(null=True, blank=True)
    living = models.BooleanField(default=True)

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def kill_target(self, details):
        victim = self.target
        self.target = victim.target
        victim.die()
        self.assign_time = now()
        self.save()
        #self.emailKillInfoToAdmin(victim, details)
        #self.emailKillInfoToTarget(victim)

    def die(self):
        self.target = None
        self.living = False
        self.save()

    def emailKillInfoToAdmin(self, deceased, details):
        killer = self
        killer_name = killer.full_name()
        deceased_name = deceased.full_name()
        subject = "%s assassinated %s" % (killer_name, deceased_name)
        
        message = ""
        
        # New target
        message += "New target: %s\n" % killer.target.full_name()
        # Assign time
        message += "Assign time: %s\n" % str(killer.assign_time)
        # Details
        message += "Details:\n%s\n\n" % details
        # Current game ring
        message += "Current game ring:\n%s\n\n" % gameRingAsString()
        
        send_mail(subject, message, "Angel of Death", ADMIN_EMAILS)


    def emailKillInfoToTarget(self, target):
        subject = "You have been assassinated..."
        
        message = ""
        message += "Thanks for playing! You are invited to revisit %s " % HOME_PAGE_URL
        message += "to see the list of currently living and assassinated "
        message += "players. "
        message += "\n"
        message += "AS A REMINDER: Please do not tell your target who "
        message += "assassinated you. Thanks!"
        message += "\n"
        message += "\n"
        message += "-Gavi"
        
        target_email = target.sunetid + "@stanford.edu"
        #target_email = 'gavilan' + "@stanford.edu"
        
        send_mail(subject, message, "Angel of Death", [target_email])


class Quote(models.Model):
    text = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text


def gameRingAsString():
    players = list(Player.objects.filter(living=True))
    output = ""
        
    for player in players[:-1]:
        target = player.target
        output += "%s is assigned %s\n" % (player.full_name(), target.full_name())
           
        # Wrap end of list back to beginning
        player = players[-1]
        target = players[0]
        output += "%s is assigned %s\n" % (player.full_name(), target.full_name())
            
    return output


def email_all(subject, message, email_admins=True):
    dest_emails = []

    if (email_admins):
        dest_emails += ADMIN_EMAILS

    players = Player.objects.all()            
    for player in players:
        sunetid = player.sunetid
        email_addr = "%s@stanford.edu" % sunetid
        dest_emails.append(email_addr)

    send_mail(subject, message, "Serra Assassins", dest_emails)


def game_over():
    players = list(Player.objects.filter(living=True))
    if len(players) == 1:
        winningPlayer = players[0]
        send_game_over_message(winningPlayer)
        return True
    
    return False

def send_game_over_message(winningPlayer):
    subject = "Your Assassins Champion"
    
    message = ""
    message += "...is %s! Congratulations!" % winningPlayer.full_name()
    message += "\n\n"
    message += "Thanks for playing everyone"
    message += "\n\n"
    message += "-Gavi"

    email_all(subject, message)
