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
pip install pandas numpy matplotlib seaborn yfinance apache-airflow pendulum
```
google-cloud-bigquery
Create a requirements.txt file to ensure that you have the necessary dependencies to run this code:

```
python -m pip freeze > requirements.txt
```

Note: I needed to run the following separately to get my script to run locally:

```
python -m pip install --upgrade pip
pip install --upgrade google-cloud
pip install --upgrade google-cloud-bigquery
pip install --upgrade google-cloud-storage
pip install pyarrow
```

Create a file for the project's Python script(s):

```
mkdir src
cd src
echo > main.py
```

# 1. Find a REST API you like as a data source.

API for this project: [yfinance](https://pypi.org/project/yfinance/)
- Allows you to download market data from Yahoo! Finance's API

# 2. Build a short script that reads that REST API and initially dumps to a CSV file

```py
# main.py
import os
import time
import datetime
import timeit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

SCRIPT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
print(f"script directory: {SCRIPT_DIR}")

start_of_script_time = (

    timeit.default_timer()

)

today = datetime.date.today()
delta = datetime.timedelta(days=1)

tix = ['BTC-USD', 'ETH-USD', 'SOL-USD']
start = today - delta
end = today

data = yf.download(
    tickers=tix,
    period='1d',   # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    interval="1h", # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    start=start,
    end=end,
)

data = data['Adj Close']
data.index = pd.to_datetime(data.index)
data.reset_index(inplace=True)

data_melted = pd.melt(
    data,
    id_vars=['Datetime'], # id
    value_vars=['BTC-USD', 'ETH-USD', 'SOL-USD'], # values are in these 3 columns
    var_name='Ticker', # name of the category in value_vars
    # NOTE: I was having issues in BigQuery when this was 'Adj Close'
    value_name='Price' # what the tickers are measuring
)

# Temporary: Write to .csv
data_melted.to_csv(os.path.join(SCRIPT_DIR, f"{today}.csv"), index=False)

print("The Modeling Script has finished running.")

print(

    f"Entire Script Runtime (Minutes): {(timeit.default_timer() - start_of_script_time) / 60:.2f}"

)  # make sure to remove from final version of document

