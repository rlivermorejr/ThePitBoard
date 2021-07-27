# <p style="text-align: center">Welcome to the Pit Board</p>
<p style="text-align:center">
This is a website created by three students at Kenzie Academy
<br />
Russell Livermore, Chris Davis, Andy Robles, and Daniel Ratzlaff
<br />
(Initial idea created by Andy Robles)
</p>

<p style="font-size: 12px">(This application uses a tool for dependency management and packaging called poetry. If you need a list of dependancies used, they are listed in the 'pyproject.toml' file.)
<br />
(You can use the command 'poetry install' to install all dependacies needed to run application.)
</p>
<br />

### To begin:
- you might need to run the command: <pre>python manage.py racerlist</pre>
  * this is to make sure you get the list of racers from the API, but since I have the database not in the gitignore file, it might already be loaded in.
- then run: <pre>python manage.py runserver</pre>
- open your web browser and go to <pre>https://127.0.0.1:8000</pre>

<br />
<hr />
<br />

## <u>Table of Contents:</u>
- <b>appuser</b> holds everything in regard to the user model. 
  * Handles displaying user profile, likes, followers/following, and drivers selected.
  * Handles editing the user profile .
- <b>authentication</b> folder holds everything regarding to logging in and out.
  * Has functions for login, logout, and create user.
- <b>conf</b> contains all setting and urls for django.
- <b>media</b> will have folders to hold uploads of picture and videos as well as profile pictures.
- <b>notification</b> handles all notifications.
- <b>post</b> has everything to handle posts.
  * It will handle likes for all posts.
  * Handles comments for posts as well and likes for comments.
  * Also has everything for deleting posts and comments.
- <b>raceapi</b> has all code for getting info from the API.
  * Contains a models for the racers and for race results.
  * Will pull all info needed from the API and insert it into the DriverStandingsModel.
  * Has the code for displaying the leaderboard and for tallying up points after a race is completed.