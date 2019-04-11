"""
Configuration file for pytest, containing global ("session-level") fixtures.

"""

import pytest
from astropy.utils.data import download_file
import vip_hci as vip


@pytest.fixture(scope="session")
def example_dataset():
    """
    Download example FITS cube from github + prepare HCIDataset object.

    Returns
    -------
    dataset : HCIDataset

    Notes
    -----
    Astropy's ``download_file`` uses caching, so the file is downloaded at most
    once per test run.

    """
    print("downloading data...")

    url_prefix = "https://github.com/carlgogo/VIP_extras/raw/master/datasets"

    f1 = download_file("{}/naco_betapic_cube.fits".format(url_prefix),
                       cache=True)
    f2 = download_file("{}/naco_betapic_psf.fits".format(url_prefix),
                       cache=True)
    f3 = download_file("{}/naco_betapic_pa.fits".format(url_prefix),
                       cache=True)

    # load fits
    cube = vip.fits.open_fits(f1)
    angles = vip.fits.open_fits(f3).flatten()  # shape (61,1) -> (61,)
    psf = vip.fits.open_fits(f2)

    # create dataset object
    dataset = vip.HCIDataset(cube, angles=angles, psf=psf,
                             px_scale=vip.conf.VLT_NACO['plsc'])

    dataset.normalize_psf(size=20, force_odd=False)

    # overwrite PSF for easy access
    dataset.psf = dataset.psfn

    return dataset


@pytest.fixture(scope="session")
def example_dataset_ifs():
    """
    Download example FITS cube from github + prepare HCIDataset object.

    Returns
    -------
    dataset : HCIDataset

    Notes
    -----
    Astropy's ``download_file`` uses caching, so the file is downloaded at most
    once per test run.

    """
    print("downloading data...")

    url_prefix = "https://github.com/carlgogo/VIP_extras/raw/master/datasets"

    f1 = download_file("{}/sphere_v471tau_cube.fits".format(url_prefix),
                       cache=True)
    f2 = download_file("{}/sphere_v471tau_psf.fits".format(url_prefix),
                       cache=True)
    f3 = download_file("{}/sphere_v471tau_pa.fits".format(url_prefix),
                       cache=True)
    f4 = download_file("{}/sphere_v471tau_wl.fits".format(url_prefix),
                       cache=True)

    # load fits
    cube = vip.fits.open_fits(f1)
    angles = vip.fits.open_fits(f3).flatten()
    psf = vip.fits.open_fits(f2)
    wl = vip.fits.open_fits(f4)

    # create dataset object
    dataset = vip.HCIDataset(cube, angles=angles, psf=psf,
                             px_scale=vip.conf.VLT_SPHERE_IFS['plsc'],
                             wavelengths=wl)

    # crop
    dataset.crop_frames(size=100, force=True)
    dataset.normalize_psf(size=None, force_odd=False)

    # overwrite PSF for easy access
    dataset.psf = dataset.psfn

    return dataset