```

Run the Python script:

```
cd src
python main.py
```

# 3. Get a Snowflake or BigQuery free trial account. Update the Python script to dump the data there.

SnowFlake: [SnowFlake 30-DAY FREE TRIAL](https://signup.snowflake.com/developers)
BigQuery: [Cloud data warehouse to power your data-driven innovation](https://cloud.google.com/bigquery?utm_source=google&utm_medium=cpc&utm_campaign=na-US-all-en-dr-bkws-all-all-trial-b-dr-1707554&utm_content=text-ad-none-any-DEV_c-CRE_665665924750-ADGP_Hybrid+%7C+BKWS+-+MIX+%7C+Txt-Data+Analytics-BigQuery-KWID_43700077225652791-kwd-33969409261&utm_term=KW_bigquery-ST_bigquery&gad_source=1&gclid=CjwKCAiArfauBhApEiwAeoB7qBpcnnTN6jh0wxjSh8YvCeOOGPiylq9TEqgM07QqJEUYiYO84TY4uhoCzT4QAvD_BwE&gclsrc=aw.ds)

I decided to go with BigQuery for this project.

Instructions on setting up BigQuery:
1. Try BigQuery Free -> Agree & Continue -> Start Free
- Directions: Write down information from current project 'My First Project'
    - Number: 519376080243
    - ID: turnkey-timer-416503

2. Open BigQuery Studio
- Directions: Search bar -> BigQuery

3. Create a Dataset
- Directions: turnkey-timer-416503 -> 3 dots -> Create dataset
- Details: 
    - ID: crypto_dataset_v1
    - Location type: Multi-region 
    - Default table expiration: Enable table expiration, 90 days

4. Create a Table
- Directions: crypto_dataset_v1 -> 3 dots -> Create table
- Details: 
    - Source: Empty table
    - Destination: 
        - Table: popular_coins
    - Schema: See Below

```sql
[
    {
        "name": "Datetime",
        "type": "DATETIME",
        "mode": "REQUIRED",
        "description": "Date and period of day, by hour"
    },
    {
        "name": "Ticker",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Name of security"
    },
    {
        "name": "Price",
        "type": "FLOAT",
        "mode": "NULLABLE",
        "description": "Price of the security at the period's close"
    }
]
```

Note: Because we did not upload any data yet, in popular_coins -> 'PREVIEW', you will see 'There is no data to display'

5. Provide user credentials for your Google Account

Note: When your code is running in a local development environment, such as a development workstation, the best option is to use the credentials associated with your user account.

To provide your user credentials to ADC for a Google Account, you use the Google Cloud CLI:

- Install and initialize the gcloud CLI.

    - Download the [Google Cloud CLI installer](https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe)

        - After installation is complete, the installer gives you the option to create Start Menu and Desktop shortcuts, start the Google Cloud CLI shell, and configure the gcloud CLI. Make sure that you leave the options to start the shell and configure your installation selected. The installer starts a terminal window and runs the gcloud init command.

        - After logging in, you will see something such as "Pick cloud project to use: [1] canvas-aviary-333005, [2] turnkey-timer-416503, [3] Enter a project ID, [4] Create a new project"
            - I selected '2'

        - More troubleshooting help can be found [here](https://cloud.google.com/sdk/docs/install)

- Create your credential file:

    ```
    gcloud auth application-default login
    ```

    - A sign-in screen appears. After you sign in, your credentials are stored in the [local credential file used by ADC](https://cloud.google.com/docs/authentication/application-default-credentials#personal).

        - Windows: %APPDATA%\gcloud\application_default_credentials.json

        - ie. [C:\Users\Myles\AppData\Roaming\gcloud\application_default_credentials.json]

    - Copy that .json file, paste it into the root directory of this repository, and rename it `key.json`.



Finally, we are ready to update the Python script to interact with our BigQuery account.

Replace the lines of code where you dump to .csv with these instead:

```py
# main.py
# data_melted.to_csv(os.path.join(SCRIPT_DIR, f"{today}.csv"), index=False)
# data_melted.to_csv(os.path.join(SCRIPT_DIR, f"{today}.csv"), index=False)

from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../key.json" #Service account key file path

MY_PROJECT_ID = "turnkey-timer-416503"
MY_DATASET_ID = "crypto_dataset_v1"
MY_TABLE_ID = "popular_coins"
table_id = f"{MY_PROJECT_ID}.{MY_DATASET_ID}.{MY_TABLE_ID}"

os.environ["GCLOUD_PROJECT"] = MY_PROJECT_ID
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

schema = [
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.schema.SchemaField
    bigquery.SchemaField(
        name="Datetime",
        field_type=bigquery.enums.SqlTypeNames.DATETIME,
        mode='REQUIRED'
    ),
    bigquery.SchemaField(
        name="Ticker",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode='REQUIRED'
    ),
    bigquery.SchemaField(
        name="Price",
        field_type=bigquery.enums.SqlTypeNames.FLOAT64,
        mode='NULLABLE'
    ),
]

# Create dataset/table, if it doesn't exist already
try:
    dataset = client.create_dataset(MY_DATASET_ID)
    print(f"Created dataset {MY_DATASET_ID}")
except:
    print(f"Dataset {MY_DATASET_ID} already exists")

try:
    table_ref = client.dataset(MY_DATASET_ID).table(MY_TABLE_ID)
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)
    print(f"Created table {MY_TABLE_ID}")
except:
    print(f"Table {MY_TABLE_ID} already exists")

# Dump data from yfinance into table
dataframe = data_melted.copy()

# https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-dataframe
job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    
    schema=schema,
    
    # Optionally, set the write disposition. BigQuery appends loaded rows
    # to an existing table by default, but with WRITE_TRUNCATE write
    # disposition it replaces the table with the loaded data.
    
    # write_disposition="WRITE_TRUNCATE",
)

job = client.load_table_from_dataframe(
    dataframe,
    table_id,
    job_config=job_config
)  # Make an API request.

job.result()  # Wait for the job to complete.

table = client.get_table(table_id)  # Make an API request.

print(
    "Loaded {} rows and {} columns to {}".format(
        dataframe.shape[0], dataframe.shape[1], table_id
    )
)

