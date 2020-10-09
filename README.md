# Reproducible Exploration of Neuroimaging Data

This repo will contain code, notebooks and documentation for the talk titled [*Reproducible Exploration of Neuroimaging Data*](https://cfp.jupytercon.com/2020/schedule/presentation/158/reproducible-exploration-of-neuroimaging-data/), to be given at JupyterCon 2020 (October 2020). The neuroimaging visualization dashboard is available [here](https://viz.corticometrics.com/)

Work here is exploratory in nature, and can be use as a guide for implementing similar reproducibility and data visualization pipelines with your own data.
We are not currently releasing the output data used for the dashboard (though may do so at a later date).

Our goal is to release an end-to-end interactive dashboard creation tool called [`SurfBoard`](https://github.com/corticometrics/surfboard) to encompass the features in this repo. 
`SurfBoard` would take commonly produced [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki) brain MRI segmentation results and create a dashboard like the one linked above for users to examine and quality check results.

**NOTE:** More information will be added by 12 October, 2020, in time for the JupyterCon Talks!

## Setup
Code in this repo has been tested using Python 3.6, and should also work with Python 3.7 and 3.8. To setup a virtual environment and install all requirements, run the following commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

## Data and Analysis Summary
The [LA5c dataset](https://openneuro.org/datasets/ds000030/versions/1.0.0) was used for the analyses in this repo, and processed with CorticoMetrics' proprietary re:THINQ software (based off of FreeSurfer version 6.0)

## Interactive plots


<!-- 
5 notebooks:
    - voila (main one used in dashboard)
    - voila (simple one with just plots for users to play around with)
    - nilearn
    - quilt
    - data exploration
HTML/JSON figures of results
 -->