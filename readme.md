# Setup

Reference: [Get started with a Virtual Environment](https://virtualenvwrapper.readthedocs.io/en/latest/)

1. Create a virtual environment called `ut_demo`
```bash
$ mkvirtualenv ut_demo
```

2. Grab the repo from Github
```bash
(ut_demo)$ git clone https://github.com/weffey/lwc_unit_tests.git
```

3. Enter the folder
```bash
(ut_demo)$ cd lwc_unit_tests
```

4. Install the requirements
```bash
(ut_demo)$ pip install -r requirements.txt
```

5. Setup the database
```bash
(ut_demo)$ python db_setup.py
```

6. Start the falcon app
```bash
(ut_demo)$ gunicorn --reload look.app
```

7. Confirm the Falcon app comes up
```bash
$ curl -v localhost:8000
```

-----

# Branches

- `step-0-setup`: App starts, 2 tests pass
- `step-1-input-validation`: App starts, 2 tests pass, 2 tests fail
- `step-2-input-sanitization`: App starts, 4 tests pass, 2 tests fail