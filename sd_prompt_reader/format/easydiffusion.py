__author__ = "receyuki"
__filename__ = "easydiffusion.py"
__copyright__ = "Copyright 2023"
__email__ = "receyuki@gmail.com"

import json
from pathlib import PureWindowsPath, PurePosixPath

from ..format.base_format import BaseFormat
from ..utility import remove_quotes


class EasyDiffusion(BaseFormat):
    # easy diffusion mapping table
    EASYDIFFUSION_MAPPING_A = {
        "prompt": "Prompt",
        "negative_prompt": "Negative Prompt",
        "seed": "Seed",
        "use_stable_diffusion_model": "Stable Diffusion model",
        "clip_skip": "Clip Skip",
        "use_vae_model": "VAE model",
        "sampler_name": "Sampler",
        "width": "Width",
        "height": "Height",
        "num_inference_steps": "Steps",
        "guidance_scale": "Guidance Scale",
    }

    EASYDIFFUSION_MAPPING_B = {
        "prompt": "prompt",
        "negative_prompt": "negative_prompt",
        "seed": "seed",
        "use_stable_diffusion_model": "use_stable_diffusion_model",
        "clip_skip": "clip_skip",
        "use_vae_model": "use_vae_model",
        "sampler_name": "sampler_name",
        "width": "width",
        "height": "height",
        "num_inference_steps": "num_inference_steps",
        "guidance_scale": "guidance_scale",
    }

    SETTING_KEY = [
        "",
        "sampler_name",
        "seed",
        "guidance_scale",
        "num_inference_steps",
        "",
    ]

    def __init__(self, info: dict = None, raw: str = ""):
        super().__init__(info, raw)
        if not self._raw:
            self._raw = str(self._info).replace("'", '"')
        self._ed_format()

    def _ed_format(self):
        data_json = json.loads(self._raw)
        if data_json.get("prompt"):
            ed = EasyDiffusion.EASYDIFFUSION_MAPPING_B
        else:
            ed = EasyDiffusion.EASYDIFFUSION_MAPPING_A
        self._positive = data_json.get(ed["prompt"]).strip()
        data_json.pop(ed["prompt"])
        self._negative = data_json.get(ed["negative_prompt"]).strip()
        data_json.pop(ed["negative_prompt"])
        if PureWindowsPath(data_json.get(ed["use_stable_diffusion_model"])).drive:
            file = PureWindowsPath(data_json.get(ed["use_stable_diffusion_model"])).name
        else:
            file = PurePosixPath(data_json.get(ed["use_stable_diffusion_model"])).name

        self._setting = (
            remove_quotes(data_json).replace("{", "").replace("}", "").strip()
        )

        for p, s in zip(super().PARAMETER_KEY, EasyDiffusion.SETTING_KEY):
            match p:
                case "model":
                    self._parameter["model"] = file
                case "size":
                    self._parameter["size"] = (
                        str(data_json.get(ed["width"]))
                        + "x"
                        + str(data_json.get(ed["height"]))
                    )
                case _:
                    self._parameter[p] = data_json.get(s)
