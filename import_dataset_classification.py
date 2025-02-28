from roboflow import Roboflow


rf = Roboflow(api_key="mSFbDvx11o3YDKGIdgsS")
project = rf.workspace("classification-glt8h").project("c-ewjxw")
version = project.version(1)
dataset = version.download("folder")
