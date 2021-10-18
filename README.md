# Reproducible Exploration of Neuroimaging Data
This repo will contain code, notebooks and documentation for the talk titled [*Reproducible Exploration of Neuroimaging Data*](https://cfp.jupytercon.com/2020/schedule/presentation/158/reproducible-exploration-of-neuroimaging-data/), given at JupyterCon 2020 (October 2020). The video of this talk is [here](https://www.youtube.com/watch?v=yXycTif7VmY), and slides are [here](Reproducible_Exploration_of_Neuroimaging_Data.pdf).

Work here is exploratory in nature, and can be use as a guide for implementing similar reproducibility and data visualization pipelines with your own data.
We are not currently releasing the output data used for the dashboard (though may do so at a later date).

Our goal is to release an end-to-end interactive dashboard creation tool called [`SurfBoard`](https://github.com/corticometrics/surfboard) to encompass the features in this repo. 
`SurfBoard` would take commonly produced [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki) brain MRI segmentation results and create a dashboard like the one linked above for users to examine and quality check results.

If you have questions or comments, or you're interested in a demo of the neuroimaging visualization dashboard, please leave an issue or reach out to me on Twitter ([@ltirrell_](https://twitter.com/ltirrell_))!

## Setup
Code in this repo has been tested using Python 3.6, and should also work with Python 3.7 and 3.8. To setup a virtual environment and install all requirements, run the following commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```
Then to activate your virtual environment in the future you can simply run, from wherever you cloned the repo:
```
source venv/bin/activate
```

## Data and Analysis Summary
The [LA5c dataset](https://openneuro.org/datasets/ds000030/versions/1.0.0) was used for the analyses in this repo, and processed with CorticoMetrics' proprietary re:THINQ software (based off of FreeSurfer version 6.0).

[Quilt](https://quiltdata.com/) was used for version control of both input and output data.
Some notes on our quilt usage is available in [here](notebooks/quilt.ipynb).

As part of processing, we created JPEGs of each slice of the brain MRI with the segmentation overlaid, as well as interactive HTML files for a 3D view, using [this script](scripts/create_images.py).
These JPEGs and 3D views are used in creating interactive quality control plots, and were created using [Nilearn](https://nilearn.github.io/).
An example walking through some steps involved is in this [notebook](notebooks/nilearn.ipynb).

## Interactive plots
We provide interactive visualizations of our results.

The first notebook, [`data_exploration.ipynb`](notebooks/data_exploration.ipynb), contains examples of loading in the results of our FreeSurfer-based analysis, and creating [Altair](https://altair-viz.github.io/) charts directly in the notebook.

The second and third notebooks ([`voila.ipynb`](notebooks/voila.ipynb) and [`voila_full.ipynb`](notebooks/voila_full.ipynb)) are notebooks meant to be rendered as [Voilà dashboards](https://github.com/voila-dashboards/voila).
- `voila.ipynb` renders results from the `data_exploration` notebook as a dashboard. 
- `voila_full.ipynb` is similar to what is rendered at our [demo website](https://viz.corticometrics.com/), where JPEGs and 3D brain viewers are included. Note that this will not work, as the necessary images are not included, but serves as an example of how this can be created.

To view the interactive dashboard, run the following command:
```
voila notebooks/voila.ipynb --template=flex
```
The dashboard will be available at http://localhost:8866/

## Description of tools used in this project
### Data versioning
Data versioning is an important and often overlooked part of creating reproducible results (summarized nicely in [this article](https://medium.com/pytorch/how-to-iterate-faster-in-machine-learning-by-versioning-data-and-models-featuring-detectron2-4fd2f9338df5), where a main thesis is `model := script(code, environment, data)`).

We investigated available software packages/platforms for data versioning in May 2020, with an overview of what we found in [this presentation](data_versioning_platforms.pdf).

Based on our use case, Quilt worked out best for us. Our data is already stored in AWS S3 buckets, and Quilt provides an easy way to directly version that data. Additionally, the Catalog created on top of these datasets would be useful in sharing results with collaborators.
Their [docs](https://docs.quiltdata.com/) provide more information on setup, and how to try it out.

Other candidates that we particularly liked are [DVC](https://dvc.org/) and [datalad](https://www.datalad.org/). These treat data more like a part of a Git repo, so it is more closely stored and versioned with your code.
This may be useful for other projects, but we liked treating data as a separate repository, away from code.

### Neuroimage viewing within Jupyter
We decided to use Nilearn for brain viewing within the notebook after being pointed there from a project we used previously called [nbpapaya](https://github.com/akeshavan/nbpapaya).
Other useful Jupyter or web-based packages for neuroimaging viewing are [niwidgets](https://github.com/nipy/niwidgets) and [Papaya](https://github.com/rii-mango/Papaya/), as well as a [Jupyter kernel for the Slicer viewer](https://github.com/Slicer/SlicerJupyter) . 
We are interested to learn about other platforms, so let us know if you are aware of others!

One disadvantage we found with Nilearn was that it takes several seconds to create the 3D viewer for a brain with our use case, so it wasn't quite "interactive" if we wanted to quickly explore a lot of different images.
We got around this by saving HTML versions of these viewers during the initial image processing step, and loading them from disk in our interactive charts.

### Interactive charts
While we normally use [seaborn](https://seaborn.pydata.org/) and [matplotlib](https://matplotlib.org/) for static plots, we wanted something more interactive for quality control and exploration of results.
After seeing *The Python Visualization Landscape* talk ([slides](https://speakerdeck.com/jakevdp/pythons-visualization-landscape-pycon-2017), [video](https://www.youtube.com/watch?v=FytuB8nFHPQ)) from Jake VanderPlas, Altair seemed to be a good tool for the job.
There's also a [Data Visualization Course](https://github.com/uwdata/visualization-curriculum) taught using this package to help learn how to use it.

We found Altair (and the [Vega](https://vega.github.io/vega/) JSON output it is built on) has good support in our Jupyter/Voilà/web based use cases, though there are some minor limitations (such as issues with resizing charts based on browser window size). There was also a learning curve (for us) in getting up to speed in creating charts, compared to the more established matplotlib-based approaches.

## Acknowledgments

This work has been partially funded by the following NIH grants:
- R42CA183150
- R42AG062026