print(
    "There are now {} rows and {} columns in {}".format(
        table.num_rows, len(table.schema), table_id
    )
)
```


Run the Python script:

```
cd src
python main.py
```

Now that the data has successfully been uploaded to 'turnkey-timer-416503.crypto_dataset_v1.popular_coins', go into Google BigQuery and look at your data:
- Directions: turnkey-timer-416503 -> crypto_dataset_v1 -> popular_coins -> 'PREVIEW'

Note: Since this is the first time you have run the script, you should see 72 rows of data (given that the above script still pulls 24 rows of data for 3 different coins)

# 4. Build aggregations on top of the data in SQL (using things like GROUP BY keyword)

Let's build our aggregations on this data.

1. Begin by creating a temporary table:

How to write/run in BigQuery:

```sql
BEGIN TRANSACTION;

CREATE TABLE turnkey-timer-416503.crypto_dataset_v1.my_temp_table_prices_from_past_week AS
SELECT
  Datetime,
  Ticker,
  Price
FROM `turnkey-timer-416503.crypto_dataset_v1.popular_coins`
WHERE datetime <= CURRENT_DATETIME()
AND DATETIME_ADD(Datetime, INTERVAL 24*7 HOUR) >= CURRENT_DATETIME();

COMMIT TRANSACTION;
```

How I decided to write/run queries instead: Using Python!

```py
# main.py
# Add logic to run SQL queries

# Perform a query.
QUERY_CREATE_TABLE_PRICES_FROM_LAST_WEEK = (
    'CREATE OR REPLACE TABLE turnkey-timer-416503.crypto_dataset_v1.prices_from_past_week AS '
    f'SELECT Datetime, Ticker, Price FROM `{MY_PROJECT_ID}.{MY_DATASET_ID}.popular_coins` '
    'WHERE datetime <= CURRENT_DATETIME() '
    'AND DATETIME_ADD(Datetime, INTERVAL 24*7 HOUR) >= CURRENT_DATETIME()' # final '' has no whitespace
)
print(f"QUERY 1: {QUERY_CREATE_TABLE_PRICES_FROM_LAST_WEEK}")
query_job = client.query(QUERY_CREATE_TABLE_PRICES_FROM_LAST_WEEK)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)
    
QUERY_CREATE_TABLE_CALCULATED_HOURLY_RETURNS = (
    'CREATE OR REPLACE TABLE turnkey-timer-416503.crypto_dataset_v1.calculated_hourly_returns AS '
    'SELECT Datetime, Ticker, Price, ((Price / lag(Price, 1) OVER (PARTITION BY Ticker ORDER BY Datetime)) - 1)* 100 AS hourly_return '
    f'FROM `{MY_PROJECT_ID}.{MY_DATASET_ID}.prices_from_past_week` '
    'Order by Ticker, Datetime'
)
print(f"QUERY 2: {QUERY_CREATE_TABLE_CALCULATED_HOURLY_RETURNS}")
query_job = client.query(QUERY_CREATE_TABLE_CALCULATED_HOURLY_RETURNS)  # API request
rows = query_job.result()  # Waits for query to finish

QUERY_CREATE_TABLE_MAX_HOURLY_RETURNS = (
    'CREATE OR REPLACE TABLE turnkey-timer-416503.crypto_dataset_v1.max_hourly_returns AS '
    'SELECT Ticker, MAX(hourly_return) as max_return '
    'FROM `turnkey-timer-416503.crypto_dataset_v1.calculated_hourly_returns` '
    'GROUP BY Ticker '
    'ORDER BY max_return DESC;' # final '' has no whitespace
)
print(f"QUERY 3: {QUERY_CREATE_TABLE_MAX_HOURLY_RETURNS}")
query_job = client.query(QUERY_CREATE_TABLE_MAX_HOURLY_RETURNS)  # API request
rows = query_job.result()  # Waits for query to finish

