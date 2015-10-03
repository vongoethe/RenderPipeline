
from ..RenderStage import RenderStage


class ApplyLightsStage(RenderStage):

    """ This stage applies the lights to the scene using the gbuffer """

    def __init__(self, pipeline):
        RenderStage.__init__(self, "ApplyLightsStage", pipeline)

    def get_input_pipes(self):
        return ["GBufferDepth", "GBuffer0", "GBuffer1", "GBuffer2",
                "CellIndices", "PerCellLights"]

    def get_produced_pipes(self):
        return {"ShadedScene": self._target.getColorTexture()}

    def get_required_inputs(self):
        return ["AllLightsData", "mainCam", "mainRender", "cameraPosition"]

    def create(self):
        self._target = self._create_target("ApplyLights")
        self._target.addColorTexture()
        self._target.setColorBits(16)
        self._target.prepareOffscreenBuffer()

    def set_shaders(self):
        self._target.setShader(self._load_shader("Stages/ApplyLights.fragment"))

    def resize(self):
        self.debug("Resizing pass")

    def cleanup(self):
        self.debug("Cleanup pass")