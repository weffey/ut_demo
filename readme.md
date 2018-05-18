# Setup

Reference: [Get started with a Virtual Environment](https://virtualenvwrapper.readthedocs.io/en/latest/)

1. Create a virtual environment called `ut_demo`
```bash
$ mkvirtualenv ut_demo
```

2. Grab the repo from Github
```bash
$ git clone https://github.com/weffey/lwc_unit_tests.git
```

3. Enter the folder
```bash
$ cd lwc_unit_tests
```

4. Install the requirements
```bash
$ pip install -r requirements.txt
```

5. Setup the database
```bash
$ python db_setup.py
```

6. Start the falcon app
```bash
$ gunicorn --reload look.app
```

7. Confirm the Falcon app comes up
```bash
$ curl -v localhost:8000
```