# Vorboss Code Test

Airtable code test. Note that this code test is _highly_ incomplete. In its current state the app doesn't run, and there are some issues with the Dockerfile as well copying the env from the `build` image to the `dev` image. Similarly, the plotting frontend is incomplete and plots do not render correctly. At best this is a sketch of the direction I intended to take, but strictly speaking it does not meet any of the requirements of the initial test.

## Requirements 
- This repo
- A valid API token with read permissions. The Docker setup is incomplete but would expect this to be an environment variable. The code base was mostly the result of experiments in the REPL and read the API token from disk.

While incomplete, the next sections provide a brief architecture overview.

### AirtableClient
This class is meant to encapsulate the Airtable database and expose one or more filtering endpoints. I found `pyairtable` which provides a programmatic interface for talking to the Airtable backend. The purpose is to allow for structured querys to be made from within the `dash_app` which would render a view of the output.

Records are returned as lists of dictionaries. Some filtering facilities are possible with the `pyairtable` API. For instance, each filtering by field or by formula. There are some helper structures to construct formulas, but only a subset of all airtable formulas are implemented in the python package. To use the complete set of formulas (including date formulas) the raw formula string needs to be constructed and passed to a `pyairtable` `API` object.

Architecturally filtering is hugely important in reducing bandwidth consumption, as the alternative is to fetch the entire table each time. While this is possible in this toy example, in general this will become the largest performance bottleneck.


### dash_app.py 
I decided to use `plotly` for the display as its the closest to any technology that I am already familiar with (in this case, `matplotlib`). Plotly serves up graphs from a flask-based web service. You provide a render function that returns a plot and this is drawn in the server. The idea was to have a different plot for each display "category". In this context, a category would be a particular view of the data, for instance, revenue for a given month or product category, number of in progress orders, and so on. A dropdown would select the category, and the render callback would return the corresponding graph.


### Docker 
In the current `docker-compose.yml` there is a single service, but in theory the same image could be use to serve an Airtable API client and a dash app seperately. This might  be useful for example if there are multiple dashboards that all read from a common client (or perhaps even a pool of clients). This is left unimplemented.


### Other notes 
There is no secrets mechanism. I initially tried out the API in a REPL directly and had a copy of my API token in a text file which I read from disk to initialize a client. Another common way to do this is through an environment variable (the `docker-compose.yml` implies this). Neither of these is particularly good security practice, however I felt that this issue was somewhat outside the scope of the task and left it as is. 
