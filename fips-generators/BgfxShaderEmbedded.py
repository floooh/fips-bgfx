"""
Wrap BGFX shader compiler as fips code generator (for code-embedded shaders)
See: bgfx/scripts/shader_embeded.mk
"""
Version = None

import os
import platform
import genutil
import tempfile
import subprocess
import yaml
from mod import log
from mod import util
from mod import settings

# HACK: Find fips-deploy dir the hard way
# TODO: Fips need pass to generators the fips-deploy dir ready to be used
proj_path = os.path.normpath('{}/..'.format(os.path.dirname(os.path.abspath(__file__))))
items = settings.load(proj_path)
if not items:
    items = {'config': settings.get_default('config')}
deploy_path = util.get_deploy_dir("../fips", "fips-bgfx", {'name': items['config']})

#-------------------------------------------------------------------------------
def get_shaderc_path() :
    """find shaderc compiler, fail if not exists"""
    shaderc_path = os.path.abspath('{}/shaderc'.format(deploy_path))
    if not os.path.isfile(shaderc_path) :
        os_name = platform.system().lower()
        shaderc_path = '{}/bgfx/tools/bin/{}/shaderc'.format(proj_path, os_name)
        shaderc_path = os.path.normpath(shaderc_path)
        if not os.path.isfile(shaderc_path) :
            log.error("bgfx shaderc executable not found, please run 'make tools' in bgfx directory")

    return shaderc_path

#-------------------------------------------------------------------------------
def get_include_path() :
    """return the global shader header search path"""
    include_path = '{}/bgfx/src'.format(proj_path)
    include_path = os.path.normpath(include_path)
    if not os.path.isdir(include_path) :
        log.error("could not find bgfx shader include search path at '{}'".format(include_path))
    return include_path

#-------------------------------------------------------------------------------
def get_basename(input_path) :
    return os.path.splitext(os.path.basename(input_path))[0]

#-------------------------------------------------------------------------------
def run_shaderc(input_file, out_tmp, platform, type, subtype, bin_name) :
    cmd = [
        get_shaderc_path(),
        '-i', get_include_path(),
        '--platform', platform,
        '--type', type
    ]
    if subtype :
        cmd.extend(['-p', subtype])
    if platform == 'windows' :
        cmd.extend(['-O', '3'])
    cmd.extend([
        '-f', input_file,
        '-o', out_tmp,
        '--bin2c', bin_name
    ])
    #print ' '.join(cmd)
    subprocess.call(cmd)

#-------------------------------------------------------------------------------
def generate(input_file, out_src, out_hdr) :
    """
    :param input:       bgfx .sc file
    :param out_src:     must be None
    :param out_hdr:     path of output header file
    """

    if not os.path.isfile(out_hdr) or genutil.isDirty(Version, [input_file], [out_hdr]):
        # deduce shader type
        base_file = os.path.basename(input_file)
        shader_type = None
        if base_file.startswith("vs_"):
            shader_type = "vertex"
        if base_file.startswith("fs_"):
            shader_type = "fragment"
        if base_file.startswith("cs_"):
            shader_type = "compute"

        if not shader_type:
            log.error("Could not identify shader type, please use prefix vs_, fs_ or cs_ on file " + input_file)
            return

        # source to bgfx shader compiler
        shaderc_path = get_shaderc_path()
        include_path = get_include_path()
        basename = get_basename(input_file)

        # call shader 3 times for glsl, dx9, dx11 into tmp files
        out_glsl = tempfile.mktemp(prefix='bgfx_glsl_shaderc_')
        out_dx9  = tempfile.mktemp(prefix='bgfx_dx9_shaderc_')
        out_dx11 = tempfile.mktemp(prefix='bgfx_dx11_shaderc_')

        # FIXME: the HLSL compiler is only supported on Windows platforms,
        # thus we would get incomplete .bin.h files on non-windows platforms...
        contents = ""

        os_name = platform.system().lower()
        run_shaderc(input_file, out_glsl, 'linux', shader_type, None, basename+'_glsl')
        with open(out_glsl, 'r') as f:
            contents += f.read()

        if os_name == 'windows':
            run_shaderc(input_file, out_dx9, 'windows', shader_type,
                    'vs_3_0' if shader_type == 'vertex' else 'ps_3_0', basename+'_dx9')
            run_shaderc(input_file, out_dx11, 'windows', shader_type,
                    'vs_4_0' if shader_type == 'vertex' else 'ps_4_0', basename+'_dx11')

            with open(out_dx9, 'r') as f:
                contents += f.read()

            with open(out_dx11, 'r') as f:
                contents += f.read()
        else:
            contents += "\n"
            contents += "// built on {}, hlsl compiler not disponible\n".format(os_name)
            contents += "static const uint8_t {}_dx9[1] = {{ 0 }};\n\n".format(basename)
            contents += "// built on {}, hlsl compiler not disponible\n".format(os_name)
            contents += "static const uint8_t {}_dx11[1] = {{ 0 }};\n\n".format(basename)

        if len(contents):
            with open(out_hdr, 'w') as f:
                f.write(contents)
