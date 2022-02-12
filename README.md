## Web Apps using Plotly Dash
- The core of Dash:
  1. Flask: web server functionality.
  2. React.js: renders the web interface.
  3. Plotly.js: generates the interactive charts (The core of plotlly is D3.js).
### 1. Covid19 App
- [Source code](https://github.com/tuantla80/Plotly-Dash-Web-Apps/tree/master/Covid19%20App%20by%20Plotly)
- [Website on Heroku](https://covid-19-tracking-at-apf.herokuapp.com/) 
  ![plot](https://github.com/tuantla80/Plotly-Dash-Web-Apps/blob/master/Covid19%20App%20by%20Plotly/sample_data/DEMO.png)  
### 2. Sale Dashboard App
- [Source code](https://github.com/tuantla80/Plotly-Dash-Web-Apps/tree/master/Sale%20Dashboard%20App)  
  ![plot](https://github.com/tuantla80/Plotly-Dash-Web-Apps/blob/master/Sale%20Dashboard%20App/Sale%20dashboard%20demo.png)  
### 3. Deploy an app to Heroku  
- Step 1
  - Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)  
  - Install [git bash](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)  
  ``` 
  C:\Users\tuantla>git --version
  git version 2.28.0.windows.1

  C:\Users\tuantla>heroku --version
  »   Warning: heroku update available from 7.53.0 to 7.54.1.
  heroku/7.53.0 win32-x64 node-v12.21.0 
  ```  
- Step 2  
  [Sign up a Heroku account](https://signup.heroku.com/) and login with email and password  
- Step 3  
  - Add a new variable called server in app.py to run your app using a [WSGI server](https://www.python.org/dev/peps/pep-3333/). 
  ```
  app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
  server = app.server  
  ```  
- Step 4
  - Create 'runtime.txt' file with the below content to let Heroku automatically detect Python app and will use the correct buildpack.
  ```
  python-3.8.5
  ```
  - Create 'requirements.txt' file with the below content. You may need to use: pip freez > requirements.txt 
  ```
  dash==1.20.0
  plotly==4.14.3
  pandas==1.1.3
  gunicorn==20.0.4
  ```  
  gunicorn is a WSGI HTTP server that is frequently used for deploying Flask apps to production.  
  - Create 'Procfile' file with the below content. Note: Procfile with capital P and without extension  
  ```
  web: gunicorn app:server
  ```
  app above is name of python file (app.py) to run this application.  
  This file let Heroku app know what commands should be executed to start your app. In this case, it starts a gunicorn server for your dashboard.  
- Step 5.  
  - Initialize a Git repository in your project’s root directory. Using git command line as below.  
  ```
  > git init
  ```
  - Making .gitignore in the root directory. Example as below.
  ```
  *.pyc
  test_folder
  ```
  - Do the following common git command lines.  
  ```
  > git status
  > git add .
  > git commit -m "your comment"
  ```
- Step 6
  - Create an app in Heroku, push your code there using Git, and start the app in one of Heroku’s free server options
  ``` 
  > heroku create APP-NAME # Choose a name for your app
  > git push heroku master
  > heroku ps:scale web=1
  ```
  - Some others command lines may be helpful sometime  
  ```
  > heroku logout
  > heroku login
  > heroku apps
  > heroku plugins
  ```  
- Step 7. If modified code, do the following commands to update.  
  ```
  > git add . # add changes
  > git commit -m 'change description'
  > git push heroku master # deploy to Heroku
  ```   
  ### 4. Ref  
  - https://github.com/nicolaskruchten/scipy2021
