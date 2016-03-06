# fips-bgfx

[![Build Status](https://travis-ci.org/floooh/fips-bgfx.svg?branch=master)](https://travis-ci.org/floooh/fips-bgfx)

fipsified version of bgfx (https://github.com/bkaradzic/bgfx)

#### Get fips and clone fips-bgfx:

```bash
> mkdir fips-workspace
> cd fips-workspace
> git clone git@github.com:floooh/fips.git
> cd fips
> ./fips clone fips-bgfx
> cd ../fips-bgfx
```

#### Build and run on command line:

Build a debug config with xcodebuild (the default build
config on OSX):

```bash
> ./fips build
> ./fips list targets
> ./fips run 00-helloworld
> ./fips run 01-cubes
...
```

### Nicer command line builds with make or ninja:

```bash
# with make:
> ./fips set config osx-make-release
> ./fips build
> ./fips run 00-helloworld
# with ninja:
> ./fips set config osx-ninja-release
> ./fips build
> ./fips run 00-helloworld
...
> ./fips unset config
```

### Work in Xcode:

```bash
> ./fips unset config
> ./fips open
[this should open Xcode and load the fips-bgfx project]
```

Most demos require the current working directory set to
fips-bgfx/bgfx/examples/runtime, do this in Xcode by selecting
the build target (e.g. 01-cubes), go to
'Edit Scheme... -> Options -> Working Directory'.

See fips-bgfx/fips.yml for the list of demos that require the
working directory to be set.

### Test for emscripten:

Only one sample currently works on emscripten, '17-drawstress':

```bash
# setup emscripten SDK for fips if not done before:
> ./fips setup emscripten
# check if all required tools are there (e.g. python2):
> ./fips diag tools
...
# select emscripten build config, configure, build and run
> ./fips set config emsc-make-release
# enable emscripten FS (FileSystem) module, in ccmake,
# find the FIPS_EMSCRIPTEN_USE_FS option, and set it to ON,
# then press (c)onfigure and (g)enerate:
> ./fips config
...
> ./fips make 17-drawstress
> ./fips run 17-drawstress
```

Once the browser opens you may have to refresh (F5) if the sample
doesn't load immediately.

### Known Issues

#### No Shader Code Generation for DirectX on non-Windows platforms

Shader code generation doesn't work fully because the bgfx shader
compiler cannot create HLSL shader on non-windows platforms, the result
will mess up the generated xxx.bin.h files checked in the source tree,
so it's better to not commit generated files or generate them on windows
if there is a need to commit them.

#### Samples

Some samples does not work on all platforms.
Most specifically Emscripten and PNaCL does not support the following samples:

	- 13-stencil
	- 14-shadowvolumes
	- 16-shadowmaps

For missing bx::CtrFileReader or equivalent implementation (see BX_CONFIG_CRT_FILE_READER_WRITER).
