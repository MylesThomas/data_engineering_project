# Causal Inference Learning

---

# 0. Project Setup

Setup the local project directory via command line, and enter into that directory:

```
mkdir data_engineering_project
cd data_engineering_project
```

Head to Github and create a new remote repository named `data_engineering_project`.

Following the creation of your new remote repository, create a new local repository on the command line:

```
echo "# data_engineering_project" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/MylesThomas/data_engineering_project.git
git push -u origin main
```

Create a .gitignore file for the project:

```
echo > .gitignore
```

Code to copy/paste for the .gitignore file: https://github.com/github/gitignore/blob/main/Python.gitignore

Next, setup a virtual Python environment:

```
py -m venv env
```

You should now see a folder 'env' with a python.exe program in the /Scripts directory.

Activate the virtual environment in the terminal:

```
.\env\Scripts\activate
```

Note: Remember that you can always leave the virtual environment with this call:

```
deactivate
```

Install the necessary packages into your virtual environment:

```
pip install pandas numpy matplotlib seaborn yfinance
```

Create a requirements.txt file to ensure that you have the necessary dependencies to run this code:

```
python -m pip freeze > requirements.txt
```

Create a file for the project's Python script:

```
echo > main.py
```

# 1. Find a REST API you like as a data source.

API for this project: [yfinance](https://pypi.org/project/yfinance/)
- Allows you to download market data from Yahoo! Finance's API

# 2. Build a short script that reads that REST API and initially dumps to a CSV file



Run the Python script:

```
python main.py
```

# 3. Get a Snowflake or BigQuery free trial account. Update the Python script to dump the data there.

SnowFlake: [SnowFlake 30-DAY FREE TRIAL](https://signup.snowflake.com/developers)
BigQuery: [Cloud data warehouse to power your data-driven innovation](https://cloud.google.com/bigquery?utm_source=google&utm_medium=cpc&utm_campaign=na-US-all-en-dr-bkws-all-all-trial-b-dr-1707554&utm_content=text-ad-none-any-DEV_c-CRE_665665924750-ADGP_Hybrid+%7C+BKWS+-+MIX+%7C+Txt-Data+Analytics-BigQuery-KWID_43700077225652791-kwd-33969409261&utm_term=KW_bigquery-ST_bigquery&gad_source=1&gclid=CjwKCAiArfauBhApEiwAeoB7qBpcnnTN6jh0wxjSh8YvCeOOGPiylq9TEqgM07QqJEUYiYO84TY4uhoCzT4QAvD_BwE&gclsrc=aw.ds)

I decided to go with BigQuery for this project.

Instructions on setting up BigQuery:
1. 
2. 
3. 

...

Replace the lines of code where you dump to .csv with these instead:

```py
# main.py

```


Run the Python script:

```
python main.py
```

# 4. Build aggregations on top of the data in SQL (using things like GROUP BY keyword)



# 5. Set up an Astronomer account to build an Airflow pipeline to automate this data ingestion



# 6. Connect something like Tableau to your data warehouse and build a fancy chart that updates to show off your hard work!