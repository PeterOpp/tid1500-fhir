Examples Overview
=================

Most examples are described also in
https://dicom4qi.readthedocs.io/en/latest/instructions/sr-tid1500/ but the
relevant information was copied here for completeness.

dcmqi
-----

This example is from the dcmqi repository, but it is also identical to the
"Dataset 1" of the RSNA 2016 round of the interoperability initiative. It is
based on a liver CT dataset, from which 3 slices were extracted, and a DICOM
SEG object "liver.dcm" defines a ROI for the measurements.

rsna2018_dataset1
-----------------

This is actually the same example as "dcmqi", but the SR is from the RSNA 2018
round and is updated. (A number of values seemed to be placeholders before.)

rsna2018_dataset2
-----------------

This SR dataset contains measurements over the segmentations of tumor and
"hot" lymph nodes.

The corresponding imaging dataset consists of a PET and CT series for subject
QIN-HEADNECK-01-0139 from the TCIA QIN-HEADNECK collection. This data set
contains 11 lesions.

rsna2018_dataset3
-----------------

This SR dataset contains radiomics features (the total of 1561) generated
using pyradiomics and dcmqi.

The corresponding imaging dataset is a chest CT with a single lung lesion
located in the right lung lobe. This dataset is subject LIDC-IDRI-0314 from
The Cancer Imaging Archive (TCIA) LIDC-IDRI collection.

rsna2018_dataset4
-----------------

This SR dataset was created using Pixelmed tools. It contains planimetric
annotation of the largest tumor diameter, and length of that diameter. The
dataset was collected as part of the Crowds Cure Cancer initiative. The
specific dataset corresponds to subject TCGA-BP-4343, series 3, from the TCIA
TCGA-KIRC collection.
