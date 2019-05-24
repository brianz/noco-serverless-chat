Hi everyone,

I've run one workshop where we try to get a real application up and running. That taught me a few things regarding everyone's
personal setups and where the pain points are. Below are the instructions to prepare yourselves and
your laptops.

We'll be building a (very basic) chat application, all with serverless technologies. Think Slack, without any extra features.
The code is all there and working. The goal of this is for you to understand all of the moving pieces and to _deploy your
own applicatioin with your own AWS account from your own laptop!_

To set yourself and me up for success, please get the prerequisites out of the way ASAP.

**DO THIS BEFORE THE DAY OF THE WORKSHOP!**

I can guarantee that if you try to do this _during_ the workshop, you will fail.

## Tools

We'll be using the Serverless framework to deploy all of our code. There are multiple ways of setting this up, of course. I've broken up the options by OS:

### MacOS

- Use a Docker image which I maintain that has the Serverless Framework and associated tooling installed and ready to go. The requirements for this setup are:
  - A shell (ie, `bash`, `zsh`, etc)
  - `make`
  - Docker
- [Install Serverless on your own](https://serverless.com/framework/docs/providers/aws/guide/installation/). The requirements for that are:
  - A shell (ie, `bash`, `zsh`, etc)
  - `node.js`

#### Docker

If your laptop has Docker and `make` installed, this will be the fastest and easiest option. If you
need to install Docker, [read the docs for MacOS](https://docs.docker.com/docker-for-mac/).

If you don't know if you have `make`, run the following in a terminal:

    $ which make
    /usr/bin/make

If nothing comes back after `which make`, you'll need to install XCode and the Developer Tools (I
think).

If you have both Docker and `make` working, run the following in a shell to pull down my Serverless
Docker image:

    docker pull brianz/serverless

#### Installing Serverless

If you'd rather install the Serverless Framework on your laptop yourself, follow the instructions
linked above. The only prerequisite is node.js (and a shell, of course).

Once you get Serverless installed, be sure you can deploy a simple application using their
[Quick start guide](https://serverless.com/framework/docs/providers/aws/guide/quick-start/).

### Linux

If you're on Linux it's probably easiest to just install Serverless on your laptop...follow the
same instructions as above.

### Windows

Sadly, if you are using a Windows laptop, I cannot help you (I simply don't know how to setup Windows for development purposes).
All of the steps and commands used in this workshop use a Linux/MacOS shell (i.e., `bash`). If you are using Windows, you'll need
to figure out the best way to install the Serverless framework.
Read [the installation docs](https://serverless.com/framework/docs/providers/aws/guide/installation/)...if you can get Serverless setup, you should be able to participate.

One thing I can point you to is Docker as an option. Note, you'll still need access to a shell, but
these docs may offer more help than me in that regard.

https://docs.docker.com/docker-for-windows/

If you can get Docker set up, pull down my image (listed above)...if you get that far, you'll be in
good shape!

If you're not using Docker but can get the Serverless framework installed, try to run through their
[Quick start guide](https://serverless.com/framework/docs/providers/aws/guide/quick-start/) and try
to deploy a `Hello World!` application. If you do that, you're good to go!

## AWS

The other big thing you'll need is an AWS account. These accounts are free to create but you do need to provide a
credit card. If you don't have an account just click the "Create an AWS Account" button in the upper right.

Whether you're creating a new account or using an existing account, you will need your `AWS_ACCESS_KEY_ID` and
`AWS_SECRET_ACCESS_KEY`.

We'll be using resources which are outside of the free tier, but we'll be destroying everything at the end of the
night...this whole thing will at most cost a few cents.

If you have any questions please @ mention me in our Slack group in the `#noco-aws-meetup` channel. If you're not a
member, you can sign up here: [https://tinyurl.com/nocotech](https://tinyurl.com/nocotech)
