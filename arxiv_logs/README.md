The idea:

Process all read from arxiv, detect the papers that have
mulitple (seveal days) sustained and increasing read rate.
Import those into a private library.


Input data:

Anonymized logs are in: 

/proj/ads/abstracts/sources/ArXiv/alsoread/

There are some post-processing scripts inside:

/proj/ads_abstracts/config/links/alsoread_bib

This use case is also a test for time series database:

InfluxDB:

 - https://github.com/BushnevYuri/DockerGrafanaInfluxKit


