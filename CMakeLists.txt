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
    add_definitions(-D__STDC_FORMAT_MACROS)
    include_directories(bx/include/compat/msvc)
endif()

#-------------------------------------------------------------------------------
fips_begin_lib(bgfx)
    include_directories(bgfx/3rdparty bgfx/3rdparty/khronos)
    fips_dir(bgfx/src GROUP "src")
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
        renderer_vk.cpp
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
    fips_dir(bgfx/include GROUP "include")
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
        fips_libs(opengl32)
    elseif (FIPS_LINUX)
        fips_libs(X11 Xrandr Xi Xinerama Xxf86vm Xcursor GL)
    elseif (FIPS_ANDROID)
        # FIXME!
    endif()
fips_end_lib()

#-------------------------------------------------------------------------------
fips_begin_lib(bgfx-examples-common)
    fips_dir(bgfx/examples/common GROUP ".")
    fips_files(
        aviwriter.h
        bgfx_utils.cpp bgfx_utils.h
        bounds.cpp bounds.h
        camera.cpp camera.h
        common.h
        cube_atlas.cpp cube_atlas.h
    )
    fips_dir(bgfx/examples/common/imgui GROUP "imgui")
    fips_files(
        droidsans.ttf.h
        fs_imgui_color.sc fs_imgui_color.bin.h
        vs_imgui_color.sc vs_imgui_color.bin.h
        fs_imgui_cubemap.sc fs_imgui_cubemap.bin.h
        vs_imgui_cubemap.sc vs_imgui_cubemap.bin.h
        fs_imgui_image.sc fs_imgui_image.bin.h
        vs_imgui_image.sc vs_imgui_image.bin.h
        fs_imgui_image_swizz.sc fs_imgui_image_swizz.sc
        fs_imgui_texture.sc fs_imgui_texture.bin.h
        vs_imgui_texture.sc vs_imgui_texture.bin.h
        fs_ocornut_imgui.sc fs_ocornut_imgui.bin.h
        vs_ocornut_imgui.sc vs_ocornut_imgui.bin.h
        imgui.cpp imgui.h
        ocornut_imgui.cpp ocornut_imgui.h
    )
    fips_dir(bgfx/examples/common/nanovg GROUP "nanovg")
    fips_files(
        fontstash.h
        fs_nanovg_fill.sc fs_nanovg_fill.bin.h
        vs_nanovg_fill.sc vs_nanovg_fill.bin.h
        nanovg.cpp nanovg.h
        nanovg_bgfx.cpp
    )
    fips_dir(bgfx/examples/common/font GROUP "font")
    fips_files(
        font_manager.cpp font_manager.h
        text_buffer_manager.cpp text_buffer_manager.h
        text_metrics.cpp text_metrics.h
        utf8.cpp utf8.h
        fs_font_basic.sc fs_font_basic.bin.h
        fs_font_distance_field.sc fs_font_distance_field.bin.h
        fs_font_distance_field_subpixel.sc fs_font_distance_field_subpixel.bin.h
        vs_font_basic.sc vs_font_basic.bin.h
        vs_font_distance_field.sc vs_font_distance_field.bin.h
        vs_font_distance_field_subpixel.sc vs_font_distance_field_subpixel.bin.h
    )
    fips_dir(bgfx/examples/common/entry GROUP "entry")
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
fips_begin_lib(bgfx-fcpp)
    add_definitions(-DNINCLUDE=64 -DNWORK=65536 -DNBUF=65536 -DOLD_PREPROCESSOR=0)
    include_directories(bgfx/3rdparty/fcpp)
    fips_dir(bgfx/3rdparty/fcpp)
    fips_files(cpp1.c cpp2.c cpp3.c cpp4.c cpp5.c cpp6.c)
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

fips_begin_lib(bgfx-3rdparty)
    fips_dir(bgfx/3rdparty/ib-compress GROUP "ib-compress")
    fips_files(
        indexbuffercompression.cpp indexbuffercompression.h
        indexbuffercompressionformat.h
        indexbufferdecompression.cpp indexbufferdecompression.h
        indexcompressionconstants.h
        readbitstream.h
        writebitstream.h
    )
    fips_dir(bgfx/3rdparty/ocornut-imgui GROUP "ocornut-imgui")
    fips_files(imgui.cpp imgui.h imconfig.h)
