# Coding Style Checking

It ensures [PEP8](https://www.python.org/dev/peps/pep-0008/) coding style.

1. Get into the api container

    ``` bash
    docker exec -it fastapi-fullstack_api_1 /bin/bash
    ```

2. Check everything

    ``` bash
    pycodestyle .
    ```


3. Automatic correction

    ``` bash
    black .
    ```