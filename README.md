# Auto Recon
Author: Kevin Li / Anduril Industries
Date: 2024-10-29
Version: 0.0.1

## Description
This is a sample application showcasing how to use Lattice HTTP SDKs to perform Entity Auto Reconnaissance.

The program streams incoming entities with the Entities API, determines if there is any non-friendly track within a certain distance from the asset, and if so, classifies the track disposition as suspicious and creates an investigation task.

The following endpoints are showcased in this application:
- the `long_poll_entity_events` Entities API endpoint to long poll for incoming entities.
- the `put_entity_override_rest` Entities API endpoint to override certain entity fields.
- the `create_task` Tasks API endpoint to create new tasks.
- the `get_task_by_id` Tasks API endpoint to retrieve tasks.

## How to run locally

#### First clone the repository

```bash
git clone https://github.com/anduril/ext-auto-recon.git ext-auto-recon
cd ext-auto-recon
```

> Optional: Initialize a virtual environment
> ```bash
> python -m venv .venv
> source .venv/bin/activate
> ```

Ensure you have a local version of Python with a version of 3.9 or higher

#### Install dependencies

Follow the guide [here](https://docs.anduril.com/guide/generate-http-sdks) to generate your Python HTTP SDK.

Navigate to the `requirements.txt` file and change the path to the SDKs according to where you have outputted the `entities_api` and `tasks_api` packages. After updating these paths, run the following command:

```bash
pip install -r requirements.txt
```

Modify the configuration file in `var/config.yml` by adding your Lattice IP and your Lattice Bearer Token.

#### Run the program

You can run the program by running the following command:

```bash
python3 src/main.py --config var/config.yml
```

Navigate to your Lattice UI and observe the `Active Tasks` tab. When assets come within range of a non-friendly track, an investigation task will be created if it hasn't been done so already.

To further experiment, you can right-click anywhere in the Common Operational Picture, and select `Add object > Track`. Create a track with a non-friendly disposition. When an asset comes within range of this track, you will see the disposition change to `DISPOSITION_SUSPICIOUS`, and an investigation task will be created.