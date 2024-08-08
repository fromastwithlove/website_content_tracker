# Website content tracker

The project involves developing a tool or system that monitors the content of a specified website or webpage and alerts the user whenever any changes or updates are detected on that page.

### Requirements

python: 3.12

### Installation

1. `python3.12 -m venv venv`
2. `venv/bin/python -m pip install --upgrade pip`
3. `venv/bin/python -m pip install -r requirements.txt`

### How to run and debug the script locally

Start a local server:
`cd tmp && python3 -m http.server 8000`

Execute the script:
`venv/bin/python tracker.py`

## Deploy and run it using [monit](https://mmonit.com/monit/documentation/monit.html#Program) on the server

Make script executable:
`sudo chmod +x tracker.py`

Configure monit in `monitrc`:

```
## Check custom program status output.
#
  check program stadt-koeln-tracker with path "/home/adil/website_content_tracker/venv/bin/python /home/adil/website_content_tracker/tracker.py"
     if status != 0 then alert
#
#
```
