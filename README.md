# course-notes

# Quick Reference

To edit existing notes:

1. **Run Jupyter** lab locally: `jupyter lab`
1. **Make content changes** to the Jupyter notebook in each course notes folder, e.g., `<course-notes-title>/<fname>.ipynb`

1. **Convert** to Quarto markdown.

    1. Open Terminal, `cd` into `<course-notes-title>` folder
    1. Convert to `.qmd` inside the directory: `quarto convert <fname>.ipynb`
        1. (The `convert` command works both ways; if folders only have a `.qmd` file, run `quarto convert <fname>.qmd` to generate a notebook)
        1. If you don't see updates on `<fname>.qmd`, hit the refresh button in the directory tree.
        1. This command takes a while. Some common errors include trying to print out giant dataframes; make sure you call `df.head()` instead of relying on the default DataFrame display.
        1. If all else fails, quit and relaunch your Jupyter session.

1. **Render** the HTML for the GitHub pages `docs` folder.

    1. Open Terminal, `cd` to the top-level `course-notes` directory.
    1. Render HTML pages: `quarto render`.
        1. To render just a single HTML page **for preview only**, run `quarto render <fname>.qmd <fname>.ipynb` in a particular directory.

1. **Check** HTML. `quarto preview`.

1. **Commit and push**.

    1. Before publishing, push to `dev`. 
    1. For publishing, merge to `main`. The "orange" indicator for your commit on the GitHub indicates that GitHub pages is currently integrating your changes; once it turns green, then your commit will be reflected on the webpage.

To make a new set of course notes:

1. Create the following **folder structure**:

    ```
    new-course-notes-title
    |_ data
    |_ images
    |_ notes-title.ipynb
    ```
1. In the new notebook, copy the **document-level YAML** setup from a publication-ready notebook (more below).

    1. Set it as a Raw cell.
    1. Update the `title` of your notebook in the YAML.
    1. Then edit your notebook.

1. **Convert** to Quarto markdown.

1. **Edit** top-level `_quarto.yml` file with the path to the new `notes-title.qmd` file. This links your new course notes in the webpage sidebar.

1. **Render** changes into `docs` and **check** HTML. If the title of your course notes is incorrect, double-check the title in your document-level YAML.

1. **Commit and push**.
  


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

## Other Quarto Resources

[Quick Start Guide](https://quarto.org/docs/get-started/)

[Comprehensive Guide](https://quarto.org/docs/guide/)

[Markdown in Quarto](https://quarto.org/docs/authoring/markdown-basics.html)
