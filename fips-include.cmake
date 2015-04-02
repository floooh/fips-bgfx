#
# bgfx_shaders(files ...)
# Compile shaders and add to target.
#
macro(bgfx_shaders files)
	fips_requires(shaderc)
    foreach (cur_file ${ARGV})
        get_filename_component(out_file ${cur_file} NAME_WE)
        fips_generate(TYPE BgfxShaderEmbedded FROM ${cur_file} HEADER ${out_file}.bin.h)
        #fips_files(${cur_file} ${out_file})
    endforeach()
endmacro()

