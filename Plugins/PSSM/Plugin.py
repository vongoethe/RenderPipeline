
from __future__ import print_function

from .. import *

from panda3d.core import Vec3, NodePath, Camera, Texture, PTAVecBase3f
from math import cos, sin

from .PSSMShadowStage import PSSMShadowStage
from .PSSMStage import PSSMStage

class Plugin(BasePlugin):

    def __init__(self, pipeline):
        BasePlugin.__init__(self, pipeline) 
        self._update_enabled = True
        self._pta_sun_vector = PTAVecBase3f.empty_array(1)
        self._last_cache_reset = 0

    @PluginHook("on_stage_setup")
    def setup_stages(self):
        self._shadow_stage = self.create_stage(PSSMShadowStage)
        self._pssm_stage = self.create_stage(PSSMStage)

        self._shadow_stage.set_num_splits(self.get_setting("split_count"))
        self._shadow_stage.set_split_resolution(self.get_setting("resolution"))

    @PluginHook("on_pipeline_created")
    def init(self):
        self.debug("Init pssm ..")

        # Construct a dummy node to parent the rig to
        self._node = Globals.base.render.attach_new_node("PSSMCameraRig")
        self._node.hide()

        # Construct the actual PSSM rig
        self._rig = PSSMCameraRig(self.get_setting("split_count"))
        self._rig.set_sun_distance(self.get_setting("sun_distance"))
        self._rig.set_pssm_distance(self.get_setting("pssm_distance"))
        self._rig.set_use_stable_csm(True)
        self._rig.set_use_fixed_film_size(True)
        self._rig.set_use_tight_frustum(False)
        self._rig.set_resolution(self.get_setting("resolution"))

        self._rig.reparent_to(self._node)

        # Attach the cameras to the shadow stage
        for i in range(self.get_setting("split_count")):
            camera_np = self._rig.get_camera(i)
            camera_np.node().set_scene(Globals.base.render)
            region = self._shadow_stage.get_split_region(i)
            region.set_camera(camera_np)

            # camera_np.node().show_frustum()

            # Make sure the pipeline knows about our camera, so it can apply
            # the correct bitmasks
            self._pipeline.get_tag_mgr().register_shadow_source(camera_np)

        # Accept a shortcut to enable / disable the update of PSSM
        Globals.base.accept("u", self._toggle_update_enabled)

        # Set inputs
        self._pssm_stage.set_shader_input("pssm_split_distance", self.get_setting("pssm_distance"))
        self._pssm_stage.set_shader_input("pssm_split_count", self.get_setting("split_count"))
        self._pssm_stage.set_shader_input("pssm_mvps", self._rig.get_mvp_array())
        self._pssm_stage.set_shader_input("pssm_rotations", self._rig.get_rotation_array())
        self._pssm_stage.set_shader_input("pssm_sun_vector", self._pta_sun_vector)

    @PluginHook("on_shader_create")
    def create_shaders(self):
        pass

    @PluginHook("pre_render_update")
    def update(self):
        sun_vector = Vec3(0.3, 0.3, 0.5)
        sun_vector.normalize()
        self._pta_sun_vector[0] = sun_vector

        if self._update_enabled:
            self._rig.fit_to_camera(Globals.base.camera, sun_vector)

            # Eventually reset cache
            cache_diff = globalClock.get_frame_time() - self._last_cache_reset
            if cache_diff > 1.0:
                self._last_cache_reset = globalClock.get_frame_time()
                self._rig.reset_film_size_cache()

    @SettingChanged("pssm_distance")
    def update_pssm_distance(self):
        print("Adjusting pssm distance")

    def _toggle_update_enabled(self):
        self._update_enabled = not self._update_enabled
        self.debug("Update enabled:", self._update_enabled)
