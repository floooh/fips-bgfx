#-------------------------------------------------------------------------------
#   bgfx_shaders(FILES files...
#		[OUTPUT path])
#
#   Compile shaders and add to current target.
#   Optionaly, you can pass an output path where to generate the files.
#
macro(bgfx_shaders)
    set(options)
    set(oneValueArgs OUTPUT)
    set(multiValueArgs FILES)
    CMAKE_PARSE_ARGUMENTS(_bs "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
    if (_bs_UNPARSED_ARGUMENTS)
        message(FATAL_ERROR "bgfx_shaders(): called with invalid args '${_bs_UNPARSED_ARGUMENTS}'")
    endif()
    if (NOT _bs_FILES)
        message(FATAL_ERROR "bgfx_shaders(): FILES file... required")
    endif()

    if (_bs_OUTPUT)
        file(TO_CMAKE_PATH ${_bs_OUTPUT} _bs_OUTPUT)
        set(_bs_OUTPUT "${_bs_OUTPUT}/")
    endif()

    foreach (cur_file ${_bs_FILES})
        get_filename_component(out_file ${cur_file} NAME_WE)
        fips_generate(TYPE BgfxShaderEmbedded FROM ${cur_file} HEADER ${_bs_OUTPUT}${out_file}.bin.h REQUIRES shaderc OUT_OF_SOURCE)
    endforeach()
endmacro()

#-------------------------------------------------------------------------------
#   bgfx_app(name
#       [GROUP fips_group]
#       [PATH source_path]
#       [DEPS dependencies])
#
#   Defines a basic application that uses bgfx.
#   This is not complete and is used most for bgfx samples, but it can be
#   used to define any application that does not require too much custom
#   fips/cmake parameters.
#
#   GROUP:    the same as fips_dir GROUP, used for grouping files in a project
#   PATH:     path where to find the sources. Accept same parameters as 
#             fips_files_ex()
#   GLOB:     A file mask or regular expression on which files to accept
#   DEPS:     any extra dependency other than bgfx itself,
#             otherwise will use same as samples
#
#   If no PATH is provided we assume this is a bgfx sample and will use the
#   default bgfx sample path structure: bgfx/examples/<name>
#
function(bgfx_app name)
    set(options)
    set(oneValueArgs PATH)
    set(multiValueArgs GROUP DEPS)
    CMAKE_PARSE_ARGUMENTS(_bs "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
    if (_bs_UNPARSED_ARGUMENTS)
        message(FATAL_ERROR "bgfx_app(): called with invalid args '${_bs_UNPARSED_ARGUMENTS}'")
    endif()

    if (NOT name)
        message(FATAL_ERROR "bgfx_app(<name>): need a name.")
    endif()

    #if (NOT _bs_GROUP)
    #    set(_bs_GROUP ".")
    #endif()

    if (NOT _bs_PATH)
        set(_bs_PATH "bgfx/examples/${name}")
    endif()

    if (NOT _bs_DEPS)
        set(_bs_DEPS bgfx-examples-common bgfx-imgui bgfx-ib-compress)
    endif()

    file(TO_CMAKE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/${_bs_PATH} _bs_relative)
    file(TO_CMAKE_PATH ${_bs_PATH} _bs_PATH) # remove trailing slash

    fips_begin_app(${name} windowed)
        fips_src(${_bs_PATH} ${ARGN})

        file(GLOB _glob_file_list RELATIVE ${_bs_relative} "${_bs_PATH}/*.def.sc")
        list(LENGTH _glob_file_list _has_files)
        if (_has_files)
            fips_files(${_glob_file_list})
        endif()

        file(GLOB _glob_file_list RELATIVE ${_bs_relative} "${_bs_PATH}/?s_*.sc")
        list(LENGTH _glob_file_list _has_files)
        if (_has_files)
            bgfx_shaders(FILES ${_glob_file_list})
        endif()

        fips_deps(bgfx ${_bs_DEPS})
    fips_end_app()

    if (FIPS_MSVC)
        set_target_properties(${name} PROPERTIES LINK_FLAGS "/ENTRY:\"mainCRTStartup\"")
    endif()
endfunction()

#-------------------------------------------------------------------------------
#   bgfx_include_compat()
#
#   Helper macro to include multi platform compatibility headers
#
macro(bgfx_include_compat)
    set(FIPS_BGFX_PATH ${FIPS_ROOT_DIR}/../fips-bgfx/)
    if (FIPS_MACOS)
        include_directories(${FIPS_BGFX_PATH}/bx/include/compat/osx)
    elseif (FIPS_IOS)
        include_directories(${FIPS_BGFX_PATH}/bx/include/compat/ios)
    elseif (FIPS_PNACL)
        include_directories(${FIPS_BGFX_PATH}/bx/include/compat/nacl)
    elseif (FIPS_WINDOWS)
        include_directories(${FIPS_BGFX_PATH}/bx/include/compat/msvc)
    endif()
endmacro()