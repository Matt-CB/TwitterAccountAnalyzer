# __Twitter Account Analyzer Documentation__


<p align="center">
  <img src="images/BannerTwitter.png" alt="twitter" width="1000">
</p>

## You can use it in this link: 
Deploy in streamlit: https://matt-cb-twitteraccountanalyzer-app-xbf2h3.streamlit.app/
Deploy en hugging face: https://huggingface.co/spaces/Matt-CB/TwitterAccountAnalyzer (Change the theme to dark mode for better visibility.)



The Twitter Account Analyzer is an web application that allows you to analyze and generate tweets. It provides functionalities for __sentiment analysis__, __emotion detection__, and __identifying the main topic__ of tweets in a a __multilingual__ way. Below is a detailed and easy-to-understand documentation for the project.

## Repository Structure 

The repository contains several files and folders that are necessary for the functioning of the analyzer. Here's a description of each of them:

- `.env`: This file contains the environment variables and libraries required for running the project.
- `.images`: This folder contains the Twitter logo used the user interface.
- `.tweets`: This folder stores all the generated and analyzed tweets.
- `app.py`: This is the main file of the project. It contains the main code of the application, including the user interface and the logic for tweet generation and analysis.

## Requirements and Dependencies

Make sure you meet the following requirements and have the following dependencies installed to run the Twitter Account Analyzer:

- [Python 3.7 or higher.](https://www.python.org/downloads/)
- The following Python libraries:
   - [`openai`](https://pypi.org/project/openai/)
   - [`dotenv`](https://pypi.org/project/python-dotenv/)
   - [`nltk`](https://pypi.org/project/nltk/)
   - [`transformers`](https://pypi.org/project/transformers/)
   - [`mtranslate`](https://pypi.org/project/mtranslate/)
   - [`pandas`](https://pypi.org/project/pandas/)
   - [`streamlit`](https://pypi.org/project/streamlit/)
   - [`Pillow`](https://pypi.org/project/Pillow/)

You can install the dependencies by running the following command in your virtual environment:

pip install -r requirements.txt

## Configuration

Before running the application, you need to configure some environment variables in the `.env` file. Make sure to provide the OpenAI API key in the `OPENAI_API_KEY` variable. This key is required to use the OpenAI API for tweet generation.

Additionally, the application allows you to select the language for tweet generation and analysis through a user interface. You can choose from the following languages: German, Spanish, French, English, and Italian.

## Using the Application

Once you have properly configured the environment and environment variables, you can run the application using the following command:

streamlit run app.py


This will start the application and open the user interface in your web browser.

# User Interface

The user interface of the application consists of two columns. The first column displays the title and the Twitter logo, while the second column contains the configuration parameters and analysis results.

In the second column, you will find the following elements:

__API KEY::__ Here you should place the key you obtained from OpenAI to use it in the tweet generator..  

__Username:__ A text field to enter the username of the Twitter account you want to analyze.  

__Number of Tweets:__ A slider to select the number of tweets to be generated and analyzed.  

__Maximum Tokens:__ A slider to select the maximum number of tokens allowed in each generated tweet.  

__Randomness:__ A slider to adjust the level of randomness in tweet generation.  

__Sentiments:__ A dropdown menu to select the type of sentiments you want to analyze in the tweets. You can choose from "All", "Positive", "Neutral", and "Negative".  


Once you have selected the configuration parameters, you can click the "Analyze" button to start analyzing the Twitter account.

#### __Tweet Generation and Analysis__
After clicking the "Analyze" button, the application will perform the following tasks:

. __Tweet Generation__: Using the OpenAI API, the application will generate the specified number of tweets for the provided Twitter user. The generated tweets will be related to a randomly selected main topic and express a specific emotion with high intensity.

. __Identifying the Main Topic__: The application will analyze the generated tweets and determine the main topic. This is done by analyzing the most frequent words and identifying relevant nouns.

. __Translation of Tweets__: If the selected language is not English, the generated tweets will be translated to English using the mtranslate library. This is done to facilitate sentiment analysis

. __Translation of Tweets__: If the selected language is not English, the generated tweets will be translated to English using the mtranslate library. This is done to facilitate sentiment analysis and emotion detection, as the classification models used primarily support the English language.

. __Sentiment Analysis__: The generated tweets will be analyzed to determine the sentiment associated with each tweet. Language-specific sentiment classification models will be used for each selected language.

. __Emotion Detection__: In addition to sentiment analysis, the application will detect the emotions present in each tweet, if it says "Neutral," it's because there are too many emotions colliding, and it doesn't specify one in particular.




. Language-specific emotion classification models will be used for each selected language.

__Analysis Results__
Once the analysis is complete, the application will display the following results:

__Account__: The username of the analyzed Twitter account.
__Main Topic__: The main topic identified in the generated tweets.
__Sentiment Table__: A table displaying the generated tweets, the detected sentiment, and the associated sentiment score.
__Emotion Table__: A table displaying the generated tweets, the detected emotion, and the detected sentiment.
