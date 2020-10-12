#!/usr/bin/env python3

from functools import partial
from io import BytesIO
import json
from multiprocessing import Pool
from pathlib import Path
import warnings

import click
import matplotlib as mpl

# need to set matplotlib backend before it is used/imported by other packages
mpl.use("agg")
import matplotlib.pyplot as plt
import nibabel as nib
from nilearn import image
import nilearn.plotting
from PIL import Image
from xvfbwrapper import Xvfb


warnings.filterwarnings("ignore")


def read_json(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)
    return data


def convert_rgb(color_map):
    for structure in color_map:
        rgb_color = color_map[structure][1][0]
        if rgb_color == "none":
            continue
        else:
            rgb_float = tuple(value / 255 for value in rgb_color)
            color_map[structure][1][0] = rgb_float
    return color_map


def load_and_relabel(image, mapping, relabel=False, affine=False, flip=False):
    img = nib.load(image)
    img_data = img.get_data()

    if relabel:
        for structure in mapping:
            output_value = mapping[structure][1][-1]
            for replacement_value in mapping[structure][1][-2]:
                img_data[img_data == replacement_value] = output_value
        # to make sure any other random structures in the FSColorLUT that aren't caught
        # don't mess with the scaling for screenshots, replace anything out of the range with Unknown
        # range of labels: 101-114, unknown == 100
        img_data[img_data > 114] = 100
        img_data[img_data < 100] = 100

    if affine:
        return img_data, img.affine
    else:
        return img_data


def create_screenshot(
    slice,
    t1_img,
    seg_img,
    affine,
    view,
    cmap,
    output_dir,
    w=256,
    h=256,
    dpi=1024,
    alpha=0.15,
    dim=-1,
    quality=95,
    optimize=True,
):
    with Xvfb() as xvfb:
        # TODO: Moved this config here for now, maybe move out of the function later?
        view_info = {
            "coronal": ("y", False, True),
            "axial": ("z", False, True),
            "sagittal": ("x", False, True),
        }
        mode, reverse, flip = view_info[view]

        output_dir = Path(f"{output_dir}/{view}")
        output_dir.mkdir(parents=True, exist_ok=True)

        image_buffer = BytesIO()
        fig = plt.figure(figsize=(w, h), dpi=dpi)
        # TODO- cleanup, may be a better way but not bothering for now...
        # coords are (y, z, x)
        if view == "sagittal":
            val = image.coord_transform(128, 128, slice, affine)[0]
        elif view == "coronal":
            val = image.coord_transform(slice, 128, 128, affine)[1]
        elif view == "axial":
            val = image.coord_transform(128, slice, 128, affine)[2]
        else:
            raise ValueError(f"view {view} not supported")
        if reverse:
            flip_list = range(256, 0, -1)
            output_file = str(
                output_dir / f"{view}_{flip_list[slice]:03d}.jpg"
            )  # reverse ordering of numberings
        else:
            output_file = str(output_dir / f"{view}_{slice+1:03d}.jpg")

        nilearn.plotting.plot_anat(
            seg_img,
            bg_img=t1_img,
            display_mode=mode,
            cut_coords=[(val)],
            annotate=False,
            black_bg=True,
            figure=fig,
            output_file=image_buffer,
            cmap=cmap,
            vmin=100,
            vmax=115,
            alpha=alpha,
            dim=dim,
        )

        image_buffer.seek(0)
        img = Image.open(image_buffer)
        if flip:
            out = img.transpose(Image.FLIP_LEFT_RIGHT).convert("RGB")
        else:
            out = img.convert("RGB")
        out.save(output_file, quality=quality, optimize=optimize)
        image_buffer.close()
        plt.close("all")


@click.command()
@click.option("--t1w_image", type=click.Path(exists=True), help="input T1w MRI volume")
@click.option(
    "--seg_image",
    type=click.Path(exists=True),
    help="input FreeSurfer segmentatation volume, in register with t1w_image",
)
@click.option(
    "--view",
    "-v",
    type=click.Choice(["sagittal", "axial", "coronal", "all"]),
    help="which view to process",
    default="all",
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="internal [re:]THINQ report config file",
)
@click.option("--threads", "-t", default=1, help="number of processes to use")
@click.option("--output_dir", "-o", default="images", help="directory to output to")
def create_screenshots(t1w_image, seg_image, view, config, threads, output_dir):
    print(f"Loading images...")
    print(f"T1w image: {t1w_image}")
    print(f"Segmentation image: {seg_image}")
    # TODO: taken from vol_screenshots.py. remove/sync in refactor
    raw_color_mapping = read_json(config)["color_mapping"]
    color_mapping = convert_rgb(raw_color_mapping)
    color_list = [color_mapping[structure][1][0] for structure in color_mapping]
    label_number_bounds = [
        color_mapping[structure][1][-1] for structure in color_mapping
    ]
    label_number_bounds.append(
        label_number_bounds[-1] + 1
    )  # needs to be 1 more than the number of colors
    cmap = mpl.colors.ListedColormap(color_list, name="fs_lut")


    tmp_seg = load_and_relabel(
        seg_image, mapping=color_mapping, relabel=True, affine=True
    )
    tmp_t1 = load_and_relabel(
        t1w_image, mapping=color_mapping, relabel=False, affine=True
    )
    seg_img = nib.Nifti1Image(tmp_seg[0], tmp_seg[1])
    t1_img = nib.Nifti1Image(tmp_t1[0], tmp_t1[1])

    # NOTE: currently always 256^3, need to change when this isn't enforced
    y, z, x = t1_img.shape  # also need to ensure correct order
    affine = tmp_t1[1]

    dpi = 2048
    alpha = 0.2
    dim = -1
    quality = 100
    optimize = True
    all_views = ["sagittal", "axial", "coronal"]
    w = x / dpi  # change when not using 256^3
    h = y / dpi  # change when not using 256^3

    # TODO: use a dict for kwargs
    with Pool(processes=threads) as pool:
        print(f"Using {threads} threads for image creation...")
        create_view_screenshot = partial(
            create_screenshot,
            t1_img=t1_img,
            seg_img=seg_img,
            affine=affine,
            cmap=cmap,
            output_dir=output_dir,
            alpha=alpha,
            dim=dim,
            w=w,
            h=h,
            dpi=dpi,
            quality=quality,
            optimize=optimize,
        )
        if view == "all":
            for current_view in all_views:
                print(f"Taking screenshots for {current_view}")
                create_view_screenshot = partial(
                    create_view_screenshot, view=current_view,
                )
                pool.map(create_view_screenshot, range(x))
        else:
            print(f"Taking screenshots for {view}")
            create_view_screenshot = partial(create_view_screenshot, view=view,)
            pool.map(create_view_screenshot, range(x))

    interactive_image = nilearn.plotting.view_img(
        seg_img,
        bg_img=t1_img,
        cmap=cmap,
        vmin=100,
        vmax=115,
        symmetric_cmap=False,
        threshold=None,
        opacity=0.2,
        colorbar=False,
        annotate=False,
        title=f"{output_dir}",
    )
    interactive_image.height = 500
    interactive_image.width = 3000
    interactive_image.save_as_html(f"{output_dir}/interactive.html")


if __name__ == "__main__":
    create_screenshots()
