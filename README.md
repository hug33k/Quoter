# Quoter

![](misc/logo.png)

> What did you just said ?

A Slack integration to show quotes

## How to use it ?

#### Step 1 : Generate quotes

Make friends, tell nonsense and take note of what made you laugh.

#### Step 2 : Save your quotes

````sh
$> mkdir quotes
$> cd quotes/
$> mkdir random_topic
$> cd random_topic
$> echo "Insert quote here" > myfirstquote.quote
````

You can create multiple folders in `quote` folder, so if you want to integrate Quoter into multiple Slack, it will be easier.

#### Step 3 : Run Quoter

If you use Docker :

````sh
$> docker pull hug33k/quoter
$> docker run -d --name Quoter -p YOUR_PORT:80 -v /path/to/my/quotes:/app/quotes hug33k/quoter
````

If you use `docker-compose.yml`:

````yaml
version: "3"

services:

  quoter:
    container_name: Quoter
    image: hug33k/quoter
    ports:
     - YOUR_PORT:80
    volumes:
     - /path/to/my/quotes:/app/quotes
    restart: always	
````

If you don't have or hate Docker : 

````sh
$> export QUOTER_PORT=YOUR_PORT
$> git clone git@github.com:hug33k/Quoter.git
$> cd Quoter/
$> pip install -r requitements.txt
$> python server.py
````

#### Step 4 : Slack integration

- Go to [Slack API Webpage](https://api.slack.com/apps) and click on `Create New App`
- Add a name ( "Quoter" is a nice name, isn't it ? ) and select a workspace
- Go in `Slash Commands` section and add your command
- The URL request will be the location of the previous Docker container. To select a folder created in step 2, you need to add `?folder=FOLDER_NAME` at the end of your URL
- In `OAuth & Permissions`, click on `Install App`

#### Step 5 : Enjoy

Now you can use the command you set in previous step and have fun !

#### Step 6 : What can I do with my command ?

- Without argument, it will send a random quote avaiable in selected folder
- `list` will list the available quotes
- `show <QUOTE_NAME>` will show the selected quote
- `help` will show you the help message
