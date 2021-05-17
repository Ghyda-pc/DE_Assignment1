This application convert CSV to JSON using Apache Nifi
you can run it on your machine by following these steps:

1-you have to get the yml file up and run all images using:
docker-compose up -d 

2- now nifi is exist on local port 8080
on your brower >> localhost:8080/nifi/

3- to upload the templete "TEST1"
right click in any empty space >>
choose "upload template" >>
select the XML file "TEST1" 

4- select "TEST1" templete 
drag and drop templete >> 
select "TEST1" templete >> 
ADD

5- start the work flow from the operate in left side of the window 

6- then your CSV (in_nifi folder) will be converted to JSON file in (out_nifi folder)
