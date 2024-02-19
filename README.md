##### Initializing the project locally

1. We use pipenv to manage package dependencies.
    - If you want to initalize a pipenv environment, (if there's no pipfile yet)
        `pipenv install --python /usr/bin/python3.7`
        - Make sure you have python3.6 installed in that location. ;) 
        
    - If you already have a pipfile in the project
        `pipenv install`


##### Steps to run locally.

1. You need to tell dynaconf where the configurations reside.
    `export ROOT_PATH_FOR_DYNACONF='camp/config'`
2. You also need to export FLASK_APP so dynaconf knows the application.
    ` export FLASK_APP='camp:create_app()' `
3. Activate the virtual env using pipenv
    `pipenv shell`

**Tip: Check if configurations are proper by running `flask routes`**   


##### Steps to docker mongo locally.
1. You need to pull mongo image
    `docker pull mongo`
2. To run mongo image
    `docker run --name mongo -p 27017:27017 -d mongo`
3. To check the running container
    `docker ps`
4. To see all the container both running and stopped
    `docker ps -a`
5. To execute mongo queries and access database in shell
    `docker exec -it <container_id> mongo`

