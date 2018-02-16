# HackerCamp-Summer-2018-Submission---API-

This repository contains #TweetFilter, a RESTful API for live streaming of #TwitterFeed and filtering the tweets for any Data Analysis purpose.

## Requirements
* [Sign Up](https://twitter.com/) for a Twitter Account.
* Create a new Consumer Key, Consumer Secret, Access Key and Access Secret in the [Developers](https://developer.twitter.com/) section.
* An application written in Python 2.7
* Uses Flask which could be installed by running the requirements command(follow the installation steps).
* Set up MongoDB by following the documentation in the respective websites
  * [Mac OS](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
  * [Ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
* (Optional) Set up [Postman](https://www.getpostman.com/) or any other similar tools to hit the APIs.

## Installation
* Git Clone or Download the repository.
* Open Terminal inside the TweetFilter folder and run the following command to install the requirements for running the service:
```python
pip install -r requirements.txt
```
* Run the following command in the terminal to set up the mongo server:
```python
mongod
```
* Open another terminal inside the TweetFilter directory and run the following command to start the service:
```python
python main.py
```

## Documentation
Complete documentation and instructions are available at: https://documenter.getpostman.com/view/3710139/tweetfilter/RVfwir4S

## License
The TweetFilter RESTful API is licensed under [MIT License](https://opensource.org/licenses/MIT). Copyright (c) 2018 TweetFilter.

## Author
Krishna Dwypayan Kota
