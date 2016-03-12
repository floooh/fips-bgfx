#
# project: fips-bgfx
#

if (NOT FIPS_IMPORT)
    cmake_minimum_required(VERSION 2.8)
    get_filename_component(FIPS_ROOT_DIR "../fips" ABSOLUTE)
    include("${FIPS_ROOT_DIR}/cmake/fips.cmake")
    fips_setup()
    fips_project(fips-bgfx)
endif()

#-------------------------------------------------------------------------------
# it looks like bgfx can auto-detect all C preprocessor defines,
# for those that are tweakable, cmake options should be defined here
#

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

#-[ Tools ]---------------------------------------------------------------------

# Build tools only if not cross-compiling
if (NOT CMAKE_TOOLCHAIN_FILE)

fips_ide_group(Tools)
fips_begin_app(shaderc cmdline)
    fips_include_directories(bgfx/3rdparty/glsl-optimizer/src/glsl)
    fips_src(bgfx/tools/shaderc GROUP "shaderc")
    fips_files_ex(bgfx/src vertexdecl.* GROUP "bgfx")
    fips_deps(bgfx-fcpp bgfx-glsl-optimizer)
    if (FIPS_WINDOWS)
        add_definitions(-D__STDC__ -D__STDC_VERSION__=199901L -Dstrdup=_strdup -Dalloca=_alloca -Disascii=__isascii)
        fips_include_directories(bgfx/3rdparty/glsl-optimizer/include/c99)
        include_directories(bgfx/3rdparty/dxsdk/include)
        set(DXSDK_LIB "$ENV{DXSDK_DIR}Lib\\${FIPS_WINDOWS_PLATFORM_NAME}\\")
        fips_libs(d3dcompiler dxguid)
    endif()
fips_end_app()

fips_begin_app(texturec cmdline)
    fips_include_directories(bx/include bgfx/include bgfx/src)
    fips_src(bgfx/tools/texturec GROUP "texturec")
    fips_files_ex(bgfx/src image.* GROUP "bgfx")
    fips_deps(bgfx-edtaa3 bgfx-libsquish bgfx-etc1 bgfx-etc2 bgfx-nvtt bgfx-pvrtc bgfx-tinyexr)
fips_end_app()

fips_begin_app(geometryc cmdline)
    fips_include_directories(bx/include bgfx/include bgfx/3rdparty bgfx/examples/common)
    fips_src(bgfx/tools/geometryc GROUP "geometryc")
    fips_files_ex(bgfx/src vertexdecl.* GROUP "bgfx")
    fips_files_ex(bgfx/examples/common bounds.* GROUP "bounds")
    fips_deps(bgfx-forsyth bgfx-ib-compress)
fips_end_app()

if (FIPS_CLANG)
    set_target_properties(shaderc PROPERTIES COMPILE_FLAGS "-Wno-strict-aliasing")
    set_target_properties(texturec PROPERTIES COMPILE_FLAGS "-Wno-unused-variable")
elseif(FIPS_GCC)
    set_target_properties(shaderc PROPERTIES COMPILE_FLAGS "-Wno-strict-aliasing")
    set_target_properties(texturec PROPERTIES COMPILE_FLAGS "-Wno-unused-variable")
elseif(FIPS_MSVC)
    set_target_properties(shaderc PROPERTIES LINK_FLAGS "/LIBPATH:\"${DXSDK_LIB}\\\"")
    set_target_properties(shaderc PROPERTIES COMPILE_FLAGS "/wd4152 /wd4204 /wd4242 /wd4244 /wd4668 /wd4996 /wd4291 /WX-")
endif()

#-[ 3rd Party Stuff ]-----------------------------------------------------------

fips_ide_group(3rdparty)

fips_begin_lib(bgfx-tinyexr)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS -DMINIZ_NO_TIME)
    fips_src(bgfx/3rdparty/tinyexr)
fips_end_lib()

fips_begin_lib(bgfx-libsquish)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    fips_src(bgfx/3rdparty/libsquish)
fips_end_lib()

fips_begin_lib(bgfx-pvrtc)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    fips_src(bgfx/3rdparty/pvrtc)
fips_end_lib()

fips_begin_lib(bgfx-nvtt)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    include_directories(bgfx/3rdparty/nvtt)
    fips_src(bgfx/3rdparty/nvtt)
fips_end_lib()

fips_begin_lib(bgfx-etc1)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    fips_src(bgfx/3rdparty/etc1)
fips_end_lib()

fips_begin_lib(bgfx-etc2)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    fips_src(bgfx/3rdparty/etc2)
fips_end_lib()

