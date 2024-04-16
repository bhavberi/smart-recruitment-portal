# Software Engineering 
## Project 3

> Team Numer: 12

### Team Members

| Name | Roll Number |
| --- | :---: |
| Bhav Beri | 2021111013 |
| Divij | 2021101001 |
| Harshit Aggarwal | 2021111015 |
| Jhalak Banzal | 2021101079 |
| Pranav Agrawal | 2021101052 |

---

----

### _Setup_

- Clone the main repository and submodules:
```
git clone 
```

- Pull latest changes for the submodules
```
cd 
```

- Run initialization script:
```
chmod +x init.sh
./init.sh
```

- Build and spin up all services
```
docker compose up --build
```
Use `-d` flag to run the services in detached mode (background).

- To stop the services (Without removing the MongoDB data)
```
docker compose down
```

To remove the containers and volumes, use the `-v` flag.