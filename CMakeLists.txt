#
# project: fips-bgfx
#
cmake_minimum_required(VERSION 2.8)

# include the fips main cmake file
get_filename_component(FIPS_ROOT_DIR "../fips" ABSOLUTE)
include("${FIPS_ROOT_DIR}/cmake/fips.cmake")

#-------------------------------------------------------------------------------
# it looks like bgfx can auto-detect all C preprocessor defines,
# for those that are tweakable, cmake options should be defined here
#

#-------------------------------------------------------------------------------
fips_setup()

include_directories(bx/include bgfx/include)
if (FIPS_MACOS)
    include_directories(bx/include/compat/osx)
elseif (FIPS_IOS)
    include_directories(bx/include/compat/ios)
elseif (FIPS_PNACL)
    include_directories(bx/include/compat/nacl)
elseif (FIPS_WINDOWS)
    include_directories(bx/include/compat/msvc)
endif()

fips_project(fips-bgfx)

#-------------------------------------------------------------------------------
fips_begin_lib(bgfx)
    include_directories(bgfx/3rdparty bgfx/3rdparty/khronos)
    fips_dir(bgfx/src)
    # note: add all files to the build process, bgfx knows
    # itself what to compile on each platform
    fips_files(
        bgfx.cpp bgfx_p.h 
        charset.h config.h
        glimports.h
        image.cpp image.h
        ovr.cpp ovr.h
        renderdoc.cpp renderdoc.h
        renderer.h
        renderer_null.cpp
        vertexdecl.cpp vertexdecl.h

        # hmm looks like these files must be included
        # on all platforms, otherwise linker errors 
        # from Bgfx::s_rendererCreator result:
        renderer_gl.cpp renderer_gl.h
        renderer_d3d11.cpp renderer_d3d11.h
        renderer_d3d12.cpp
        renderer_d3d9.cpp renderer_d3d9.h
    )
    if (FIPS_MACOS)
        fips_files(glcontext_nsgl.mm glcontext_nsgl.h)
    elseif (FIPS_IOS)
        fips_files(glcontext_eagl.mm glcontext_eagl.h)
    elseif (FIPS_LINUX)
        fips_files(glcontext_glx.cpp glcontext_glx.h)
    elseif (FIPS_PNACL)
        fips_files(glcontext_ppapi.cpp glcontext_ppapi.h)
    elseif (FIPS_WINDOWS)
        fips_files(glcontext_wgl.cpp glcontext_wgl.h)
    else()
        fips_files(glcontext_egl.cpp glcontext_egl.h)
    endif()
    fips_dir(bgfx/include)
    fips_files(
        bgfx.c99.h
        bgfx.h
        bgfxdefines.h
        bgfxplatform.c99.h
        bgfxplatform.h
    )

    # untested, note: OSX and iOS currently
    # automatically link against GL
    if (FIPS_WINDOWS)
        fips_deps(opengl32)
    elseif (FIPS_LINUX)
        fips_deps(X11 Xrandr Xi Xinerama Xxf86vm Xcursor GL)
    elseif (FIPS_ANDROID)
        # FIXME!
    endif()
fips_end_lib()

#-------------------------------------------------------------------------------
fips_begin_lib(bgfx-examples-common)
    fips_dir(bgfx/examples/common)
    fips_files(
        aviwriter.h
        bgfx_utils.cpp bgfx_utils.h
        bounds.cpp bounds.h
        camera.cpp camera.h
        common.h
        cube_atlas.cpp cube_atlas.h
    )
    fips_dir(bgfx/examples/common/entry)
    fips_files(
        cmd.cpp cmd.h
        dbg.cpp dbg.h
        entry.cpp entry.h entry_p.h
        input.cpp input.h
    )
    if (FIPS_ANDROID)
        fips_files(entry_android.cpp)
    elseif (FIPS_EMSCRIPTEN)
        fips_files(entry_asmjs.cpp)
    elseif (FIPS_PNACL)
        fips_files(entry_nacl.cpp)
    elseif (FIPS_WINDOWS)
        fips_files(entry_windows.cpp)
    elseif (FIPS_LINUX)
        fips_files(entry_x11.cpp)
    elseif (FIPS_MACOS)
        fips_files(entry_osx.mm)
    elseif (FIPS_IOS)
        fips_files(entry_ios.mm)
    else()
        fips_files(entry_qnx.cpp entry_sdl.cpp entry_winrt.cpp)
    endif()
fips_end_lib()

#-------------------------------------------------------------------------------
fips_begin_lib(bgfx-3rdparty)
    fips_dir(bgfx/3rdparty/ib-compress)
    fips_files(
        indexbuffercompression.cpp indexbuffercompression.h
        indexbuffercompressionformat.h
        indexbufferdecompression.cpp indexbufferdecompression.h
        indexcompressionconstants.h
        readbitstream.h
        writebitstream.h
    )
fips_end_lib()

#-------------------------------------------------------------------------------
fips_begin_app(00-helloworld windowed)
    include_directories(bgfx/examples/common)
    fips_dir(bgfx/examples/00-helloworld)
    fips_files(helloworld.cpp logo.h screenshot.png)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_finish()


