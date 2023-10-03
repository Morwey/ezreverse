Here is a brief manuel for Python shiny app deplotment

### Deploy to shinyapps.io (cloud hosting)

##### 1. Installing Shiny for python

For both virtual and conda environments, the Shiny package can be easily installed. In a conda environment, you can create a Shiny environment and install or update the Shiny app using the code provided below.

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

Check this link for more information: [Shiny for Python - Installing Shiny for Python](https://shiny.posit.co/py/docs/install.html)

##### 2. Download VScode and Shiny for Python extension

To better visualize and check in real-time, it's recommended to download the Shiny extension for **VScode**. 

Use the link below to download the **Shiny extension** for your VSCode. In the sidebar of VScode you can turn it on and off.

[Shiny for python extension](https://marketplace.visualstudio.com/items?itemName=posit.shiny-python)

##### 3.create an To deploy shiny in shinyapps.io

Create an account via [shinyapps.io](https://www.shinyapps.io/)

