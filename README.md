Kudos Bot
============

This is a simple Slack app that is designed to give kudos to your teammates.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Setup
-----

You will need to set a few environment variables to get this to work properly:

    `SLACK_SLASH_TOKEN` - The token that you set up for your slash command.
    `SLACK_KUDOS_CHANNEL` - The channel name that you'd like to send kudos to. Defaults to `#general`
    `SLACK_WEBHOOK_URL` - The URL that you set up for posting back your kudos to.
