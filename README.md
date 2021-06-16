## Web Apps using Plotly Dash
- The core of Dash:
  1. Flask: web server functionality.
  2. React.js: renders the web interface.
  3. Plotly.js: generates the interactive charts (The core of plotlly is D3.js).
### 1. Covid19 App
### 2. Deploy an app to Heroku  
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
  - Create file 'runtime.txt' with the below content to let Heroku automatically detect Python app and will use the correct buildpack.
  ```
  python-3.8.5
  ```
  - 
  

