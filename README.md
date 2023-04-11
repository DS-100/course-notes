# course-notes

# Guide to Quarto Installation & Use
## Quarto Set-Up

Begin by [installing Quarto](https://quarto.org/docs/get-started/).

Texts can be authored in Quarto using JupyterLab or classic Jupyter Notebook. To start a new document, open Jupyter and create a new notebook file. 

To set up the document, create a new Raw NBConvert cell. This will be used to set document-level YAML options. The Data 100 lecture notes are generated using the following YAML settings:

```
---
title: "Name of the Lecture"
execute:
    echo: true
format:
  html:
    code-fold: true
    code-tools: true
    toc: true
    toc-title: Name of the Lecture
    page-layout: full
    theme: [cosmo, cerulean]
    callout-icon: false
jupyter: python3
---
```

Now, the notebook is ready for writing content. Quarto supports all the functionality of a standard ipynb file – code cells, markdown, and LaTeX. To begin writing lecture notes, it's a good idea to first set out the main headings of the document. These typically correspond to the title slides of each lecture ([example](https://docs.google.com/presentation/d/1FZJhOS8S1lCqZCRxbyys9rCZT0QxdY4hcmvZDskEHFI/edit#slide=id.g1150ea2fb2b_0_220)) and are written with the Markdown second headng level (`##`). Quarto will auto-populate the table of contents as these headings are created.

To view the Quarto file, open a terminal window (either [within Jupyter](https://docs.google.com/presentation/d/1FZJhOS8S1lCqZCRxbyys9rCZT0QxdY4hcmvZDskEHFI/edit#slide=id.g1150ea2fb2b_0_220) or through your machine's terminal) and navigate to the notebook's directory. Running the command `quarto preview notebook.ipynb` will render the document and open it in a new web browser tab.

With the preview activated, the rendered view will update every time a change is saved in the notebook. When editing the document, it's helpful to have side-by-side views of the notebook and preview so you can watch changes in real-time.

## Document Formatting

A pdf view of how this notebook renders in Quarto can be found [here](https://drive.google.com/file/d/17ga5wvfcmvAzQ1rbnCP4kEf5bckST3--/view?usp=sharing).

#### Formatting Code

The `code-fold: true` option in the YAML set-up will automatically collapse all code cells in the rendered document. If a particular code cell should be uncollapsed by default (e.g. to explicitly show a `pandas` example), a cell-specific YAML option can be specified:

```
#| code-fold: false
print("this code is now visible")
```

#### Formatting Images

Inserting images in a Quarto document is similar to the standard Markdown syntax. The difference is that Quarto will insert figure captions automatically. The syntax below will insert an image with an accompanying description.

```
#![The best class at Berkeley](data.png)
```

#### Formatting Learning Outcomes

Each lecture note should start with a brief list of intended student learning outcomes. These are formatted as collapsable call-out cells, which can be created in a Markdown cell using the syntax below.

```
::: {.callout-note collapse="true"}
## Learning Outcomes
* Gain familiarity with Quarto
* Create your first Quarto document
* Write A+ Data 100 lecture notes
:::
```

## Generating Output
To generate the final notebook as an HTML, run the terminal command `quarto render notebook.ipynb`. The HTML will be outputted in the same directory as the notebook.

# Data 100-specific items

General commands/notes:
  * `jupyter lab # local jupyter setup`
  * `ipynb` -> `qmd`: `quarto convert notebook.ipynb` or `quarto convert notebook.qmd`
  * `quarto render`: renders HTML to `docs`. Note `qmd` has to exist for rendering
  * Edit `_quarto.yml` to include note in sidebar/table of contents
* Quick local development:
  * TODO: how to quickly render just one notes directory and not all notes?
* Publish notes to GitHub pages:
  * `quarto render` everything
  * `git add`, `git commit`, `git push`
  * Can view website compilation on GitHub (look for yellow-to-green button next to commit number)
* Common errors:
  * `Illegal instruction: 4 ...` close jupyter lab

## Other Quarto Resources

[Quick Start Guide](https://quarto.org/docs/get-started/)

[Comprehensive Guide](https://quarto.org/docs/guide/)

[Markdown in Quarto](https://quarto.org/docs/authoring/markdown-basics.html)
