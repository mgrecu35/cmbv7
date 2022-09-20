from urllib.request import urlopen
from bs4 import BeautifulSoup
from netCDF4 import Dataset
# Fetch the html file
i=2
url='https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L2/GPM_2BCMB.07/2018/%3.3i/'%i
response = urlopen(url+'contents.html')
html_doc = response.read()

# Parse the html file
soup = BeautifulSoup(html_doc, 'html.parser')
ic=0
files=[]
for l in soup.get_text().split("\n"):
    if "2B" in l and "HDF5" in l and "xml" not in l:
        print(l)
        files.append(l)
        ic+=1
fh=Dataset(url+files[-1].strip())
