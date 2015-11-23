# Load the plugin api
from .. import *

from panda3d.core import Texture

from .ColorCorrectionStage import ColorCorrectionStage


class Plugin(BasePlugin):

    def __init__(self, pipeline):
        BasePlugin.__init__(self, pipeline)

    @PluginHook("on_stage_setup")
    def setup_stages(self):

        # Disable default display stage to use our own stage
        get_internal_stage_handle(FinalStage).disable_stage()

        self._stage = self.create_stage(ColorCorrectionStage)
        self._stage.set_use_auto_exposure(self.get_setting("use_auto_exposure"))

    @PluginHook("on_pipeline_created")
    def pipeline_created(self):
        self._load_lut()

    def _load_lut(self):
        lut_path = self.get_resource("ShiftedLUT.png")
        lut = SliceLoader.load_3d_texture(lut_path, 64)
        lut.set_wrap_u(Texture.WM_clamp)
        lut.set_wrap_v(Texture.WM_clamp)
        lut.set_wrap_w(Texture.WM_clamp)
        lut.set_minfilter(Texture.FT_linear)
        lut.set_magfilter(Texture.FT_linear)
        lut.set_anisotropic_degree(0)

        self._stage.set_shader_input("ColorLUT", lut)