fips_begin_lib(bgfx-forsyth)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    include_directories(bgfx/3rdparty/forsyth-too)
    fips_src(bgfx/3rdparty/forsyth-too)
fips_end_lib()

fips_begin_lib(bgfx-edtaa3)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    include_directories(bgfx/3rdparty/edtaa3)
    fips_src(bgfx/3rdparty/edtaa3)
fips_end_lib()

fips_begin_lib(bgfx-fcpp)
    add_definitions(-DNINCLUDE=64 -DNWORK=65536 -DNBUFF=65536 -DOLD_PREPROCESSOR=0 -D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    include_directories(bgfx/3rdparty/fcpp)
    fips_src(bgfx/3rdparty/fcpp EXCEPT usecpp.c)
fips_end_lib()

fips_begin_lib(bgfx-glsl-optimizer)
    include_directories(bgfx/3rdparty/glsl-optimizer/include)
    include_directories(bgfx/3rdparty/glsl-optimizer/src/mesa)
    include_directories(bgfx/3rdparty/glsl-optimizer/src/mapi)
    include_directories(bgfx/3rdparty/glsl-optimizer/src/glsl)
    include_directories(bgfx/3rdparty/glsl-optimizer/src)
    file(GLOB glsl_sources
        bgfx/3rdparty/glsl-optimizer/src/glsl/glcpp/*.c
        bgfx/3rdparty/glsl-optimizer/src/glsl/*.cpp
        bgfx/3rdparty/glsl-optimizer/src/glsl/*.c
        bgfx/3rdparty/glsl-optimizer/src/mesa/*.c
        bgfx/3rdparty/glsl-optimizer/src/mesa/main/*.c
        bgfx/3rdparty/glsl-optimizer/src/mesa/program/*.c
        bgfx/3rdparty/glsl-optimizer/src/util/*.c
    )
    file(GLOB glsl_sources_remove
        bgfx/3rdparty/glsl-optimizer/src/glsl/glcpp/glcpp.cpp
        bgfx/3rdparty/glsl-optimizer/src/glsl/ir_set_program_inouts.cpp
        bgfx/3rdparty/glsl-optimizer/src/glsl/main.cpp
        bgfx/3rdparty/glsl-optimizer/src/glsl/builtin_stubs.cpp
    )
    list(REMOVE_ITEM glsl_sources ${glsl_sources_remove})
    fips_files(${glsl_sources})
fips_end_lib()

if (FIPS_MSVC)
    set_target_properties(bgfx-glsl-optimizer PROPERTIES COMPILE_FLAGS "/wd4291 /WX-")
endif()

endif() # NOT CMAKE_TOOLCHAIN_FILE

#
# These are used in examples and should be cross-compiled
#
fips_begin_lib(bgfx-imgui)
    set_property(DIRECTORY PROPERTY COMPILE_DEFINITIONS "")
    fips_src(bgfx/3rdparty/ocornut-imgui)
fips_end_lib()

fips_begin_lib(bgfx-ib-compress)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
    fips_src(bgfx/3rdparty/ib-compress)
fips_end_lib()

#-------------------------------------------------------------------------------
fips_ide_group("") # remove grouping

#
# BGFX_CONFIG_PROFILER_REMOTERY ?
# ENTRY_CONFIG_* ?
#

fips_begin_lib(bgfx)
    if (NOT FIPS_PNACL)
        include_directories(bgfx/3rdparty/khronos)
    endif()
    include_directories(bgfx/3rdparty)
    fips_src(bgfx/src EXCEPT amalgamated.cpp GROUP "src")
    fips_files(varying.def.sc)
    bgfx_shaders(FILES
        fs_clear0.sc fs_clear1.sc fs_clear2.sc fs_clear3.sc fs_clear4.sc
        fs_clear5.sc fs_clear6.sc fs_clear7.sc vs_clear.sc
        fs_debugfont.sc vs_debugfont.sc
    )

    if (FIPS_MACOS)
        fips_files(glcontext_nsgl.mm glcontext_nsgl.h)
        fips_files(renderer_mtl.h renderer_mtl.mm)
    elseif (FIPS_IOS)
        fips_files(glcontext_eagl.mm glcontext_eagl.h)
        fips_files(renderer_mtl.h renderer_mtl.mm)
    elseif (FIPS_LINUX)
        fips_files(glcontext_glx.cpp glcontext_glx.h)
    elseif (FIPS_PNACL)
        fips_files(glcontext_ppapi.cpp glcontext_ppapi.h)
    elseif (FIPS_WINDOWS)
        fips_files(glcontext_wgl.cpp glcontext_wgl.h)
    else()
        fips_files(glcontext_egl.cpp glcontext_egl.h)
    endif()
    fips_src(bgfx/include/bgfx GROUP "include")

    fips_src(bx/include GROUP "bx")

    if (FIPS_MACOS)
        fips_frameworks_osx(Cocoa IOKit CoreFoundation CoreVideo Carbon OpenGL Metal QuartzCore)
    elseif (FIPS_WINDOWS)
        fips_libs(opengl32 psapi)
    elseif (FIPS_LINUX)
        fips_libs(X11 Xrandr Xi Xinerama Xxf86vm Xcursor GL dl)
    elseif (FIPS_ANDROID)
        # FIXME!
    elseif (FIPS_IOS)
        fips_frameworks_osx(OpenGLES GLKit Metal)
    endif()
fips_end_lib()

if ("${CMAKE_BUILD_TYPE}" STREQUAL "Debug")
    set_target_properties(bgfx PROPERTIES COMPILE_DEFINITIONS "BGFX_CONFIG_DEBUG=1")
endif()

# Temporarily disable warning caused by some BX_CHECK use.
if (FIPS_CLANG OR FIPS_GCC)
    set_target_properties(bgfx PROPERTIES COMPILE_FLAGS "-Wno-unused-variable")
endif()

#-------------------------------------------------------------------------------
fips_begin_lib(bgfx-examples-common)
    include_directories(bgfx/3rdparty/dxsdk/include)
    add_definitions(-D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS -D__STDC_FORMAT_MACROS)
    fips_src(bgfx/examples/common GROUP ".")
    fips_src(bgfx/examples/common/imgui GROUP "imgui")
    bgfx_shaders(FILES
        fs_imgui_color.sc   vs_imgui_color.sc
        fs_imgui_cubemap.sc vs_imgui_cubemap.sc
        fs_imgui_image.sc   vs_imgui_image.sc
        fs_imgui_texture.sc vs_imgui_texture.sc
        fs_ocornut_imgui.sc vs_ocornut_imgui.sc
        fs_imgui_image_swizz.sc
    )
    fips_files(varying.def.sc)

    fips_src(bgfx/examples/common/nanovg GROUP "nanovg")
    bgfx_shaders(FILES fs_nanovg_fill.sc vs_nanovg_fill.sc)
    fips_files(varying.def.sc)
    fips_src(bgfx/examples/common/font GROUP "font")
    bgfx_shaders(FILES
        fs_font_basic.sc
        vs_font_basic.sc
        fs_font_distance_field.sc
        vs_font_distance_field.sc
        fs_font_distance_field_subpixel.sc
        vs_font_distance_field_subpixel.sc
    )
    fips_files(varying.def.sc)

    fips_dir(bgfx/examples/common/entry GROUP "entry")
    fips_files(cmd.cpp cmd.h dbg.cpp dbg.h entry.cpp entry.h entry_p.h input.cpp input.h)
    
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

#-[ Samples ]-------------------------------------------------------------------
if (NOT FIPS_IMPORT)
    fips_ide_group(Samples)
    fips_include_directories(bgfx/examples/common)
    fips_include_directories(${CMAKE_CURRENT_BINARY_DIR}/)

    bgfx_app(00-helloworld)
    bgfx_app(01-cubes)
    bgfx_app(02-metaballs)
    bgfx_app(03-raymarch)
    bgfx_app(04-mesh)
    bgfx_app(05-instancing)
    bgfx_app(06-bump)
    bgfx_app(07-callback)
    bgfx_app(08-update)
    bgfx_app(09-hdr)
    bgfx_app(10-font)
    bgfx_app(11-fontsdf)
    bgfx_app(12-lod)
    bgfx_app(15-shadowmaps-simple)
    bgfx_app(17-drawstress)
    bgfx_app(18-ibl)
    bgfx_app(19-oit)
    bgfx_app(20-nanovg)
    bgfx_app(21-deferred)
    bgfx_app(22-windows)
    bgfx_app(23-vectordisplay)
    bgfx_app(24-nbody)
    bgfx_app(25-c99)
    bgfx_app(26-occlusion)
    bgfx_app(27-terrain)

    if (NOT FIPS_EMSCRIPTEN AND NOT FIPS_PNACL)
        bgfx_app(13-stencil)
        bgfx_app(14-shadowvolumes)
        bgfx_app(16-shadowmaps)
    endif()

    fips_finish()
endif()
