* [docker cp <containerId>:/file/path/within/container /host/path/target](http://stackoverflow.com/questions/22049212/docker-copy-file-from-container-to-host)
* [docker cp foo.txt mycontainer:/foo.txt](http://stackoverflow.com/questions/22907231/copying-files-from-host-to-docker-container)
* [Elasticsearch: Five Things I was Doing Wrong](http://gibrown.com/2013/01/24/elasticsearch-five-things-i-was-doing-wrong/)

## What I did wrong
1. Don't create indexes named "events", "reports", etc. Create "events-MMDDYYYY" and _alias_ it as "events"

