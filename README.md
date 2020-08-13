# web-scraping-challenge

before running app.py:<br>
In gitbash:
> conda activate PythonData
> "C:\Program Files\MongoDB\Server\4.4\bin\mongod.exe"<br>
Open MongoDB Compass
- select "localhost:27017" under recent connections on the left
- Click "Connect" (green button)

To run app.py:
In gitbash:
> conda activate PythonData         <!-- if you haven't already -->
> cd <path to where app.py lives>
> python app.py
...
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) <!-- user can click on http link to open a new browser -->

Once the browser is open:
* user can click the scrape button to get the most recent mars data
* another browser will open and navigate to multiple pages, collecting the data
* this process can take a minute or two DO NOT close the new browser
* once the data is collected the new browser will close on its own
* finally, the homepage will automatically reload with the new data
