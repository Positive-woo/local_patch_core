from __future__ import annotations

from importlib import import_module
from pathlib import Path

import numpy as np
import cv2
from anomalib.deploy import Inferencer


def get_inferencer(weight_path: Path, metadata: Path | None = None) -> Inferencer:
    extension = weight_path.suffix
    inferencer: Inferencer
    module = import_module("anomalib.deploy")
    if extension in (".pt", ".pth", ".ckpt"):
        torch_inferencer = getattr(module, "TorchInferencer")
        inferencer = torch_inferencer(path=weight_path)

    elif extension in (".onnx", ".bin", ".xml"):
        if metadata is None:
            raise ValueError(
                "When using OpenVINO Inferencer, the following arguments are required: --metadata"
            )

        openvino_inferencer = getattr(module, "OpenVINOInferencer")
        inferencer = openvino_inferencer(path=weight_path, metadata=metadata)

    else:
        raise ValueError(
            f"Model extension is not supported. Torch Inferencer exptects a .ckpt file,"
            f"OpenVINO Inferencer expects either .onnx, .bin or .xml file. Got {extension}"
        )

    return inferencer


def infer(
    image: np.ndarray, inferencer: Inferencer
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    predictions = inferencer.predict(image=image)

    return predictions.segmentations, predictions.pred_score
