
from roboflow import Roboflow

rf = Roboflow(api_key="mSFbDvx11o3YDKGIdgsS")
project = rf.workspace("classification-glt8h").project("fffff-covp2")
version = project.version(3)
dataset = version.download("folder")
