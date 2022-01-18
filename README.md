# Score-Predictor

  &emsp; IPL Score Predictor is a web app built using azure web app services to predict total runs scored by the batting team when score within the first 10 overs is given. First, the batting team and the bowling team should be chosen from the given list of consistent teams. Then the runs scored and wickets taken at the specified over must be provided. Finally the score at the previous 5 overs should be given to get the total runs scored by the batting team after 20 overs.
 &emsp; The application is built primarily using flask framework and HTML, CSS and Javascript for the front-end. I have used linear regression model to train and test the dataset which gave a reasonable accuracy of 68%. 
 &emsp; The application is hosted and deployed in Azure using web app and app services. I have create a resource group called ipl-crics to hold and manage the resources. The application is built in python with Python 3.8 as runtime stack. The app is deployed from the Github repository with github actions as build provider.
  &emsp; This application can be used by the team management to choose the best fit player. This project will majorly help the audience to know the winning chances of their favorite team. This project can be extended to predict score in other formats of matches including ODI and Test matches. 
  
  Demo URL: https://ipl-crics.azurewebsites.net
