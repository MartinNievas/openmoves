import sys
sys.path.insert(0, '.')

import openmoves
application = openmoves.init(configfile='openmoves.cfg')

assert 'ADMINS' in application.config, 'no admins configured'
admins = application.config['ADMINS']

assert 'SYSTEM_SENDER_ADDRESS' in application.config, 'no system sender address configured'
system_sender_address = application.config['SYSTEM_SENDER_ADDRESS']

smtp_server = application.config['SMTP_SERVER']

# http://flask.pocoo.org/docs/errorhandling/
if not application.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(smtp_server, system_sender_address, admins, 'openmoves.net application error')
    mail_handler.setLevel(logging.ERROR)
    application.logger.addHandler(mail_handler)
