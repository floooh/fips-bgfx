#-------------------------------------------------------------------------------
#   bgfx_shaders(FILES files...
#		[OUTPUT path]
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
        fips_generate(TYPE BgfxShaderEmbedded FROM ${cur_file} HEADER ${_bs_OUTPUT}${out_file}.bin.h REQUIRES shaderc)
    endforeach()
endmacro()

