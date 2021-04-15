import os.path as op
from pyxnat import Interface

fp = op.abspath('.devxnat.cfg')
central = Interface(config=fp)
p = central.select.project('pyxnat_tests')
s = p.subject('rs')
e1 = s.experiment('BBRCDEV_E03094')

p = central.select.project('pyxnat_tests')
s = p.subject('BBRCDEV_S02627')
e2 = s.experiment('BBRCDEV_E03106')


def test_ashs_volumes():
    r = central.select.experiment('BBRCDEV_E03094').resource('ASHS')
    hv = r.volumes()
    v = hv.query('region=="CA1" & side=="left"')['volume'].tolist()[0]
    assert (v == 1287.675)


def test_freesurfer6_aparc():
    r = e1.resource('FREESURFER6')
    hv = r.aparc()
    q = 'region=="supramarginal" & side=="left" & measurement=="CurvInd"'
    v = hv.query(q)['value'].tolist()[0]
    assert(v == '10.8')


def test_freesurfer6_aseg():
    r = e1.resource('FREESURFER6')
    hv = r.aseg()
    v = hv.query('region=="BrainSegVol"')['value'].tolist()[0]
    assert(v == 2463095.0)


def test_scandate():
    s = e2.scans().first()
    r = s.resource('DICOM')
    assert(r.scandate() == '2008-05-06')


def test_ftm_quantification():
    r = e1.resource('FTM_QUANTIFICATION')
    c1 = r.centiloids()
    c2 = r.centiloids(False)
    assert(c1 == -6.731959667125082)
    assert(c2 == -7.958670071142706)


def test_fdg_quantification():
    r = e1.resource('FDG_QUANTIFICATION')
    c1 = r.landau_signature()
    v1 = float(c1.query('region == "landau_Composite"')['value'])
    c2 = r.landau_signature(optimized=False)
    v2 = float(c2.query('region == "landau_Composite"')['value'])
    assert(v1 == 1.2596989870071411)
    assert(v2 == 1.2491936683654783)


def test_bamos_volume():
    r = e1.resource('BAMOS')
    v = r.volume()
    assert(v == 33620.32498628937)


def test_bamos_stats():
    r = e1.resource('BAMOS')
    v = r.stats()
    print(sum(v['volume']))
    assert(sum(v['volume']) == 33620.32429030311)
    r.bullseye_plot(stats=v)


def test_bamos_n_lesion():
    r = e1.resource('BAMOS')
    v = r.n_lesions()
    assert(v == 296)


def test_freesurfer7_amygNucVolumes():
    r = e1.resource('FREESURFER7')
    hv = r.amygNucVolumes()
    assert (hv.shape == (20, 3))
    q = 'region=="Whole_amygdala" & side=="left"'
    v = hv.query(q)['value'].tolist()[0]
    assert(v == 1426.132879)


def test_freesurfer7_hippoSfVolumes():
    r = e1.resource('FREESURFER7')
    hv = r.hippoSfVolumes()
    assert (hv.shape == (44, 3))
    q = 'region=="Whole_hippocampus" & side=="left"'
    v = hv.query(q)['value'].tolist()[0]
    assert(v == 2853.846782)


def test_freesurfer7_aparc():
    r = e1.resource('FREESURFER7')
    hv = r.aparc()
    assert (hv.shape == (632, 4))
    q = 'region=="supramarginal" & side=="left" & measurement=="CurvInd"'
    v = hv.query(q)['value'].tolist()[0]
    assert(v == '5.0')


def test_freesurfer7_aseg():
    r = e1.resource('FREESURFER7')
    hv = r.aseg()
    assert (hv.shape == (424, 3))
    v = hv.query('region=="BrainSegVol"')['value'].tolist()[0]
    assert(v == 906719.90625)


def test_spm12_volumes():
    r = e1.resource('SPM12_SEGMENT')
    v = r.volumes()
    assert(v['c1'] > v['c2'] > v['c3'])


def test_cat12_volumes():
    r = e1.resource('CAT12_SEGMENT')
    v = r.volumes()
    assert(v['mri/p1'] > v['mri/p2'] > v['mri/p3'])


def test_donsurf():
    r = e1.resource('DONSURF')
    st = r.aparc()
    left = float(st.query('measurement == "CurvInd" &'\
                          'region == "insula" & side == "left"')['value'])
    right = float(st.query('measurement == "CurvInd" &'\
                           'region == "insula" & side == "right"')['value'])
    assert(left == 15.7 and right == 15.8)
