# Author: Oana Florean

# Open Targets Platform Bioinformatician Code Test 

# This script queries the Open Targets REST API (https://docs.targetvalidation.org/programmatic-access/rest-api),
# it fetches association_score.overall data for a given target or disease id, it parses the output, prints it and its analysis to the stdout.

# Uses python 3.8.5
# Needs: 
# pip install pandas
# pip install requests


# Instructions/examples to run code in a unix-like machine:

# python OT_testOana.py -t ENSG00000197386  
# python OT_testOana.py -d Orphanet_399 


import requests
import sys
import pandas as pd


# The API REST call broken down as server+path and query parameters.

api_url = "https://platform-api.opentargets.io/v3/platform/public/association/filter" 
score_filter = "&size=10000&fields=target.id&fields=disease.id&fields=association_score.overall" 


# Show instructions if arguments are not complete.

if len(sys.argv) < 3:
	print("You need to provide at least 3 arguments" + "\n"+ 
		"   For the association_score.overall of a target please provide -t flag and the specific target" + "\n"+ 
        "      E.g. python OT_testOana.py -t ENSG00000197386" + "\n"+ 
        "   For the association_score.overall of a disease please provide -d flag and the specific disease" + "\n"+  
        "      E.g. python OT_testOana.py -d Orphanet_399")
	exit(1)


# Parse command-line parameters and prepare full API url. Exit if unsuccessful.

search_type = sys.argv[1]
search_value = sys.argv[2]

if search_type == "-t":
    url = api_url + "?target=" + search_value + score_filter
elif search_type == "-d":
    url = api_url + "?disease=" + search_value + score_filter
else: 
    print("Only -t and -d flags are supported")
    exit(1)


# Fetch response with filter query and check if successful.

response = requests.get(url)
if response.status_code != 200:
	print("Unsuccesul request")
	exit(1)

response_data = response.json()["data"]


# Check if requested search_value was found.

if len(response_data) == 0:
	print("Cannot find data for your request")
	exit(1)


# Transform json into pandas data frame. Print all data frame with new columns order.

data = pd.json_normalize(response_data)
pd.set_option("display.max_rows", None)
data = data[["target.id", "disease.id", "association_score.overall"]]
print (data)


# Print analysis.

min = data["association_score.overall"].min()
max = data["association_score.overall"].max()
mean = data["association_score.overall"].mean()
std = data["association_score.overall"].std()

print("")
print("Maximum: ", max)
print("Minimum: ", min)
print("Average: ", mean)
print("Standard Deviation: ", std)
