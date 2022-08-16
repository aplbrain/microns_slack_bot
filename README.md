<p align="center">
  <img src="https://github.com/nikood/microns_slack_bot/blob/main/figures/clear_logo.png" />
</p>

# MICrONS Slack Bot
Microns slack bot sends updates on the progress of the MICrONS (Machine Intelligence From Cortical Networks) project in the Slack channels it has been added to or even direct messages.

* **This bot sends daily update at 11:00 AM EST to the "proofreading-bot" channel in the MICrONS Slack channel**
![alt text](https://github.com/nikood/microns_slack_bot/blob/main/figures/daily.png)

* **When the bot is mentioned in a group with a message containing the word "update" (ex. "@MICrONS Bot send update!"), the bot sends a summary of the recent updates to the user**

![alt text](https://github.com/nikood/microns_slack_bot/blob/main/figures/update.png)

* **It can also send a graph that depicts the summary of the data to the user. All you need to do, is again mention the bot with a message containing one of the following:** "graph", "chart", "plot", "figure", "draw", "Graph", "Chart", "Plot", "Figure", "Draw"
Example: "@MICrONS Bot send a graph please!" or "@MICrONS Bot draw"**

![alt text](https://github.com/nikood/microns_slack_bot/blob/main/figures/draw.png)
![alt text](https://github.com/nikood/microns_slack_bot/blob/main/figures/zoom.png)

* **You rather receive updates and graphs directly and not in a group channel? No worries! The bot can also be accessed through direct messages to provide the same updates!**

## Installation

Clone this repo using:
```
$ git clone https://github.com/nikood/microns_slack_bot.git
```
                      
In order for the slack bot to function 24/7 without having to keep the script open and running on your local computer, set up a **virtual machine** and then run the code with **tmux**. 

Additionally, the project's .env file was not shared in this repository for security reasons, but in order for this Python module to function, the developer's Slack app and bot tokens must be saved in an .env file in the same directory as final_bot.py.


## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

