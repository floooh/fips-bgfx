# fips-bgfx
fipsified version of bgfx (https://github.com/bkaradzic/bgfx)

**ONLY TESTED ON OSX SO FAR!**

#### Get fips and clone fips-bgfx:

> mkdir fips-workspace
> cd fips-workspace
> git clone git@github.com:floooh/fips.git
> cd fips
> ./fips clone fips-bgfx
> cd ../fips-bgfx

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

#### No fips exporting yet

Currently no exports are defined in the fips-bgfx/fips.yml
file, so fips-bgfx cannot yet be used in another fips project
as import.

#### Only tested on OSX so far

Only OSX has been tested so far. Other platform will probably
have compile errors because I forgot important C preprocessor
defines.

#### No Shader Code Generation

Shader code generation doesn't work yet, there is a started
code generator script under fips-bgfx/fips-generators, but this
is relatively useless at the moment because the bgfx shader compiler
cannot create HLSL shader on non-windows platforms, the result
would mess up the generated xxx.bin.h files in the source tree, so it's
currently better to leave shader code generation out of the 
build process.


