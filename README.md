# course-notes

[![Accessibility Checks](https://github.com/DS-100/course-notes/actions/workflows/a11y.yml/badge.svg)](https://github.com/DS-100/course-notes/actions/workflows/a11y.yml)

This was built with [Jupyter Book (MyST flavor)](https://jupyterbook.org/en/stable/intro.html). 

## Structure

Only two things need to be edited.
- `myst.yml`: Configuration information about the textbook. Modify this file for things like:
    - changing the logo or favicon;
    - adding or removing launch buttons;
    - changing information about the book.
    - table of contents (section, chapter numbering and order)
- `content/`: Content of the textbook. All the notebooks with section and chapter content go here. Modify these files to change the content of the sections.

## Maintaining the Textbook
This section details how to maintain the textbook.

### One-time Setup
Follow these steps the first time you set up a computer to modify and maintain the textbook.
1. Create a local copy of this repo by running `git clone https://github.com/DS-100/course-notes.git` from the command line in whichever folder you want to contain the textbook.
2. Next, you need to install all the required packages. Either of the commands `pip install -r requirements.txt` or `conda install --file requirements.txt` should work. If you have a Windows device, it's preferable to run this in an Anaconda Prompt terminal. This should install the packages used to build the textbook and execute the notebooks. If you use pip to install the packages, I recommend using a python virtual environment:
```
python3 -m venv venv # create virtual environment
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt # as above
```
If you use a virutal environment, make sure to activate it before updating the textbook by first running `source venv/bin/activate` at the top level of this repo. You can deactivate the environment with `deactivate`. If you choose to use a virtual environment not named venv, ensure that you add this to the `.gitignore` so it is NOT tracked by git.

### Updating the Textbook
These steps detail the process you should go through every time you update the textbook. Remember to activate your virtual environment first if you are using one.
1. **Pull:** `cd` into `course-notes/`, your local copy of the repository and `git pull origin main` to collect any updates which may have been pushed to the remote copy by other collaborators.
2. **Update:** Make any changes you wish to make. This should (likely) only consist of changes to `_myst.yml` and the files in `content/`.
    - If you added new sections or chapters, update the `toc` in `myst.yml` to ensure your changes are included.
3. **Build and Check:** `cd` into the top level directory of this repository and run `jupyter book start` to build the book and serve it on localhost. View what the textbook looks like with any changes you've made. Make sure nothing is broken and the changes are as you want them. 
6. **Push:**  Stage any changes you made (i.e. using `git add [file]`, `git add -u`, `git add .`, etc.), commit your changes with `git commit -m "[description]"` (please include a useful description of any changes you made), and push to the repository with `git push origin main`. Deployment will happen automatically via GitHub Actions.

### Deployment
The textbook is hosted on GitHub Pages and deployed automatically everytime you push to the main branch via [this workflow](https://github.com/DS-100/course-notes/actions/workflows/deploy.yml).

## Helpful Things
The [Jupyter Book](https://jupyterbook.org/stable/) website has lots of information about Jupyter Book. This textbook uses Jupyter Book v2 built on [MyST](https://mystmd.org/).

If changes you've made aren't showing up the HTML after building, sometimes deleting `_build` and then building again helps. You can also run `jupyter book clean`.

Some cells are hidden with tags like `remove-input` or `remove-cell`. 

### Images

All images must have alt text. [More on images and figures in MyST.](https://mystmd.org/guide/figures)

### Links
Links to the internet should be done as they are usually done in Markdown. However, to cross-link to other pages of the textbook, there is an internal linking system that should be used instead (since it is robust to file structure changes). This system is described [here](https://mystmd.org/guide/cross-references#targeting-headers). 

For example, Section 12.4 Exercise 3 of the [Stat 88 Textbook](https://github.com/stat88/textbook) contains a link to Section 12.2. 
1. The flag `(ch12.2)=` was added *before* the primary header of the notebook.
```
(ch12.2)=
## The Distribution of the Estimated Slope ##
```
2. The link referencing Section 12.2 is created like so:
```
**3.** 
Refer to the regression of active pulse rate on resting pulse rate in [Section 12.2](ch12.2). Here are the estimated values again, along with some additional data.
```

### Hidden Cells

[Use tags to hide cells and/or their output](https://mystmd.org/guide/interactive-notebooks#notebooks-cell-visibility)

I wasn't able to figure out a quick dropdown to hide the cell before it is clicked, so this is what I ended up with. In a markdown cell, I first put the code that I want to hide in a dropdown [directive](https://mystmd.org/guide/directives):

````{dropdown} Click to see the code
:open: false
```python
import pandas as pd
import numpy as np
import urllib.request
import os.path
import zipfile
```
````

Then I put the code I want to execute (and see its output on the website) in a code cell with the `remove-input` tag added. You can add tags via VSCode or like so:

```{code-cell} python
:tags: [remove-input]
print("This will show output with no input!")
```