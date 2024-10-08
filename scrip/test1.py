import os, sys

sys.path.append(os.getcwd())
import onnxruntime
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

# 自定义的数据增强
def get_test_transform(): 
    return transforms.Compose([
        transforms.Resize([224, 224]),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

# 推理的图片路径
image = Image.open('./0a0b8641cac0ce40315e38af020bb18f-device4-0-f_items6.jpg').convert('RGB')

img = get_test_transform()(image)
img = img.unsqueeze_(0)  # -> NCHW, 1,3,224,224
# 模型加载
onnx_model_path = "test.onnx"
resnet_session = onnxruntime.InferenceSession(onnx_model_path)
inputs = {resnet_session.get_inputs()[0].name: to_numpy(img)}
outs = resnet_session.run(None, inputs)[0]

print("onnx weights", outs)
print("onnx prediction", outs.argmax(axis=1)[0])