```

Now, our aggregations are saved as tables, and we simply need to make a request to their new table to get our aggregations.

1. Aggregation #1 - Take the data from the last week, this will become a line graph.

```sql
SELECT * FROM turnkey-timer-416503.crypto_dataset_v1.prices_from_past_week;
```

2. Aggregation #2 - Aggregate the data from the past week so we see the top performing hourly return for each Ticker.

```sql
SELECT * FROM turnkey-timer-416503.crypto_dataset_v1.max_hourly_returns;
```

Good work!

Note: There may be duplicates of data being created due to running the same queries multiple times, this can be handled in 2 ways:
1. SELECT DISTINCT using the timestamp in all of our views
2. Identify duplicates by hand
- Create a SELECT statement to identify unique values.
- Materialize the result to a new table.

# 5. Set up an Astronomer account to build an Airflow pipeline to automate this data ingestion

Astronomer: Astro is a unified data platform built on Apache Airflow that ensures data is delivered on time, securely, and accurately.

Crash course on Airflow:
- [An introduction to Apache Airflow](https://docs.astronomer.io/learn/intro-to-airflow)
- [Airflow operators](https://docs.astronomer.io/learn/what-is-an-operator)
- [Introduction to Airflow DAGs](https://docs.astronomer.io/learn/dags)
- []()


Directions:
1. Login to Astronomer
- https://www.astronomer.io/ -> Log in -> Continue with GitHub -> Authorize astronomer
- https://cloud.astronomer.io/welcome -> Start a Free Astro Trial -> Create Organization
    - Organization Name: Myles Thomas
    - Workspace Name: Temp Workspace
    - How familiar are you with Apache Airflow? 'Researching Airflow as a solution'
    - Why are you signing up for an Astro trial? 'Personal learning and development'

2. Create a Deployment
- https://cloud.astronomer.io/ -> Deployments
    - Name: Deployment1
    - Description: my first deployment
    - Cluster: Standard Cluster
    - Provider: Google Cloud
    - Region: us-central1
    - Execution: Celery Executor
    - Advanced: Make sure 'Contact Emails' is up-to-date ie. mylescgthomas@gmail.com

3. Install the Astro CLI

- What this does: Gives us a full local development environment

- Instructions:

    - [Step 1: Install the Astro CLI](https://docs.astronomer.io/astro/first-dag-cli?tab=windowswithwinget#install-the-astro-cli)
        - Make sure you have the following: 
            - Winget installed: winget --version
            - Enable Hyper-V:
                - Check if you have it already done: Command Prompt -> systeminfo.exe
                    - If not, continue.
                - Enable Virtualization Technology & Data Execution Prevention (DEP) in BIOS:
                    - Restart the computer and repeatedly press one of these keys: F2, F10, F8, F12 or Del* when the computer manufacturer's logo appears on the screen to enter the BIOS/UEFI settings (* The key may vary from manufacturer to manufacturer)
                    - Enable Virtualization in BIOS:
                        - Intel CPU: Click the Advanced* tab and set the Virtualization aka "Intel® Virtualization Technology (VT-x)" to Enable.

                - Enable Data Execution Prevention (DEP) in BIOS:
                    - Control Panel -> System and Security -> System -> Advanced system settings -> Performance -> Settings -> Data Execution Prevention -> Turn on DEP

                - 10 more steps continue [here](https://www.wintips.org/how-to-enable-hyper-v-on-windows-10-11-home/) ........

            - The latest version of the [Windows App Installer](https://apps.microsoft.com/detail/9nblggh4nns1?hl=en-ca&gl=ca)
            - Windows 10 1709 (build 16299) or later or Windows 11. (Duh)

        - Open Windows Powershell (as admin) and run the following command:

            ```
            winget install -e --id Astronomer.Astro
            ```

        - Next, restart your computer. Then, run the following command to access the location of the CLI executable:

            ```
            $env:path.split(";")
            ```

        - Copy this path
            - It should look like this: C:\Users\myname\AppData\Local\Microsoft\WinGet\Packages\Astronomer.Astro_Microsoft.Winget.Source_8wekyb3d8bbwe

        - Paste the path into File Explorer or open the file path in terminal, then rename the Astro executable to astro.exe

        - Run astro version to confirm the Astro CLI is installed properly.

            ```
            astro version
            ```

        - Note: To Upgrade the Astro CLI:

            ```
            winget install -e --id Astronomer.Astro
            ```

    - [Step 2: Create a Deployment](https://docs.astronomer.io/astro/first-dag-cli?tab=windowswithwinget#step-2-create-a-deployment)
        - I have already done this step above!

    - [Step 3: Create an Astro project](https://docs.astronomer.io/astro/first-dag-cli?tab=windowswithwinget#step-3-create-an-astro-project)
        - Open terminal/command line.
        
        - Create a new folder for your Astro project (for now, put it in your current repo/project):

            ```
            cd data_engineering_project
            mkdir first_astro_project
            ```

        - Open the folder:

            ```
            cd first_astro_project
            ```

        - Run the following Astro CLI command to initialize an Astro project in the folder:

        ```
        astro dev init
        ```

        - Note: This command generates the following files in your folder:

            ```
            .
            ├── .env # Local environment variables
            ├── dags # Where your DAGs go
            │   ├── example-dag-basic.py # Example DAG that showcases a simple ETL data pipeline
            │   └── example-dag-advanced.py # Example DAG that showcases more advanced Airflow features, such as the TaskFlow API
            ├── Dockerfile # For the Astro Runtime Docker image, environment variables, and overrides
            ├── include # For any other files you'd like to include
            ├── plugins # For any custom or community Airflow plugins
            │   └── example-plugin.py
            ├── tests # For any DAG unit test files to be run with pytest
            │   └── test_dag_example.py # Example test that checks for basic errors in your DAGs
            ├── airflow_settings.yaml # For your Airflow connections, variables and pools (local only)
            ├── packages.txt # For OS-level packages
            └── requirements.txt # For Python packages
            ```
    
    - [Step 4: Deploy example DAGs to your Astro Deployment](https://docs.astronomer.io/astro/first-dag-cli?tab=windowswithwinget#step-4-deploy-example-dags-to-your-astro-deployment)
        - DAG-only deploys are an Astro feature that you can use to quickly update your Astro Deployment by only deploying the dags folder of your Astro project.
            - You'll now trigger a DAG-only deploy to push your example DAGs to Astro.

        - Run the following command to authenticate to Astro on the CLI:

            ```
            astro login astronomer.io
            ```

        - After running this command, you are prompted to open your web browser and enter your credentials to the Cloud UI. (Login with GitHub)
            - The Cloud UI then automatically authenticates you to the CLI.
            - The next time you log in, you can run astro login without specifying a domain.
            - If you run into issues logging in, check to make sure that you have the latest version of the Astro CLI.

        - Run the following command to deploy your DAGs to Astro:

            ```
            astro deploy --dags
            ```

        - This command returns a list of Deployments available in your Workspace and prompts you to confirm where you want to deploy your DAG code.
            - Select '1' for Deployment1

        - After you select a Deployment, the CLI parses your DAGs to ensure that they don't contain basic syntax and import errors.
            - If your code passes the parse, the Astro CLI deploys your DAGs to Astro.

    - [Step 5: Trigger your DAG on Astro](https://docs.astronomer.io/astro/first-dag-cli?tab=windowswithwinget#step-5-trigger-your-dag-on-astro)

        - Newly-deployed DAGs are paused by default and will not start running automatically.
            - To run one of the example DAGs in your Astro project according to its schedule, you must unpause it from the Airflow UI hosted on your Deployment.

        - In the Deployment page of the Cloud UI, click the Open Airflow button.
            - ie. Deployments -> Deployment1 -> 'Open Airflow'

        - In the main DAGs view of the Airflow UI, click the slider button next to example-dag-basic to unpause it. If you hover over the DAG, it says DAG is Active. When you do this, the DAG starts to run on the schedule that is defined in its code.

        - Optional: Manually trigger a DAG run of example-dag-basic by clicking the play button in the Actions column. When you develop DAGs on Astro, triggering a DAG run instead of waiting for the DAG schedule can help you quickly identify and resolve issues.
            - After you press Play, the Runs and Recent Tasks sections for the DAG start to populate with data.

        - Click on the name of the DAG, example-dag-basic, to open the Grid view for the DAG.
            - To see if your DAG ran successfully, the most recent entry in the grid should have green squares for all of your tasks.
        
        - Pause your DAG by clicking the slider button next to example-dag-basic.
            - This prevents your example DAG from running automatically and consuming your Deployment resources.

    - [Step 6: View your DAG status in the Cloud UI](https://docs.astronomer.io/astro/first-dag-cli?tab=windowswithwinget#step-6-view-your-dag-status-in-the-cloud-ui)

        - The Cloud UI shows you information about the health of your Deployment, including analytics and logs for your DAG runs.

        - Go back to your Deployment page in the Cloud UI. Because you ran your example DAG, your Deployment information page now has data about your Deployment and DAG runs. The following example shows an example of what you might find in the Overview page for your Deployment.

            - When you're done exploring, you can delete your Deployment from the More Options menu on your Deployments page.

    
    

4. Deploy a DAG
- What this does: Deploys DAGs from our local development environment to the production Airflow environment in the cloud
- Instructions:
    - We have done this already in the previous step.
        - Now we need to make our own DAG and deploy it!

5. Add DAGs
- Additional help: https://docs.astronomer.io/astro/cli/develop-project#add-dags

- Instructions:
    - Create a new `.py` file and save it to the `dags` folder
        - You can start by copy/pasting `.py`, if you want a good start for an ETL script.
        - My filename: `my_first_dag.py`

    - Add the same logic that you created in the initial `main.py` file that is interacting with BigQuery.
        - 

    - Now that your dag is ready for testing, let's setup Docker.

6. Download Docker
- Link: https://docs.docker.com/
- What is Docker: Docker is an open platform for developing, shipping, and running applications.
    - Docker packages software into standardized units called containers that have everything the software needs to run including libraries, system tools, code, and runtime
        - which means that developers can easily ship their applications to other environments without having to worry about dependencies or configuration issues.

- Instructions:
    - https://docs.docker.com/desktop/install/windows-install/ -> Docker Desktop for Windows
    - 
    - Restart Computer
    - 
    
docker ps

7. Deploy your DAG
- Instructions:
    - Make sure you are logged in:

        ```
        astro login astronomer.io
        ```

    - Make sure we are in the right workspace:

        ```
        astro workspace list
        ```
        
        - You should see 'Temp Workspace', as that is what we named it at the start.

    - Deploy:

        ```
        astro deploy
        ```
        
        - Select '1' for 'Deployment1'

    - Check on your deployment in the UI:
        - There are links you can copy/paste
        - Deployment1 should be 'Deploying'
            - This means it is currently installing the Docker image onto the Airflow environment
            - In a few minutes, the Deployment should be 'Healthy' and we will be able to see the DAGs we pushed to this airflow environment


8. Monitor
- Instructions:
    - Go back to your Cloud UI
    - Click 'Get Analytics' on your deployment screen
        - You will now see the DAG runs/tasks runs over the time period you choose!
        - You will also see workers CPU utilization rate


WARNING: Airflow is designed to handle orchestration of data pipelines in batches, and this feature is not intended for streaming or low-latency processes. If you need to run pipelines more frequently than every minute, consider using Airflow in combination with tools designed specifically for that purpose like Apache Kafka.

# 6. Connect something like Tableau to your data warehouse and build a fancy chart that updates to show off your hard work!



---

# References:

1. [TechTrapture - Load and extract data in BigQuery using Python](https://www.youtube.com/watch?v=RO6roY6nwlA)
2. [Google Cloud - Load data from DataFrame](https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-dataframe)
3. [How to select records from last 24 hours using SQL?](https://stackoverflow.com/questions/1888544/how-to-select-records-from-last-24-hours-using-sql)
4. [BEGIN TRANSACTION](https://cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language)
5. [Create a temporary table](https://cloud.google.com/bigquery/docs/multi-statement-queries#create_temporary_table)
6. [Perform a query](https://cloud.google.com/python/docs/reference/bigquery/latest/index.html)
7. [Error Response without leveraging CREATE OR UPDATE](https://stackoverflow.com/questions/3825990/http-response-code-for-post-when-resource-already-exists)
8. [When to use Kubernetes Executor](https://forum.astronomer.io/t/when-to-use-kubernetes-executor/1289)
9. [How to Get Started with Astro!](https://www.youtube.com/watch?v=Gvw1QZ4oUiw&t=45s)
10. []()
11. []()
12. []()
13. []()

