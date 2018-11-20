import ee


def landsat_c1_toa_cloud_mask(input_img):
    """Extract cloud mask from the Landsat Collection 1 TOA BQA band

    Parameters
    ----------
    input_img : ee.Image
        Image from a Landsat Collection 1 TOA collection with a BQA band
        (e.g. LANDSAT/LE07/C01/T1_TOA).

    Returns
    -------
    ee.Image

    Notes
    -----
    Output image is structured to be applied directly with updateMask()
        i.e. 0 is cloud, 1 is cloud free

    Assuming Cloud must be set to check Cloud Confidence

    Bits
        0:     Designated Fill
        1:     Terrain Occlusion (OLI) / Dropped Pixel (TM, ETM+)
        2-3:   Radiometric Saturation
        4:     Cloud
        5-6:   Cloud Confidence
        7-8:   Cloud Shadow Confidence
        9-10:  Snow/Ice Confidence
        11-12: Cirrus Confidence (Landsat 8 only)

    Confidence values
        00: "Not Determined", algorithm did not determine the status of this
            condition
        01: "No", algorithm has low to no confidence that this condition exists
            (0-33 percent confidence)
        10: "Maybe", algorithm has medium confidence that this condition exists
            (34-66 percent confidence)
        11: "Yes", algorithm has high confidence that this condition exists
            (67-100 percent confidence)

    References
    ----------
    https://landsat.usgs.gov/collectionqualityband

    """
    qa_img = ee.Image(input_img.select(['BQA']))
    cloud_mask = qa_img.rightShift(4).bitwiseAnd(1).neq(0)\
        .And(qa_img.rightShift(5).bitwiseAnd(3).gte(2))\
        .Or(qa_img.rightShift(7).bitwiseAnd(3).gte(3))\
        .Or(qa_img.rightShift(9).bitwiseAnd(3).gte(3))
    # Excluding Cirrus band for now
    #     .Or(qa_img.rightShift(11).bitwiseAnd(3).gte(3))

    # Set cloudy pixels to 0 and clear to 1
    return cloud_mask.Not()


def landsat_c1_sr_cloud_mask(input_img):
    """Extract cloud mask from the Landsat Collection 1 SR pixel_qa band

    Parameters
    ----------
    img : ee.Image
        Image from a Landsat Collection 1 SR image collection with a pixel_qa
        band (e.g. LANDSAT/LE07/C01/T1_SR).

    Returns
    -------
    ee.Image

    Notes
    -----
    Output image is structured to be applied directly with updateMask()
        i.e. 0 is cloud, 1 is cloud free

    Assuming Cloud must be set to check Cloud Confidence

    Bits
        0: Fill
        1: Clear
        2: Water
        3: Cloud Shadow
        4: Snow
        5: Cloud
        6-7: Cloud Confidence

    Confidence values
        00: "None"
        01: "Low"
        10: "Medium"
        11: "High"

    References
    ----------
    https://landsat.usgs.gov/landsat-surface-reflectance-quality-assessment

    """
    qa_img = ee.Image(input_img.select(['pixel_qa']))
    cloud_mask = qa_img.rightShift(5).bitwiseAnd(1).neq(0)\
        .And(qa_img.rightShift(6).bitwiseAnd(3).gte(2))\
        .Or(qa_img.rightShift(3).bitwiseAnd(1).neq(0))\
        .Or(qa_img.rightShift(4).bitwiseAnd(1).neq(0))

    # Set cloudy pixels to 0 and clear to 1
    return cloud_mask.Not()


def sentinel_2_toa_cloud_mask(input_img):
    """Extract cloud mask from the Sentinel 2 TOA QA60 band

    Parameters
    ----------
    input_img : ee.Image
        Image from the COPERNICUS/S2 collection with a QA60 band.

    Returns
    -------
    ee.Image

    Notes
    -----
    Output image is structured to be applied directly with updateMask()
        i.e. 0 is cloud, 1 is cloud free

    Bits
        10: Opaque clouds present
        11: Cirrus clouds present

    References
    ----------
    https://sentinel.esa.int/documents/247904/685211/Sentinel-2_User_Handbook
    https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-2-msi/level-1c/cloud-masks

    """
    qa_img = ee.Image(input_img.select(['QA60']))
    cloud_mask = qa_img.rightShift(10).bitwiseAnd(1).neq(0)\
        .Or(qa_img.rightShift(11).bitwiseAnd(1).neq(0))

    # Set cloudy pixels to 0 and clear to 1
    return cloud_mask.Not()
