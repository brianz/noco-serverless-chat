Hi everyone,

I sent this out over email last week but wanted to put it here for new folks who are RSVPing and didn't get it.

Thanks for RSVPing for our first hands-on workshop. I think this will be fun. I'll also fully admit that workshops
like this are notoriously tough since there are always varying degrees of familiarity with tooling, languages, 
AWS concepts, etc. We should be a fairly small group, so I'm hopeful that we can work through any issues which pop up. 
I'm going to be working on the code this weekend...we'll be building a (very basic) chat application, all with 
serverless technologies. Think Slack, without any extra features. 

To set yourself and me up for success, please get the prerequisites out of the way ASAP. If you can try to do this 
over the weekend it'll give you some buffer in case you hit any snags.

We'll be using the Serverless framework to deploy all of our code. I have a Docker image which has Serverless and 
the associated tooling already installed and ready to go. 

**If you are running MacOS or Windows, I strongly encourage using Docker!**

1. Install Docker: https://www.docker.com/products/docker-desktop
1. Once Docker is running, pull down my image: "docker pull brianz/serverless"

If anyone is running a Linux laptop, it'd be easiest to install Serverless on your system. See the Serverless docs for 
installation.

The other big thing you'll need is an AWS account. These accounts are free to create but you do need to provide a 
credit card. If you don't have an account just click the "Create an AWS Account" button in the upper right.

Whether you're creating a new account or using an existing account, you will need your `AWS_ACCESS_KEY_ID` and 
`AWS_SECRET_ACCESS_KEY`.

We'll be using resources which are outside of the free tier, but we'll be destroying everything at the end of the 
night...this whole thing will at most cost a few cents.

If you have any questions please @ mention me in our Slack group in the `#noco-aws-meetup` channel. If you're not a
member, you can sign up here: [https://tinyurl.com/nocotech](https://tinyurl.com/nocotech)

Looking forward to this!
