#Junior test project

##### How to install and use this webservice

1. Download this project from git as a zip-file
2. Unzip anywhere on your machine
3. You're done!


##### How to launch the service

1. Open command line
2. Go to the service directory
3. Type this command: docker-compose up
4. The server is running!

##### How to use the service

1. Go to http://localhost:8000, select "UPLOAD FILE" and upload a "deals.csv" file
2. If the file was uploaded correctly, then go to http://localhost:8000/data-view/ or click on the "SEE RESULTS" on the home page in order to see the result
3. You can also view the result in JSON format on the api side: http://localhost:8000/api/top-clients/


##### Warning:

- Use "deals.csv" file only. Others names and formats are unacceptable.
- The "deals.csv" file should contain 5 fields in strict order: "customer - username, item - the name of the item, total - the amount of money spent, quantity - the number of gems bought, date - the time when purchase happened."
- customer, item should be str type
- item, total should be int type
- date should be str type