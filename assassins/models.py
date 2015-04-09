from django.db import models
from django.utils.timezone import now
from django.core.mail import EmailMessage

from assassins.settings import *

from random import shuffle

class Dorm(models.Model):
    name = models.CharField(max_length=200)
    game_started = models.BooleanField(default=False)
    sudden_death_countdown = models.DateTimeField(null=True, blank=True)
    sudden_death = models.BooleanField(default=False)
    game_over = models.BooleanField(default=False)
    
    
    def __unicode__(self):
        return self.name

    def get_sudden_death_countdown_remaining(self):
        #time_elapsed = now() - self.sudden_death_countdown
        time_remaining = self.sudden_death_countdown - now()
        if (time_remaining.total_seconds() > 0):
            #time_remaining = SUDDEN_DEATH_COUNTDOWN_VALUE - time_elapsed
            return int(time_remaining.total_seconds())  #truncate decimals
        else:
            return 0

    def start_sudden_death_countdown(self):
        self.sudden_death_countdown = now() + SUDDEN_DEATH_COUNTDOWN_VALUE
        self.save()


class Admin(models.Model):
    sunetid = models.CharField(max_length=200)    
    dorm = models.ForeignKey(Dorm)
    
    def __unicode__(self):
        return self.sunetid


class Player(models.Model):
    sunetid = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    dorm = models.ForeignKey(Dorm)
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
        self.emailKillInfoToAdmin(victim, details)
        self.emailKillInfoToTarget(victim)

    def die(self):
        self.target = None
        self.living = False
        self.save()

    def die_from_timeout(self):
        # Save who is targeting me and who I am targeting
        myKiller = Player.objects.get(target=self)
        myTarget = self.target

        # Die
        self.die()

        # Rewire the loop of players
        myKiller.target = myTarget
        #myKiller.assign_time = now()
        myKiller.save()

        # Email everyone
        self.inform_of_self_timeout()
        self.inform_admin_of_self_timeout()
        myKiller.inform_of_victim_timeout()


    def inform_admin_of_self_timeout(self):
        if not SENDING_EMAILS: return;

        subject = "%s timed out" % self.full_name()
        message = "Current game ring:\n%s\n\n" % game_ring_as_string(self.dorm)

        admins = Admin.objects.filter(dorm=self.dorm)
        
        admin_emails = [admin.sunetid+"@stanford.edu" for admin in admins]
        
        #send_mail(subject, message, 
        #          "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
        #          ADMIN_EMAILS)
        email = EmailMessage(subject, message, 
                             "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
                             to=[OUTGOING_MAIL_ADDRESS],
                             bcc=admin_emails)
        email.send()
        

    def inform_of_self_timeout(self):
        if not SENDING_EMAILS: return;

        subject = "You have been eliminated..."

        message = ""
        message += "The allotted time has passed and your contract has "
        message += "expired. You have been eliminated."
        message += "\n\n"
        message += "Thanks for playing! You are invited to revisit %s " % HOME_PAGE_URL
        message += "to see the list of currently living and assassinated "
        message += "players. "
        message += "\n"
        message += "\n"

        email = self.sunetid + "@stanford.edu"
        
        #send_mail(subject, message, 
        #          "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
        #          [email])

        email = EmailMessage(subject, message, 
                             "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
                             to=[OUTGOING_MAIL_ADDRESS],
                             bcc=[email])
        email.send()


    def inform_of_victim_timeout(self):
        if not SENDING_EMAILS: return;

        subject = "Your target has expired"

        message = ""
        message += "Your target failed to fulfill their contract in time "
        message += "and has been eliminated."
        message += "\n\n"
        message += "Your new target is %s " % self.target.full_name()
        message += "\n\n"
        message += "Good luck."

        email = self.sunetid + "@stanford.edu"

        #send_mail(subject, message,
        #          "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
        #          [email])

        email = EmailMessage(subject, message, 
                             "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
                             to=[OUTGOING_MAIL_ADDRESS],
                             bcc=[email])
        email.send()
        

    def get_time_remaining(self):
        time_elapsed = now() - self.assign_time
        if (PLAYER_TIMEOUT_VALUE > time_elapsed):
            time_remaining = PLAYER_TIMEOUT_VALUE - time_elapsed
            return int(time_remaining.total_seconds())  #truncate decimals
        else:
            return 0

    def emailKillInfoToAdmin(self, deceased, details):
        if not SENDING_EMAILS: return;

        killer = self
        killer_name = killer.full_name()
        deceased_name = deceased.full_name()
        subject = "%s assassinated %s" % (killer_name, deceased_name)
        
        message = ""
        
        # New target
        message += "New target: %s\n" % killer.target.full_name()
        # Details
        message += "Details:\n%s\n\n" % details
        # Current game ring
        message += "Current game ring:\n%s\n\n" % game_ring_as_string(self.dorm)
        
        admins = Admin.objects.filter(dorm=self.dorm)
        admin_emails = [admin.sunetid+"@stanford.edu" for admin in admins]

        #send_mail(subject, message, 
        #          "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
        #          admin_emails)

        email = EmailMessage(subject, message, 
                             "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
                             to=[OUTGOING_MAIL_ADDRESS],
                             bcc=admin_emails)
        email.send()


    def emailKillInfoToTarget(self, target):
        if not SENDING_EMAILS: return;

        subject = "You have been assassinated..."
        
        message = ""
        message += "You are invited to revisit %s " % HOME_PAGE_URL
        message += "to see the list of currently living and assassinated "
        message += "players. "
        message += "\n\n"
        message += "As a reminder: Please DO NOT tell your target who "
        message += "assassinated you."
        message += "\n\n"
        message += "Thanks for playing!"
        
        target_email = target.sunetid + "@stanford.edu"
        
        #send_mail(subject, message, 
        #          "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
        #          [target_email])

        email = EmailMessage(subject, message, 
                             "Angel of Death <%s>" % OUTGOING_MAIL_ADDRESS, 
                             to=[OUTGOING_MAIL_ADDRESS],
                             bcc=[target_email])
        email.send()


