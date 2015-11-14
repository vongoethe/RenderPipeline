
/*

ALCHEMY AO

Projects random points to screen space, and uses the average unoccluded vector
to approximate AO.

*/


const int num_samples = GET_SETTING(AO, alchemy_num_samples);
float max_dist = GET_SETTING(AO, alchemy_max_distance);
float accum = 0.0;
float accum_count = 0;

vec3 bent_normal = vec3(0);

for (int i = 0; i < num_samples; ++i) {

    // Get random texcoord offset
    vec2 offset = poisson_disk_2D_32[i] + noise_vec.xy * 0.2;
    vec2 offcoord = texcoord + offset * pixel_size * sample_radius * kernel_scale * 0.1;

    // Get view position at that offset
    vec3 off_pos = get_view_pos_at(offcoord);

    // Get the vector s-p to that sample position
    vec3 sample_vec = normalize(off_pos - pixel_view_pos);

    // Check if the distance matches, discard matches which are too far away
    float dist = distance(off_pos, pixel_view_pos) / max_dist;
    if (dist < 1.0) {

        // Weight sample by the angle
        accum += max(0, dot(pixel_view_normal, sample_vec)) / dist;

        // Update bent normal
    }

    bent_normal += normalize(-sample_vec);

}

// Normalize
bent_normal /= max(1.0, length(bent_normal));
// bent_normal = viewNormalToWorld(bent_normal);

// TODO: Bent normal is buggy right now. Using world space normal instead
bent_normal = pixel_world_normal;

// Normalize values
accum /= num_samples;
accum *= 0.05;
result = vec4(bent_normal, 1 - saturate(accum));