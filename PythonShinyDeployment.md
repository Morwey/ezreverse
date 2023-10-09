Here is a brief manuel for Python shiny app deployment

### Deploy to shinyapps.io (cloud hosting)

#### 1. Download VScode and Shiny for Python extension

To better visualize and check in real-time, it's recommended to download the Shiny extension for **VScode**.

Use the link below to download the **Shiny extension** for your VScode. In the sidebar of VScode you can turn it on and off.

[Shiny for python extension](https://marketplace.visualstudio.com/items?itemName=posit.shiny-python)

#### 2. Installing Shiny for python and build basic shiny app

First create a new directory for your first Shiny app, and change to it.

```shell
mkdir myapp
cd myapp
```

Next, for both virtual and conda environments, the Shiny package can be easily installed. In a conda environment, you can create a Shiny environment and install or update the Shiny app using the code provided below.

```shell
# Create a conda environment named 'myenv'
conda create --name myenv
# Activate the virtual environment
conda activate myenv

# Install shiny
conda install -c conda-forge shiny
# Update shiny
conda update -c conda-forge shiny
```

To creat and run a basic shiny app, run:

```shell
#This should creat a basic shiny app named `app.py`
shiny create .

# This should start your app and sutomatically launch a web browser
shiny run --reload
```

Then, launch the `app.py` file you created, using VS Code with the Shiny extension activated. This will open a subpage for your app, facilitating simultaneous coding and checking.
*Check this link for more information: [Shiny for Python - Installing Shiny for Python](https://shiny.posit.co/py/docs/install.html)*

#### 3.create an account and deploy shiny in shinyapps.io

First, Create an account via [shinyapps.io](https://www.shinyapps.io/)

Second, to deploy a Python Shiny app on shinyapps.io, adhere to the following steps:

```shell
# install esconnect-python package
pip install rsconnect-python

# log in your shinyapps.io account and replace the information below
rsconnect add --account <ACCOUNT> --name <NAME> --token <TOKEN> --secret <SECRET>
rsconnect deploy shiny /path/to/app --name <NAME> --title my-app
```


