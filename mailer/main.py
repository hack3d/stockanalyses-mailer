#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import configparser
import requests
import time as t
import logging.handlers
from email.mime.text import MIMEText
import smtplib

# config
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(dir_path + '/config')

prod_server = config['prod']
storage = config['storage']

##########
# Logger
##########
LOG_FILENAME = storage['storage_logs'] + 'Mailer.log'
# create a logger with the custom name
logger = logging.getLogger('stockanalyses.Mailer')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(LOG_FILENAME)
fh.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=11000000, backupCount=5)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(handler)


# logger.addHandler(ch)


def getJob():
    """
    Retrieve a job to work.
    :return: 
    """
    try:
        print(prod_server['url'] + 'job/mailer_jobs')
        r = requests.get(prod_server['url'] + 'job/mailer_jobs')
        print(r.text)

        return r.json()

    except requests.exceptions.RequestException as e:
        logger.error("Error [%s]" % (e))


def updateJob(job_id, new_action):
    """
    Update job for mailer.
    :param job_id: 
    :param new_action: 
    :return: 
    """
    try:
        json_data = []
        json_data.append({'action': str(new_action)})
        print(prod_server['url'] + 'job/set_mailer_jobs_state/' + str(job_id))
        r = requests.put(prod_server['url'] + 'job/set_mailer_jobs_state/' + str(job_id), data=json.dumps(json_data),
                         headers={'Content-Type': 'application/json'})

        result_text = r.text
        result_text = result_text.encode('utf-8')
        print(result_text)

        return new_action

    except requests.exceptions.RequestException as e:
        logger.error("Error [%s]" % (e))


def sendMail(emailaddress, frommail, subject, message, mailserver, mailport, mailusername, mailpassword):
    """
    Send a mail
    :param emailaddress: 
    :param frommail:
    :param subject: 
    :param message: 
    :param mailserver:
    :return: 
    """

    logger.debug('Variables for function \'sendMail\'; emailaddress: %s' % (emailaddress))

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = frommail
    msg['To'] = emailaddress
    result = False

    try:
        s = smtplib.SMTP(mailserver, mailport)
        s.starttls()
        s.login(mailusername, mailpassword)
        problems = s.sendmail(frommail, emailaddress, msg.as_string())
        logger.debug('Send mail problems: %s' % problems)
        s.quit()
        result = True
    except:
        logger.error('Error: %s' % sys.exc_info()[0])
        result = False
    finally:
        return result


def main():
    logger.info('Start StockanalysesMailer...')

    while True:
        logger.debug('Get a job...')
        result = getJob()
        action_tmp = "-1"
        smtp_status = False

        if result['idemail_queue'] != 0 and result['action'] == 1000:
            logger.info('Job with id %s and action %s' % (result['idemail_queue'], result['action']))
            action_tmp = updateJob(result['idemail_queue'], '1100')

            logger.info('Set action to %s' % action_tmp)
        else:
            logger.info('No job for me...')

        if result['idemail_queue'] != 0 and action_tmp == '1100':
            logger.info('Start working on job with id %s' % result['idemail_queue'])
            smtp_status = sendMail(result['emailaddress'], prod_server['smtp_from'], result['subject'],
                                   result['message'], prod_server['smtp_server'], prod_server['smtp_port'],
                                   prod_server['smtp_user'], prod_server['smtp_password'])
        else:
            updateJob(result['idemail_queue'], '1900')

        if result['idemail_queue'] != 0 and smtp_status is True:
            logger.info('Set action to 1200')
            updateJob(result['idemail_queue'], '1200')
        else:
            updateJob(result['idemail_queue'], '1900')

        t.sleep(5)


if __name__ == '__main__':
    main()
