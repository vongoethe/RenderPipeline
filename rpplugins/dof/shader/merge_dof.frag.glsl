/**
 *
 * RenderPipeline
 *
 * Copyright (c) 2014-2016 tobspr <tobias.springer1@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

#version 430

#pragma include "render_pipeline_base.inc.glsl"
#pragma include "includes/color_spaces.inc.glsl"

uniform sampler2D ShadedScene;
uniform sampler2D SourceTex;
out vec3 result;

void main() {
    const float sharpness = 0.5;

    vec2 texcoord = get_texcoord();
    vec4 dof_result = textureLod(SourceTex, texcoord, 0);
    vec3 scene_color = textureLod(ShadedScene, texcoord, 0).xyz;

    // Reconstruct original color
    // dof_result.xyz = dof_result.xyz / (1 - (1 - sharpness) * get_luminance(dof_result.xyz));
    float dof_weight = saturate(dof_result.w * 10.0);

    #if DEBUG_MODE
        dof_weight = 0;
    #endif

    // result = mix(scene_color * 0, dof_result.xyz, dof_weight);
    // result = mix(vec3(1, 0, 0), dof_result.xyz, dof_weight);
    // result.xyz = vec3(dof_result.w);
    result.xyz = dof_result.xyz;
    // result.xyz = scene_color;
}
