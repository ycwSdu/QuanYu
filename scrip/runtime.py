import onnxruntime  
import torch  
import numpy as np  
providers = ['CUDAExecutionProvider']  
ort_session = onnxruntime.InferenceSession(r"C:\Users\29291\Desktop\QuanYu\scrip\cuda.onnx", providers=providers)

print(ort_session.get_inputs()[0])
#ort_session = onnxruntime.InferenceSession(r"C:\Users\29291\Desktop\QuanYu\scrip\cuda.onnx")  
batch_size = 1  # 批处理大小  
input_shape = (1, 2, 300)  # 输入数据维度（注意这里可能需要调整以匹配模型的实际输入）  

# 创建一个随机的 CUDA 张量  
x = torch.randn(batch_size, *input_shape).cuda()  

# 将 CUDA 张量转换为 CPU 上的 NumPy 数组  
x_np = x.cpu().detach().numpy()  

# 创建 ONNX Runtime 的输入  
ort_inputs = {ort_session.get_inputs()[0].name: x_np}  

# 运行 ONNX Runtime 会话  
ort_outs = ort_session.run(None, ort_inputs)  
print(ort_outs)
print(ort_outs[0].shape)
# ort_outs 现在包含了模型的输出
prediction = torch.max(ort_outs, 1)[1].cpu()
pred_y = prediction.data.numpy()
print(pred_y)