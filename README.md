The purpose of this template is to be a foundation for creating a new research project, specifically for data/network science research in the [NERDS research group](https://nerds.itu.dk/) - but feel free to use it in any way. The template comes with a basic folder structure and a workflow adapted for programming using Python.
# Paris bicycle plan and vote delays
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

This is the source code for the scientific paper/project [*PROJECTNAME*](PAPERURL) by [AUTHOR1](AUTHOR1URL), [AUTHOR2](AUTHOR2URL), and [AUTHOR3](AUTHOR3URL). The code SHORTEXPLANATION.

**Preprint**: [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)  
**Data repository**: [zenodo.XXXXXXX](https://zenodo.org/record/XXXXXXX)  

[![PROJECTNAME](SPLASHIMAGE.JPG/PNG/GIF)](PROJECTURL)

## Installation
First clone the repository:

```
git clone https://github.com/csebastiao/paris_vote_bicycle.git
```

Go to the cloned folder and create a new virtual environment. 

### Installation with pixi

Installation with [`pixi`](https://pixi.prefix.dev/latest/) is fastest and most stable. Setup a new virtual environment using the `environment.yml` file:

```
pixi init --import environment.yml
```

### Installation with pip/mamba/conda

You can either create a new virtual environment then install the necessary dependencies with `pip` using the `requirements.txt` file:

```
pip install -r requirements.txt
```

Or create a new environment with the dependencies with `conda`/`mamba` using the `environment.yml` file:

```
conda env create -f environment.yml
```
Then, install the virtual environment's kernel in Jupyter:

```
conda activate paris_vote_bicycle
ipython kernel install --user --name=paris_vote_bicycle
mamba deactivate
```

## Repository structure

```
├── data
│   ├── processed           <- Modified data
│   └── raw                 <- Original, immutable data
├── notebooks               <- Jupyter notebooks
├── plots                   <- Generated figures
├── scripts                 <- Scripts to execute
├── .gitignore              <- Files and folders ignored by git
├── .pre-commit-config.yaml <- Pre-commit hooks used
├── CITATION.cff            <- Citation file (template)
├── README.md
├── TEMPLATE.md             <- Explanation for the template, delete it after use
├── environment.yml         <- Environment file to set up the environment using conda/mamba
└── requirements.txt        <- Requirements file to set up the environment using pip
```

## Credits

Please cite as: 
>AUTHOR1, AUTHOR2, and AUTHOR3, PROJECTNAME, JOURNAL (YYYY), DOIURL  

Development of PROJECTNAME was supported by FUNDER.


