# Steam-game-recommendation
Project Discription

Overview

This solution enables you to create a program to recommend Steam game app for various users. This recommendations system is based on the following models:
1.	Popularity Recommendations: For the new user, we will recommend top-10 popular games according to the data in both history and recent two weeks. 
2.	Item-based Recommendations: This is the "Customers who liked this product also liked these other products" scenario. We develop a model to discover the new customers for a game app by calculating the similarity of the games apps based on a linear algorithms.
3.	Content-based Recommendations: We analyzed the content and rating of the game by unstructured text analysis technique, and find the predicted game apps for various given users.
4.	ALS(Alternating Least Squares Method) Recommendations: By using a Matrix Factorization approach we decompose the large user/item matrix into lower dimensional user factors and item factors, which can train model and predict the results fast. We recommended 100+ games for each user (5000+users) 

All the recommendation results were saved in to SQL tables.  A WebApp has been built to fetch these SQL tables and show the recommended games. 

![alt text](http://url/to/img.png) 
Software environments:

The program needs to be run in a python 3 environments. (Python 3 installation: https://www.python.org/downloads/) 

Meanwhile, the following libraries were used and some of them need to be installed:
(1)	Numpy and Pandas
(2)	Scikit-learn
(3)	Json
(4)	NLTK(Natural Language Toolkit)
(5)	SQLAlchemy
(6)	Spark

A SQL software also need to be installed such as my SQL (https://www.mysql.com/)

The program and data

The data folder contains the all data we used in this program. Some of them were acquired from custom and some of them were from the Steam Web. 

The Py folder contains all the code: 

(1)	‘get_data_from_web.py ‘ is the coding to crawl the data by APT from Steam Web.

(2)	‘recommendation by ALS.py’ and ‘recommendation by users content and popularity.py’ are the coding to build the recommendation models. 