fips_end_lib()

file(GLOB_RECURSE BX_FILES bx/include/bx/*.h bx/include/compat/*.h bx/include/tinystl/*.h)
fips_files(${BX_FILES} GROUP "bx")

#-------------------------------------------------------------------------------

fips_ide_group(Tools)
fips_begin_app(shaderc cmdline)
    fips_include_directories(bgfx/3rdparty/glsl-optimizer/src/glsl)
    fips_dir(bgfx/tools/shaderc GROUP "shaderc")
    fips_files(shaderc.cpp shaderc.h shaderc_glsl.cpp shaderc_dx11.cpp shaderc_dx9.cpp)
    fips_dir(bgfx/src GROUP "bgfx")
    fips_files(vertexdecl.cpp vertexdecl.h)
    fips_deps(bgfx-3rdparty bgfx-fcpp bgfx-glsl-optimizer)
    if (FIPS_WINDOWS)
        add_definitions(-D__STDC__ -D__STDC_VERSION=199901L -Dstrdup=_strdup -Dalloca=_alloca -Disascii=__isascii)
        fips_include_directories(bgfx/3rdparty/glsl-optimizer/include/c99)
        fips_include_directories($ENV{DXSDK_DIR}/include)
        fips_libs(d3dx9 d3dcompiler dxguid)
    endif()
fips_end_app()

fips_begin_app(texturec cmdline)
    fips_include_directories(bx/include)
    fips_include_directories(bgfx/include)
    fips_include_directories(bgfx/src)
    fips_dir(bgfx/tools/texturec GROUP "texturec")
    fips_files(texturec.cpp)
    fips_dir(bgfx/src GROUP "bgfx")
    fips_files(image.cpp image.h)
    fips_deps(bgfx-3rdparty)
fips_end_app()

fips_begin_app(geometryc cmdline)
    fips_include_directories(bx/include)
    fips_include_directories(bgfx/include)
    fips_include_directories(bgfx/3rdparty)
    fips_include_directories(bgfx/examples/common)
    fips_dir(bgfx/tools/geometryc GROUP "geometryc")
    fips_files(geometryc.cpp)
    fips_dir(bgfx/src GROUP "bgfx")
    fips_files(vertexdecl.cpp vertexdecl.h)
    fips_dir(bgfx/3rdparty/forsyth-too GROUP "forsyth-too")
    fips_files(forsythtriangleorderoptimizer.cpp forsythtriangleorderoptimizer.h)
    fips_dir(bgfx/examples/common GROUP "bounds")
    fips_files(bounds.cpp bounds.h)
    fips_deps(bgfx-3rdparty)
fips_end_app()

fips_begin_app(makedisttex cmdline)
    fips_include_directories(bx/include)
    fips_include_directories(bgfx/3rdparty)
    fips_dir(bgfx/tools GROUP "makedisttex")
    fips_files(makedisttex.cpp)
    fips_dir(bgfx/3rdparty/edtaa3 GROUP "edtaa3")
    fips_files(edtaa3func.cpp edtaa3func.h)
    fips_deps(bgfx-3rdparty)
fips_end_app()

if (FIPS_CLANG)
    set_target_properties(shaderc PROPERTIES COMPILE_FLAGS "-Wno-strict-aliasing")
    set_target_properties(makedisttex PROPERTIES COMPILE_FLAGS "-Wno-missing-field-initializers")
elseif(FIPS_GCC)
    set_target_properties(shaderc PROPERTIES COMPILE_FLAGS "-Wno-strict-aliasing")
    set_target_properties(makedisttex PROPERTIES COMPILE_FLAGS "-Wno-missing-field-initializers")
elseif(FIPS_MSVC)
    set_target_properties(shaderc PROPERTIES COMPILE_FLAGS "/wd4152 /wd4204 /wd4242 /wd4244 /wd4668 /wd4996")
endif()

#-------------------------------------------------------------------------------
if (NOT FIPS_IMPORT)

fips_ide_group(Samples)
fips_include_directories(bgfx/examples/common)

fips_begin_app(00-helloworld cmdline)
    fips_dir(bgfx/examples/00-helloworld GROUP ".")
    fips_files(helloworld.cpp logo.h screenshot.png)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(01-cubes cmdline)
    fips_dir(bgfx/examples/01-cubes GROUP ".")
    fips_files(cubes.cpp screenshot.png)
    fips_files(fs_cubes.sc vs_cubes.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(02-metaballs cmdline)
    fips_dir(bgfx/examples/02-metaballs GROUP ".")
    fips_files(metaballs.cpp screenshot.png)

    # FIXME: shader compiler integration doesn't work yet,
    # see fips-generators/BgfxShaderEmbedded.py for open issues
    fips_files(fs_metaballs.sc fs_metaballs.bin.h)
    fips_files(vs_metaballs.sc vs_metaballs.bin.h)
    #fips_generate(FROM fs_metaballs.sc
    #              TYPE BgfxShaderEmbedded
    #              HEADER fs_metaballs.bin.h
    #              ARGS "{ type: fragment }")
    #fips_generate(FROM vs_metaballs.sc
    #              TYPE BgfxShaderEmbedded
    #              HEADER vs_metaballs.bin.h
    #              ARGS "{ type: vertex }")
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(03-raymarch cmdline)
    fips_dir(bgfx/examples/03-raymarch GROUP ".")
    fips_files(raymarch.cpp fs_raymarching.sc vs_raymarching.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(04-mesh cmdline)
    fips_dir(bgfx/examples/04-mesh GROUP ".")
    fips_files(mesh.cpp fs_mesh.sc vs_mesh.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(05-instancing cmdline)
    fips_dir(bgfx/examples/05-instancing GROUP ".")
    fips_files(instancing.cpp fs_instancing.sc vs_instancing.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(06-bump cmdline)
    fips_dir(bgfx/examples/06-bump GROUP ".")
    fips_files(bump.cpp fs_bump.sc vs_bump.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(07-callback cmdline)
    fips_dir(bgfx/examples/07-callback GROUP ".")
    fips_files(callback.cpp fs_callback.sc vs_callback.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(08-update cmdline)
    fips_dir(bgfx/examples/08-update GROUP ".")
    fips_files(update.cpp fs_update.sc fs_update_cmp.sc vs_update.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(09-hdr cmdline)
    fips_dir(bgfx/examples/09-hdr GROUP ".")
    fips_files(hdr.cpp)
    fips_files(fs_hdr_blur.sc fs_hdr_bright.sc
               fs_hdr_lum.sc fs_hdr_lumavg.sc
               fs_hdr_mesh.sc fs_hdr_skybox.sc
               fs_hdr_tonemap.sc)
    fips_files(vs_hdr_blur.sc vs_hdr_bright.sc
               vs_hdr_lum.sc vs_hdr_lumavg.sc
               vs_hdr_mesh.sc vs_hdr_skybox.sc
               vs_hdr_tonemap.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(10-font cmdline)
    fips_dir(bgfx/examples/10-font GROUP ".")
    fips_files(font.cpp)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(11-fontsdf cmdline)
    fips_dir(bgfx/examples/11-fontsdf GROUP ".")
    fips_files(fontsdf.cpp)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(12-lod cmdline)
    fips_dir(bgfx/examples/12-lod GROUP ".")
    fips_files(lod.cpp fs_tree.sc vs_tree.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(13-stencil cmdline)
    fips_dir(bgfx/examples/13-stencil GROUP ".")
    fips_files(stencil.cpp)
    fips_files(fs_stencil_color_black.sc fs_stencil_color_lightning.sc
               fs_stencil_color_texture.sc
               fs_stencil_texture.sc fs_stencil_texture_lightning.sc)
    fips_files(vs_stencil_color.sc vs_stencil_color_lightning.sc
               vs_stencil_color_texture.sc vs_stencil_texture.sc
               vs_stencil_texture_lightning.sc)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(14-shadowvolumes cmdline)
    fips_dir(bgfx/examples/14-shadowvolumes GROUP ".")
    fips_files(
        fs_shadowvolume_color_lightning.sc
        fs_shadowvolume_color_texture.sc
        fs_shadowvolume_svbackblank.sc
        fs_shadowvolume_svbackcolor.sc
        fs_shadowvolume_svbacktex1.sc
        fs_shadowvolume_svbacktex2.sc
        fs_shadowvolume_svfrontblank.sc
        fs_shadowvolume_svfrontcolor.sc
        fs_shadowvolume_svfronttex1.sc
        fs_shadowvolume_svfronttex2.sc
        fs_shadowvolume_svside.sc
        fs_shadowvolume_svsideblank.sc
        fs_shadowvolume_svsidecolor.sc
        fs_shadowvolume_svsidetex.sc
        fs_shadowvolume_texture.sc
        fs_shadowvolume_texture_lightning.sc
        shadowvolumes.cpp
        vs_shadowvolume_color_lightning.sc
        vs_shadowvolume_color_texture.sc
        vs_shadowvolume_svback.sc
        vs_shadowvolume_svfront.sc
        vs_shadowvolume_svside.sc
        vs_shadowvolume_texture.sc
        vs_shadowvolume_texture_lightning.sc
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(15-shadowmaps-simple cmdline)
    fips_dir(bgfx/examples/15-shadowmaps-simple GROUP ".")
    fips_files(
        fs_sms_mesh.sc
        fs_sms_mesh_pd.sc
        fs_sms_shadow.sc
        fs_sms_shadow.sh
        fs_sms_shadow_pd.sc
        screenshot.png
        shadowmaps_simple.cpp
        vs_sms_mesh.sc
        vs_sms_shadow.sc
        vs_sms_shadow_pd.sc
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(16-shadowmaps cmdline)
    fips_dir(bgfx/examples/16-shadowmaps GROUP ".")
    fips_files(
        fs_shadowmaps_color_black.sc
        fs_shadowmaps_color_lightning.sh
        fs_shadowmaps_color_lightning_esm.sc
        fs_shadowmaps_color_lightning_esm_csm.sc
        fs_shadowmaps_color_lightning_esm_linear.sc
        fs_shadowmaps_color_lightning_esm_linear_csm.sc
        fs_shadowmaps_color_lightning_esm_linear_omni.sc
        fs_shadowmaps_color_lightning_esm_omni.sc
        fs_shadowmaps_color_lightning_hard.sc
        fs_shadowmaps_color_lightning_hard_csm.sc
        fs_shadowmaps_color_lightning_hard_linear.sc
        fs_shadowmaps_color_lightning_hard_linear_csm.sc
        fs_shadowmaps_color_lightning_hard_linear_omni.sc
        fs_shadowmaps_color_lightning_hard_omni.sc
        fs_shadowmaps_color_lightning_main.sh
        fs_shadowmaps_color_lightning_pcf.sc
        fs_shadowmaps_color_lightning_pcf_csm.sc
        fs_shadowmaps_color_lightning_pcf_linear.sc
        fs_shadowmaps_color_lightning_pcf_linear_csm.sc
        fs_shadowmaps_color_lightning_pcf_linear_omni.sc
        fs_shadowmaps_color_lightning_pcf_omni.sc
        fs_shadowmaps_color_lightning_vsm.sc
        fs_shadowmaps_color_lightning_vsm_csm.sc
        fs_shadowmaps_color_lightning_vsm_linear.sc
        fs_shadowmaps_color_lightning_vsm_linear_csm.sc
        fs_shadowmaps_color_lightning_vsm_linear_omni.sc
        fs_shadowmaps_color_lightning_vsm_omni.sc
        fs_shadowmaps_color_texture.sc
        fs_shadowmaps_hblur.sc
        fs_shadowmaps_hblur_vsm.sc
        fs_shadowmaps_packdepth.sc
        fs_shadowmaps_packdepth_linear.sc
        fs_shadowmaps_packdepth_vsm.sc
        fs_shadowmaps_packdepth_vsm_linear.sc
        fs_shadowmaps_texture.sc
        fs_shadowmaps_unpackdepth.sc
        fs_shadowmaps_unpackdepth_vsm.sc
        fs_shadowmaps_vblur.sc
        fs_shadowmaps_vblur_vsm.sc
        shadowmaps.cpp
        vs_shadowmaps_color.sc
        vs_shadowmaps_color_lightning.sc
        vs_shadowmaps_color_lightning_csm.sc
        vs_shadowmaps_color_lightning_linear.sc
        vs_shadowmaps_color_lightning_linear_csm.sc
        vs_shadowmaps_color_lightning_linear_omni.sc
        vs_shadowmaps_color_lightning_omni.sc
        vs_shadowmaps_color_texture.sc
        vs_shadowmaps_depth.sc
        vs_shadowmaps_hblur.sc
        vs_shadowmaps_packdepth.sc
        vs_shadowmaps_packdepth_linear.sc
        vs_shadowmaps_texture.sc
        vs_shadowmaps_texture_lightning.sc
        vs_shadowmaps_unpackdepth.sc
        vs_shadowmaps_vblur.sc
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(17-drawstress cmdline)
    fips_dir(bgfx/examples/17-drawstress GROUP ".")
    fips_files(drawstress.cpp)
    fips_files(fs_drawstress.sc fs_drawstress.bin.h)
    fips_files(vs_drawstress.sc vs_drawstress.bin.h)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(18-ibl cmdline)
    fips_dir(bgfx/examples/18-ibl GROUP ".")
    fips_files(
        fs_ibl_mesh.sc
        fs_ibl_skybox.sc
        ibl.cpp
        vs_ibl_mesh.sc
        vs_ibl_skybox.sc
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(19-oit cmdline)
    fips_dir(bgfx/examples/19-oit GROUP ".")
    fips_files(
        fs_oit.sc
        fs_oit_wb.sc
        fs_oit_wb_blit.sc
        fs_oit_wb_separate.sc
        fs_oit_wb_separate_blit.sc
        oit.cpp
        vs_oit.sc
        vs_oit_blit.sc
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(20-nanovg cmdline)
    fips_dir(bgfx/examples/20-nanovg GROUP ".")
    fips_files(nanovg.cpp blendish.h)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(21-deferred cmdline)
    fips_dir(bgfx/examples/21-deferred GROUP ".")
    fips_files(
        deferred.cpp
        fs_deferred_combine.sc
        fs_deferred_debug.sc
        fs_deferred_debug_line.sc
        fs_deferred_geom.sc
        fs_deferred_light.sc
        vs_deferred_combine.sc
        vs_deferred_debug.sc
        vs_deferred_debug_line.sc
        vs_deferred_geom.sc
        vs_deferred_light.sc
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(22-windows cmdline)
    fips_dir(bgfx/examples/22-windows GROUP ".")
    fips_files(windows.cpp)
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(23-vectordisplay cmdline)
    fips_dir(bgfx/examples/23-vectordisplay GROUP ".")
    fips_files(
        fs_vectordisplay_blit.sc
        fs_vectordisplay_blur.sc
        fs_vectordisplay_fb.sc
        main.cpp
        vectordisplay.cpp
        vectordisplay.h
        vs_vectordisplay_fb.sc
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(24-nbody cmdline)
    fips_dir(bgfx/examples/24-nbody GROUP ".")
    fips_files(
        cs_init_instances.sc
        cs_update_instances.sc
        fs_particle.sc
        nbody.cpp
        varying.def.sc
        vs_particle.sc
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()

fips_begin_app(25-c99 cmdline)
    fips_dir(bgfx/examples/25-c99 GROUP ".")
    fips_files(
        helloworld.c
    )
    fips_deps(bgfx bgfx-3rdparty bgfx-examples-common)
fips_end_app()
endif() # NOT FIPS_IMPORT

if (NOT FIPS_IMPORT)
    fips_finish()
endif()


