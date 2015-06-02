# udacity-tournament-planner

This is the course project of the Udacity course "Intro to Relational Databases"

This is a Python module which uses the PostgreSQL database to keep track of players and matches in a game tournament. 

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible. 

How to Run (copied from https://github.com/DawoonC/dw-tournament-planner)

First, you need to install VirtualBox and Vagrant on your machine.

Then, you'll need to clone this repo to your local machine.

Go to the vagrant directory in the cloned repository, then open a terminal window and type vagrant up to launch your virtual machine. This will take some time in your first run, because it needs to install some dependencies.

Once it is up and running, type vagrant ssh to log into it. This will log your terminal in to the virtual machine, and you'll get a Linux shell prompt.

Copy the tournament directory in this repository and paste in the vagrant directory. This will overwrite the existing tournament directory.

Type the following commands on your virtual machine: cd /vagrant/tournament -> psql -> create database tournament; -> \c tournament -> \i tournament.sql -> \q

Finally, you can now run the tests for the project by typing python tournament_test.py on your virtual machine. The test results will be displayed on your terminal.
