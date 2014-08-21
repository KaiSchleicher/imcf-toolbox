#!/usr/bin/python

"""ImageJ related stuff like reading measurement results, etc."""

from log import log

from os import sep
from os.path import join, dirname
from microscopy.pathtools import exists
from misc import readtxt, flatten


def gen_tile_config(mosaic_ds, fixsep=False):
    """Generate a tile configuration for Fiji's stitcher.

    Generate a layout configuration file for a ceartain mosaic in the format
    readable by Fiji's "Grid/Collection stitching" plugin. The configuration is
    stored in a file in the input directory carrying the mosaic's index number
    as a suffix.

    Parameters
    ----------
    mosaic_ds : volpy.dataset.MosaicData
        The mosaic dataset to generate the tile config for.
    fixsep : bool
        Convert path separators in the tileconfig to current OS environment?

    Returns
    -------
    config : list(str)
        The tile configuration as a list of strings, one per line.
    """
    conf = list()
    app = conf.append
    subvol_size_z = mosaic_ds.subvol[0].get_dimensions()['Z']
    subvol_position_dim = len(mosaic_ds.subvol[0].position['relative'])
    app('# Define the number of dimensions we are working on\n')
    if subvol_size_z > 1:
        app('dim = 3\n')
        if subvol_position_dim < 3:
            coord_format = '(%f, %f, 0.0)\n'
        else:
            coord_format = '(%f, %f, %f)\n'
    else:
        app('dim = 2\n')
        coord_format = '(%f, %f)\n'
    app('# Define the image coordinates (in pixels)\n')
    for vol in mosaic_ds.subvol:
        line = '%s; ; ' % join(vol.storage['dname'], vol.storage['fname'])
        # TODO: investigate if the stitcher accepts '/' as pathsep on windows
        if(fixsep):
            line = line.replace('\\', sep)
        line += coord_format % vol.position['relative']
        app(line)
    return conf


def write_tile_config(mosaic_ds, outdir='', fixsep=False):
    """Generate and write the tile configuration file.

    Call the function to generate the corresponding tile configuration and
    store the result in a file. The naming scheme is "mosaic_xyz.txt" where
    "xyz" is the zero-padded index number of this particular mosaic.

    Parameters
    ----------
    mosaic_ds : volpy.dataset.MosaicData
        The mosaic dataset to write the tile config for.
    outdir : str
        The output directory, if empty the input directory is used.
    fixsep : bool
        Passed on to gen_tile_config().
    """
    log.info('write_tile_config(%i)' % mosaic_ds.supplement['index'])
    config = gen_tile_config(mosaic_ds, fixsep)
    # TODO: add some padding mechanism to the experiment/dataset classes
    # fname = 'mosaic_%0*i.txt' % (len(str(len(mosaic_ds))))
    fname = 'mosaic_%s.txt' % mosaic_ds.supplement['index']
    if(outdir == ''):
        fname = join(mosaic_ds.storage['path'], fname)
    else:
        fname = join(outdir, fname)
    out = open(fname, 'w')
    out.writelines(config)
    out.close()
    log.warn('Wrote tile config to %s' % out.name)


def write_all_tile_configs(experiment, outdir='', fixsep=False):
    """Wrapper to generate all TileConfiguration.txt files.

    All arguments are directly passed on to write_tile_config().
    """
    for mosaic_ds in experiment:
        write_tile_config(mosaic_ds, outdir, fixsep)


def gen_stitching_macro_code(experiment, pfx, path='', tplpath='', flat=False):
    """Generate code in ImageJ's macro language to stitch the mosaics.

    Take two template files ("head" and "body") and generate an ImageJ
    macro to stitch the mosaics. Using the splitted templates allows for
    setting default values in the head that can be overridden in this
    generator method (the ImageJ macro language doesn't have a command to
    check if a variable is set or not, it just exits with an error).

    Parameters
    ----------
    experiment : volpy.experiment.MosaicExperiment
        The object containing all information about the mosaic.
    pfx : str
        The prefix for the two template files, will be completed with the
        corresponding suffixes "_head.ijm" and "_body.ijm".
    path : str
        The path to use as input directory *INSIDE* the macro.
    tplpath : str
        The path to a directory or zip file containing the templates.
    flat : bool
        Used to request a flattened string instead of a list of strings.

    Returns
    -------
    ijm : list(str) or str
        The generated macro code as a list of str (one str per line) or as
        a single long string if requested via the "flat" parameter.
    """
    # pylint: disable-msg=E1103
    #   the type of 'ijm' is not correctly inferred by pylint and it complains
    # TODO: generalize by supplying a dict with values to put between the head
    # and body section of the macro
    # by default templates are expected in a subdir of the current package:
    if (tplpath == ''):
        tplpath = join(dirname(__file__), 'ijm_templates')
        log.debug('Looking for template directory: %s' % tplpath)
        if not exists(tplpath):
            tplpath += '.zip'
            log.debug('Looking for template directory: %s' % tplpath)
    if not exists(tplpath):
        raise IOError("Template directory can't be found!")
    log.info('Template directory: %s' % tplpath)
    ijm = readtxt(pfx + '_head.ijm', tplpath)
    ijm.append('\n')

    ijm.append('name = "%s";\n' % experiment.infile['dname'])
    # windows path separator (in)sanity:
    path = path.replace('\\', '\\\\')
    ijm.append('input_dir="%s";\n' % path)
    ijm.append('use_batch_mode = true;\n')

    # If the overlap is below a certain level (5 percent), we disable
    # computing the actual positions and subpixel accuracy:
    if (experiment[0].get_overlap('pct') < 5.0):
        ijm.append('compute = false;\n')

    ijm.append('\n')
    ijm += readtxt(pfx + '_body.ijm', tplpath)
    log.debug('--- ijm ---\n%s\n--- ijm ---' % ijm)
    if (flat):
        return(flatten(ijm))
    else:
        return(ijm)


def write_stitching_macro(code, fname, dname):
    """Write generated macro code into a file.

    Parameters
    ----------
    code : list(str)
        The code as a list of strings, one per line.
    fname : str
        The desired output filename.
    dname : str
        The output directory.
    """
    fname = join(dname, fname)
    log.debug('Writing macro to output directory: "%s".' % fname)
    with open(fname, 'w') as out:
        out.writelines(code)
        log.warn('Wrote macro template to "%s".' % out.name)
