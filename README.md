# Personal-Financial-App
App for weekly, monthly check personal financial

Send mail contain Monthly Financial Report to user

# Tech Stack

Front-end: ReactJS

Back-end: Django

Database: PostgresSQL

Celery + Redis: Redis is middle-man to transfer task, worker of Celery receive task from Redis and implement

## Future Feature: Deploy on basic AWS

AWS S3 : Front-end

AWS EC2 : Back-end

AWS RDS: Databse PostgresSQL

# Flowchart

![image](https://github.com/user-attachments/assets/3689cb50-4fbe-4313-9825-369cbd5e217a)



# System Requirements

- **Operating System**: Windows  
- **Dependencies**:
  - Docker Desktop
  - WSL 2 (Windows Subsystem for Linux)

---

## 1. Install Docker Desktop

1. Download and install Docker Desktop from:  
   https://www.docker.com/products/docker-desktop/  
2. During the installation wizard, **select “Use WSL 2”** instead of “Hyper‑V”.  
3. Once installed, launch Docker Desktop.  
4. In Docker Desktop, go to **Settings → Resources → WSL Integration** and enable integration with your WSL 2 distributions.

---

## 2. Clone the Project

Open PowerShell or your WSL terminal and run:

```bash
# Clone repository and navigate into it
git clone https://github.com/lnguyend-agai/Personal-Financial-App.git
cd Personal-Financial-App
```

## 3. Start the container

In the root of project, run:

```bash
docker-compose up -d
```

Check the containers that are running:

```bash
docker ps
```

### Docker Desktop result when run successfully

![Docker Desktop](https://github.com/user-attachments/assets/80dd534b-e747-48b6-8d66-7b57dc062a92)

### Click on container with port 3000, this is the front-end, the result is 

![Frontend View](https://github.com/user-attachments/assets/21b69197-0f04-451e-b4ae-661b0f120df0)

## Stop container

```bash
docker-compose down
```

## Delete volumes (database)

```bash
docker-compose down -v
```

## Rebuild the container
```bash
docker-compose build
docker-compose up -d
```

# User Interface

## User input the Transaction
![image](https://github.com/user-attachments/assets/c324e8d4-b93d-4367-b76a-9309d9f810d9)

## Show Monthly and Daily Transaction
![image](https://github.com/user-attachments/assets/975d13f9-4fc3-445e-b0c8-085036853cf7)

## Send Monthly Report to User
![image](https://github.com/user-attachments/assets/a88498e4-e6eb-46ff-87fb-d0213684c9f3)

# Fake database

Use the Faker library to create a big database. This for learn in-memory and load balancing

![image](https://github.com/user-attachments/assets/d4796b92-b8a4-4170-8b7b-42202a752015)







