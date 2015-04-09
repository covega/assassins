from datetime import timedelta

SENDING_EMAILS = True

HOME_PAGE_URL = 'assassins.stanford.edu'

DOMAIN_NAME = 'assassins.stanford.edu'

OUTGOING_MAIL_ADDRESS = 'noreply@' + DOMAIN_NAME

PLAYER_TIMEOUT_VALUE = timedelta(seconds=259200)

SUDDEN_DEATH_COUNTDOWN_VALUE = timedelta(days=2)
