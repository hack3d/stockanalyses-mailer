# Stockanalyses-Mailer
It's a microservice which will send mails from a queue.

## Actions
This is a list of possible supported actions:

| Action | Description |
| ------ | ----------- |
| 1000 | Initial state |
| 1100 | Job is in progress |
| 1200 | Job is finished |
| 1900 | Job failed |