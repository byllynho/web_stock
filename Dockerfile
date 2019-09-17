FROM python:3.6

#RUN pip install pipenv && pipenv install --system

RUN mkdir -p /opt/services/djangoapp/
WORKDIR /opt/services/djangoapp/
COPY requirements.txt /opt/services/djangoapp/

RUN pip3 install -r /opt/services/djangoapp/requirements.txt

COPY . /opt/services/djangoapp/

RUN cd app && python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "app", "app.wsgi:application"]
