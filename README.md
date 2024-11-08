# Auto Recon
Author: Kevin Li / Anduril Industries
Date: 2024-10-29
Version: 0.0.1

## Description

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

Follow the guide [here](https://dev.tdm.anduril.com/docs/guide/generate-http-sdks) to generate your Python HTTP SDK






*** We currently use `anduril-python` for `StreamEntityComponents` in the `EntityManagerAPI` within the gRPC SDK, when the corresponding component is added to the REST SDK, we will migrate this business logic over to utilize the REST SDK instead ***

Installation of the `anduril-python` dependency requires your SSH key be added to your keychain: 

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

```bash
pip install -r requirements.txt
```

#### Run the program

> Modify the configuration file in `var/config.yml`, add your Lattice Bearer Token

```bash
python3 src/main.py --config var/config.yml
```

