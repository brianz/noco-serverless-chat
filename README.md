# Serverless noco-sls-chat

This is a Serverless project which creates a websocket chat backend. It's quite basic, but supports
some standard features including setting a nickname, multiple channels, and broadcasting messages
to channel members. The coolest this is that this is entirely serverless and in Python!


# Demo

[![asciicast](https://asciinema.org/a/O1ya9VitrkhH1lQVCqxbJsV6P.svg)](https://asciinema.org/a/O1ya9VitrkhH1lQVCqxbJsV6P)

# Getting started

- Add AWS credentials into the `envs/$(whoami)` file. This file can be named anything, but I
  suggest your username or something else specific. You can just name it `envs/dev` as well. See
  `envs/example` for help. **Use `us-west-2` as your default region, others will not function properly.**
- Start up the shell with docker: `ENV=$(whoami) make shell` *NOTE*: The value after `ENV=` is merely
  the name of the file you created. So if you created the `envs/dev` file, do `ENV=dev`. Now you're
  in your Docker container which has all of the necessary libraries and tooling.

**Run all of the following commands in your Docker container!**

- Run `make deploy`
- This will deploy everything you need to AWS. You'll see a websocket URI from the output of that command, something like
  `wss://aipsb783ea.execute-api.us-west-2.amazonaws.com/username`
- Install `wscat` by just running `yarn` (still in the `/code` directory)
- In two different terminals: `./node_modules/.bin/wscat -c wss://YOUR_WS_ENDPOING`
- Now start typing...you'll see messages from one window pop up into another.

# Commands

- `/name bz` - Change your display name to `bz`
- `/channel random` - Change to the `random` channel. Default channel is `general`
- `/help`

# Dev setup

This project was bootstrapped using the my Serverless Cookiecutter template. This is a
opinionated setup in order to facilitate developing, running and bootstrapping Serverless projects
authored in Python.

For more information, see the following:

- [Serverless Docker image, used in this template](https://github.com/brianz/serverless)
- [A thorough explanation of this layout and reasoning behind it](http://blog.brianz.bz/post/structuring-serverless-applications-with-python/)
