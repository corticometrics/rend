# Reproducible Exploration of Neuroimaging Data
This repo will contain code, notebooks and documentation for the talk titled [*Reproducible Exploration of Neuroimaging Data*](https://cfp.jupytercon.com/2020/schedule/presentation/158/reproducible-exploration-of-neuroimaging-data/), to be given at JupyterCon 2020 (October 2020). The neuroimaging visualization dashboard is available [here](https://viz.corticometrics.com/)

Work here is exploratory in nature, and can be use as a guide for implementing similar reproducibility and data visualization pipelines with your own data.
We are not currently releasing the output data used for the dashboard (though may do so at a later date).

Our goal is to release an end-to-end interactive dashboard creation tool called [`SurfBoard`](https://github.com/corticometrics/surfboard) to encompass the features in this repo. 
`SurfBoard` would take commonly produced [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki) brain MRI segmentation results and create a dashboard like the one linked above for users to examine and quality check results.

Some additional information on why we chose the tools used in this repo will be provided before our talk on 14 October 2020.

Please add any questions or comments as issues to this repo!

## Setup
Code in this repo has been tested using Python 3.6, and should also work with Python 3.7 and 3.8. To setup a virtual environment and install all requirements, run the following commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

## Data and Analysis Summary
The [LA5c dataset](https://openneuro.org/datasets/ds000030/versions/1.0.0) was used for the analyses in this repo, and processed with CorticoMetrics' proprietary re:THINQ software (based off of FreeSurfer version 6.0).

[Quilt](https://quiltdata.com/) was used for version control of both input and output data.
Some notes on our quilt usage is available in [here](notebooks/quilt.ipynb).

As part of processing, we created JPEGS of each slice of the brain MRI with the segmentation overlaid, as well as interactive HTML files for a 3D view, using [this script](scripts/create_images.py).
These JPEGS and 3D views are used in creating interactive quality control plots, and were created using [Nilearn](https://nilearn.github.io/)
An example walking through some steps involved is in this [notebook](notebooks/nilearn.ipynb).

## Interactive plots
We provide of interactive visualizations of our results.

The first notebook, [`data_exploration.ipynb`](notebooks/data_exploration.ipynb), contains examples of loading in the results of our FreeSurfer-based analysis, and creating [Altair](https://altair-viz.github.io/) charts directly in the notebook.

The second and third notebooks ([`voila.ipynb`](notebooks/voila.ipynb) and [`voila_full.ipynb`](notebooks/voila_full.ipynb)) are notebooks meant to be rendered as [Voila dashboards](https://github.com/voila-dashboards/voila).
- `voila.ipynb` renders results from the `data_exploration` notebook as a dashboard. 
- `voila_full.ipynb` is similar to what is rendered at our [demo website](https://viz.corticometrics.com/), where JPEGs and 3D brain viewers are included. Note that this will not work, as the necessary images are not included, but serves as an example of how this can be created.

To view the interactive dashboard, run the following command:
```
voila notebooks/voila.ipynb --template=flex
```
The dashboard will be available at http://localhost:8866/