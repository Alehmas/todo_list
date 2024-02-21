# TODO List

## Technologies used
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

##  Description
The Todo application is a simple task management tool designed to help users organize their tasks effectively. With this application, users can create, update, and delete tasks, mark tasks as completed

### Features
- Create new tasks with titles, descriptions.
- Edit existing tasks to update their details.
- Mark tasks as completed.
- Delete tasks that are no longer needed.
- Filter tasks based on various status.
- User authentication and authorization.

### User roles and permissions
**What unauthorized users can do**
- None

**What authorized users can do**
- Retrieve a list of tasks
- Retrieve a list of own tasks
- Retrieve details of a specific task
- Create/edit/delete your own task
- Filter tasks by tags status
- Set status of specific task is completed
- Create/refresh JWT token
- Create/edit/delete your own user


## Run the project locally
### Clone the repository
Clone the repository to your local machine:
```bash
git clone git@github.com:Alehmas/todo_list.git
```

Move to a new directory
```bash
cd todo_list/
```

### Launching and working with the project
**Step 1** Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/Scripts/activate
```

**Step 2** Create an _todo_list/todo/todo/.env_ file with the touch .env command and add environment variables to it:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<your_django_secret_key>
```
To ensure the safety of the project, after adding .env to `setting.py`, you must remove the *default* values ​​in the variables.

**Step 3** Update pip and install dependencies:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Step 4** From the directory with the file `manage.py` run the migrations:
```bash
python manage.py migrate
```

**Step 5** Create a superuser:
```bash
python manage.py createsuperuser
```

**Step 6** Project launch:
```bash
python manage.py runserver
```

**Step 6** Fill out the database using APi endpoints

##  Project Applications
All applications of the project are covered by tests.
To run the tests you need to call from the `todo_list/todo/` directory
```
python manage.py test -v {0,1,2,3}
```
*where 0 means no details, 3 means maximum information.

## Specification
You can see the full API specification:
- To view the entire specification, you can use a ready-made specification stored in the file _todo_list/todo/schema.yaml_ and use the [online editor Swagger](https://editor.swagger.io/). 
- Use [Swagger](http://127.0.0.1:8000/swagger/) online documentation 
- Use [ReDoc](http://127.0.0.1:8000/redoc/) online documentation 

## Development plans for Todo List
- _Timeframe for completing tasks:_ Provide users with the ability to set deadlines for tasks.
- _Task Prioritization:_ Introduce the ability for users to prioritize tasks by adding priority levels (e.g., high, medium, low) or assigning numerical values to tasks to indicate their importance.
- _Task Reminders and Notifications:_ Implement reminders and notifications to alert users about upcoming task deadlines or incomplete tasks. Users could receive notifications via email, SMS, or push notifications.
- _Collaboration and Sharing:_ Enable users to collaborate on tasks and share task lists with other users or teams. This could involve implementing features like task assignment, commenting, and real-time collaboration.
- _Advanced Filtering and Sorting:_ Enhance the filtering and sorting capabilities to allow users to filter tasks based on various criteria such as due date, priority, category, or assigned user. Implement advanced search functionality to help users find specific tasks quickly.
- _Integration with Calendar and Scheduling Tools:_ Integrate the Todo list application with popular calendar and scheduling tools like Google Calendar, Outlook, or Apple Calendar. This allows users to sync tasks with their existing calendars and manage their schedules more efficiently.
- _Mobile App Development:_ Develop native mobile applications for iOS and Android platforms to provide users with a seamless mobile experience.
- _Web service development:_ Adding functionality for accessing the service from a personal computer.

## Authors
- [Aleh Maslau](https://github.com/Alehmas)
