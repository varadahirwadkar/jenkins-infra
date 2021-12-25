# Importing libraries
import os.path
import requests
requests.urllib3.disable_warnings()
from bs4 import BeautifulSoup

# vars
BUILDS = []
URL    = "https://ppc64le.ocp.releases.ci.openshift.org"
SOUP   = BeautifulSoup(requests.get(URL, verify=False).content, "html.parser")
OLD_BUILDS = []


if os.path.isfile("builds.txt"):
    with open("builds.txt","r+") as f:
        OLD_BUILDS = f.readlines()

# getting all stable builds till now
def get_current_stable_build():
    cnt = 0
    for tag in SOUP.findAll('tbody'):
        if cnt > 1 and cnt <= 5:
            for build in tag.findAll("tr"):
                my_build = []
                for col in build.find_all("td"):
                    if col.text != "" :
                        if col.find('a') != None and not col.text.strip().startswith("ppc64le"):
                            new_url = URL+col.find('a').get('href')
                            my_build.append(new_url)
                        my_build.append(col.text.strip())
                # print("registry.ci.openshift.org/ocp-ppc64le/release-ppc64le:"+my_build[1])
                # print(my_build[3])
                BUILDS.append(my_build)
                if my_build[2] != "Accepted":
                    print(my_build[2])
                else:
                    break
        cnt=cnt+1

  
# print(my_build)
get_current_stable_build()
with open("builds.txt","w+") as f:
    for build in BUILDS:
        f.write(build[1]+"\n")

for build in BUILDS:
    if build[1] +"\n" not in OLD_BUILDS:
        with open("latest_build.txt","w+") as lf:
            print(build[1])
            lf.write(build[1]+"\t"+ build[1][0:build[1].index(".0-0.nightly")] +"\n")
        break