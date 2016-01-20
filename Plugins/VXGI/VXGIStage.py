"""

RenderPipeline

Copyright (c) 2014-2015 tobspr <tobias.springer1@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
                    
"""

from __future__ import division

from .. import *
from panda3d.core import SamplerState

class VXGIStage(RenderStage):

    required_inputs = []
    required_pipes = ["ShadedScene"]

    def __init__(self, pipeline):
        RenderStage.__init__(self, "VXGIStage", pipeline)

    def create(self):
        self._target = self._create_target("VXGI:ApplyGI")
        self._target.add_color_texture(bits=16)
        

    def set_shaders(self):
        pass
        # self._target.set_shader(self._load_plugin_shader("CorrectColor.frag"))
        # if self._use_sharpen:
        #     self._target_sharpen.set_shader(self._load_plugin_shader("Sharpen.frag"))