class Quote(models.Model):
    text = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text


def game_ring_in_order(dorm):
    players = list(Player.objects.filter(living=True, dorm=dorm))
    if len(players) is 0:
        return players

    firstPlayer = players[0]
    currentPlayer = firstPlayer.target
    
    index = 1
    while (currentPlayer != firstPlayer):
        players[index] = currentPlayer
        currentPlayer = currentPlayer.target
        index += 1

    return players
    

def game_ring_as_string(dorm):
    players = game_ring_in_order(dorm)
    output = ""
        
    for player in players[:-1]:
        target = player.target
        output += "%s is assigned %s\n" % (player.full_name(), target.full_name())
           
    # Wrap end of list back to beginning
    player = players[-1]
    target = players[0]
    output += "%s is assigned %s\n" % (player.full_name(), target.full_name())
            
    return output


def game_over(dorm):
    players = list(Player.objects.filter(living=True, dorm=dorm))
    if len(players) == 1:
        winningPlayer = players[0]
        send_game_over_message(winningPlayer, dorm)
        dorm.game_over = True
        dorm.save()
        return True
    
    return False

def send_game_over_message(winningPlayer, dorm):
    subject = "Your Assassins Champion"
    
    message = ""
    message += "...is %s! Congratulations!" % winningPlayer.full_name()

    players = Player.objects.filter(dorm=dorm)
    admins = Admin.objects.filter(dorm=dorm)

    dest_addresses = [player.sunetid+"@stanford.edu" for player in players]
    dest_addresses.extend([admin.sunetid+"@stanford.edu" for admin in admins])

    #send_mail(subject, message, 
    #          "Assassins <%s>" % OUTGOING_MAIL_ADDRESS, 
    #          dest_addresses)

    email = EmailMessage(subject, message, 
                         "Assassins <%s>" % OUTGOING_MAIL_ADDRESS, 
                         to=[OUTGOING_MAIL_ADDRESS],
                         bcc=dest_addresses)
    email.send()


def assign_targets(dorm, reset_timestamps=True):
    players = list(Player.objects.filter(living=True, dorm=dorm))
    shuffle(players)
    
    # Null out any previous assignments for each player
    for player in players:
        player.target = None
        player.save()
        
    # Assign targets to each player
    for index, player in enumerate(players[:-1]):
        target = players[index + 1]
        
        player.target = target
        if (reset_timestamps):
            player.assign_time = now()#.replace(tzinfo=utc)
        player.save()
        
    # Wrap end of list back around to the beginning to complete cycle
    player = players[-1]
    target = players[0]
    
    player.target = target
    if (reset_timestamps):
        player.assign_time = now()
    player.save()
