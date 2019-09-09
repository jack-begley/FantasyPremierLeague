# FantasyPremierLeague
Getting the data out of the FPL API (Python).

This is based around a console app for executing various methods.

The methods that have been constructed can also be extracted if needed for use in external applications.

# Python in a nutshell:

Python is a language used a lot in data science for manipulating large data sets, and creating applications that allow people to automate tasks that result in the generation of data. Because it is open source, there are 1000's of packages that have been created to allow people to do really specific tasks well.

Python as a language has built in garbage collection. This is important because it means that when a method is completed, all local data is cleared out (something I leared after hours of pulling my hair out). 

# Getting python set up:
Go to the [python website](https://www.python.org/downloads/) to download the most recent version of python onto your machine.

In order to run and develop this code you will need to use an IDE (Integrated Development Environment) - This is essentially a platform that allows you to write, compile (turn your code into the 1's and 0's that computing is based on) and test in the console.

My suggestion would be [Visual Studio Code](https://code.visualstudio.com/download). This is an open source piece of software created by Microsoft.

This means that the base product is created by Microsoft but many people have created a load of extensions for the products that allow you to do more powerful work with the product.

Best of all it is entirely free to use.

Finally, you will need to keep your code somewhere. You can always dump it on your local drive but that doesn't really allow you to have source control.

Source control is ensuring that there is a single source of truth in the code repository (the "repo"). 
The case of this FantasyPremierLeague Repo,  "master" is the single source of truth.
Source control protects people from making changes to the same piece of code and breaking each others work. 
Finally, it keeps a history of the changes made, and if it turns out someone accidentally makes a breaking change (a change that stops the code working) we can always roll those changes back.

GitHub allows us to manage source control really well. 
This is managed by Pull requests (see "Using GitHub") which allow us to send our code changes to the Repo and check our changes (e.g. one developer can check another developers code) and it will also test for conflicts in the code (these come up when 2 people have changed the same area of code)

To manage source control, I would suggest [creating a GitHub](https://github.com/join) account and downloading [GitHub Desktop](https://desktop.github.com/) - a desktop app that will allow you to:
* Manage any local changes to the code
* Create code branches (a seperate set of code from the "master" code that allows you to check your code changes)
* Create pull requests (ask to merge your code changes into the "master" and add just those changes in)

# Download Python:

This is pretty simple, go to the link at the top and download it. Click the ".exe" file and install it.

# Installing external Python packages:

Python as a language is open source (again, this means that people can develop packages or extensions to do some of the stuff you may want to do without you having to do the work yourself).

This does mean we have to install stuff ourself which is slightly annoying.

On the plus side, there is a python package installer (called ```pip```) which does the heavy lifting for you.

In order to install these packages you will need to:
1) Go to the python program file (normally it is somewhere like: ```C:\Users\[YourName]\AppData\Local\Programs\Python\Python37-32```)
2) When you are there in the file explorer , Go to "File" > "Open windows powershell" > "Open windows powershell as administrator"
3) Install pip using: ```python -m pip install -U pip```

Once this is set up and up to date, you can now install all the packages you want, using the format:

```pip install (package name)``` e.g: ```pip install csv``` which imports a load of methods for writing data to a csv

The names of the packages you will need to install are:
* pprint
* requests
* json
* argparse
* csv 
* zipfile
* pyodbc
* aiohttp
* asyncio
* unicodecsv
* urllib.request
* urllib.parse
* tkinter

# Setting up Visual Studio Code:

In order to set up visual studio code to be able to run Python, you will need to download some extensions. They can be found here on the left hand task bar.

You will want to download the extension called "Python" made by Microsoft (~62.5M downloads) - This will let you run python scripts.

For more info on how to download and manage extensions have a look [here](https://code.visualstudio.com/docs/editor/extension-gallery)

Once this has been installed, to test the compiler:
1) Create a new file
2) Save the file as a ".py" file e.g. MyScript.py
3) Add one line saying ```print("Hello World!)``` and save your script
4) Go to Debug --> Start with Debugging OR hit F5
5) In the bottom console, you should see "Hello World!" printed out

This process of Debugging allows you to run the program locally when testing and will throw errors (send an error message) when something is broken.

# Setting up GitHub Desktop and clone the repo

In order to work on the repository, you will need to clone it so you have a copy. This can be done in GitHub desktop.

1) First, install the program and log in with your GitHub handle/account.
2) Next, in the right hand area there is a dropdown called "Current repository". Under this area there is ANOTHER dropdown called "Add".
3) Under "Add" there is another option called "Clone repository...", click this
4) In the pop up, there is a tab called URL. Go here and paste in "https://github.com/jack-begley/FantasyPremierLeague.git"
5) Select a folder location that you want to keep this in ("C:\Repos" isn't a bad place to keep it)

This will now allow you to start working on the code.

# Creating branches and pull requests:
* **Branches** = a seperate section of the code that you are working on. This protects our single source of truth from having changes put straight into it and breaking the code that other people are using (this is called cowboying code in)
* **Committing changes** = you may do multiple pieces of work in one branch. A "Commit" is a single chunk of that work that performs one function. If you are working on multiple functions, it's work splitting these into seperate commits.
* **Pull request** = a request for someone to take a look at your code and make sure everything looks good before putting it into the live environment. This is one final check from someone that didn't create the code.

In GitHub desktop, you will want to create a new branch before making changes to master. This is ideally done before you start making changes to the code but if you forget to (like i do all the time), you can create a new branch before creating a pull request.

To create a new branch:
1) Go to "Branch" > "New Branch"
2) Give your branch a name - This is normally your name, followed by a short summary of the work you are going to do
  e.g. ```jack-begley/fixed-export-to-csv-issue```
  
To commit code changes to a branch:
1) First you will need to commit your changes to your branch. In the bottom left there is a single line text box, and a multi line text box.
2) In the single line box, type in a summary of the individual code changes you made in this commit (the single send of changes)
  *e.g. sorted issue with tabs not seperating*
3) In the multi line box give a more extensive summary
  *e.g. the data was not seperating into individual cells. The issue was that the tabs were not being read as the delimiter. I updated the code to have a seperate delimiter method that would work purely on this data set. The old comma seperated sets are still seperated correctly as this is an entierly new method*
4) Commit your changes to the branch with the button in the bottom left corner that has the word "Commit" in it

To create a pull request once you have done all the changes you need for that branch:
1) Go to "Branch" > "Create pull request"
2) If you haven't already, publish your branch to GitHub (it will prompt you to do this if you haven't)
3) It will load up GitHub in the browser, and there will be a green button that allows you to create a pull request - click this.
4) (Optional:) Assign another user to review your PR.

