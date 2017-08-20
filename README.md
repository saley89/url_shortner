# Url Shortener - David Sale

Written in Python 3.6.1 using a Redis database.

## Setup

- Ensure `redis-server` is installed on your system. For MacOS:
```
$ brew install redis
```

For debian based OS:

```
$ apt-get install redis-server
```

- Ensure you using Python 3.6.1 or make a virtualenv for the project such as:
```
$ mkvirtualenv -p python3 url_shortner
```

- install requirements

```
$ pip install -r requirements.txt
```

- run the build and ensure all passing

```
$ fab build
```

- run the server standalone from testing. You will find task `runserver` and `stop_server` which take care of 
starting up redis and the web application using gunicorn. 

```
$ fab runserver
$ fab stop_server
```

## Scaling

The application is setup to be executed using the industry standard Gunicorn web server.  I have already placed some
basic tuning of the server in `gunicorn_conf.py`. This includes running multiple workers based on the number of CPU's 
available to the running application. I've also switched to the gevent worker type which is async in design, allowing 
for higher throughput through the server versus the default sync worker type.

With more time, I would dockerize the application, creating a `Dockerfile` to install the application and setup any
dependencies.  We could then setup the application with as many running instances as required in a cloud setup such as 
kubernetes.  I would undertake non functional testing using JMeter or Gatlin to understand the load one node could take in
terms of transactions per second (TPS), memory and CPU usage. This would allow us to scale to expected TPS as required.

Of course, the database would require scaling also.  I would recommend running a redis cluster of nodes to allow for 
downtime or outages of nodes and still being able to serve traffic. It would also provide redundancy of data so that we 
don't experience data loss should any of the nodes go down.


## Example API usage:
```
Request:
    POST http://localhost:8000/shorten_url

    body:
    {
        "url": "www.helloworld.com"
    }

Response: 
    Status code: 201
    response_body:
    {
        "shortened_url": 'http://www.your_service.com/ouoYFY48'
    }
```


`http://localhost:8000/ouoYFY48` -> 302 Redirect to www.helloworld.com