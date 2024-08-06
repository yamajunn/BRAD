import sys
import cv2
from openpose import pyopenpose as op

# OpenPoseのパラメータ設定
params = dict()
params["model_folder"] = "models/"

# OpenPoseの初期化
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# 画像の読み込み
image_path = "image.jpg"
imageToProcess = cv2.imread(image_path)

# OpenPoseによるポーズ推定
datum = op.Datum()
datum.cvInputData = imageToProcess
opWrapper.emplaceAndPop([datum])

# 結果の表示
cv2.imshow("OpenPose - Tutorial Python API", datum.cvOutputData)
cv2.waitKey(0)
cv2.destroyAllWindows()
