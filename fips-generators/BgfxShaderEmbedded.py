"""
Wrap BGFX shader compiler as fips code generator (for code-embedded shaders)
See: bgfx/scripts/shader_embeded.mk

Version 3 - Threading shader compilation
Version 2 - Added support to metal shader compilation
Version 1 - Initial version
"""
Version = 3

import os
import platform
import genutil
import tempfile
import subprocess
import yaml
from mod import log
from mod import util
from mod import settings
from threading import Thread

# HACK: Find fips-deploy dir the hard way
# TODO: Fips need pass to generators the fips-deploy dir ready to be used
os_name = platform.system().lower()
extension = ""
proj_path = os.path.normpath('{}/..'.format(os.path.dirname(os.path.abspath(__file__))))
items = settings.load(proj_path)
if not items:
    items = {'config': settings.get_default('config')}

# HACK: even setting PROJECT in fips_setup does not work here without a way to get the
# fips-deploy path, so we force to search in Project for windows as it is the default
if os_name == "windows":
    extension = ".exe"

deploy_path = util.get_deploy_dir("../fips", "fips-bgfx", {'name': items['config']})

#-------------------------------------------------------------------------------
def get_shaderc_path() :
    """find shaderc compiler, fail if not exists"""

    shaderc_path = os.path.abspath('{}/shaderc{}'.format(deploy_path, extension))
    if not os.path.isfile(shaderc_path) :
        os_name = platform.system().lower()
        shaderc_path = '{}/bgfx/tools/bin/{}/shaderc{}'.format(proj_path, os_name, extension)
        shaderc_path = os.path.normpath(shaderc_path)
        
        if not os.path.isfile(shaderc_path) :
            log.error("bgfx shaderc executable not found, please run 'make tools' in bgfx directory: ", shaderc_path)

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
def run_shaderc(input_file, out_tmp, platform, shader_type, subtype, bin_name) :
    cmd = [
        get_shaderc_path(),
        '-i', get_include_path(),
        '--platform', platform,
        '--type', shader_type
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
    output = ' '.join(cmd) + "\n"
    print output
    subprocess.call(cmd)

class BuildShaderTask(Thread):
    def __init__(self, input_file, fmt, platform, shader_type, sub_type, basename):
        self.contents = ""
        self.input_file = input_file
        self.fmt = fmt
        self.platform = platform
        self.shader_type = shader_type
        self.sub_type = sub_type
        self.basename = basename
        super(BuildShaderTask, self).__init__()

    def run(self):
        if os_name == 'windows' and self.fmt == 'dx9' and self.shader_type == 'compute':
            self.contents = "// dx9 do not have compute\n"
        elif os_name != 'windows' and self.fmt in ['dx9','dx11']:
            self.contents  = ""
            self.contents += "// built on {}, hlsl compiler not disponible\n".format(os_name)
            self.contents += "static const uint8_t {}_{}[1] = {{ 0 }};\n\n".format(self.basename, self.fmt)
        else:
            out_file = tempfile.mktemp(prefix='bgfx_'+self.fmt+'_shaderc_')
            run_shaderc(self.input_file, out_file, self.platform,
                        self.shader_type, self.sub_type, self.basename+'_'+self.fmt)
            f = open(out_file, 'r')
            self.contents += f.read() + "\n"
            f.close()
            os.remove(out_file)


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

        glsl = BuildShaderTask(input_file, 'glsl', 'linux', shader_type, None, basename)
        mtl = BuildShaderTask(input_file, 'mtl', 'ios', shader_type, None, basename)
        dx9 = BuildShaderTask(input_file, 'dx9', 'windows', shader_type,
                'vs_3_0' if shader_type == 'vertex' else 'ps_3_0', basename)
        dx11 = BuildShaderTask(input_file, 'dx11', 'windows', shader_type,
                'vs_4_0' if shader_type == 'vertex' else 
                'cs_5_0' if shader_type == 'compute' else 'ps_4_0', basename)

        glsl.start()
        mtl.start()
        dx9.start()
        dx11.start()

        glsl.join()
        mtl.join()
        dx9.join()
        dx11.join()

        contents = glsl.contents + mtl.contents + dx9.contents + dx11.contents
        if len(contents):
            with open(out_hdr, 'w') as f:
                contents = "// #version:{}#\n".format(Version) + contents
                f.write(contents)
