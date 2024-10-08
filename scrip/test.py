import torch
from CNN import cnn
device = torch.device("cuda:0")
model = cnn(15).to(device)



model_weight_path = r"C:\Users\29291\Desktop\QuanYu\QuanYu\models\cnn_net_epoch_40.pkl"
model.load_state_dict(torch.load(model_weight_path, map_location=device))
model.eval()



batch_size = 1  # 批处理大小
input_shape = (1,2,300)  # 输入数据

x = torch.randn(batch_size, *input_shape).cuda()  # 生成张量
export_onnx_file = "cuda.onnx"  # 目的ONNX文件名
torch.onnx.export(model,
                  x,
                  export_onnx_file,
                  opset_version=10,
                  do_constant_folding=True,  # 是否执行常量折叠优化
                  input_names=["input"],  # 输入名
                  output_names=["output"],  # 输出名
                  dynamic_axes={"input": {0: "batch_size"},  # 批处理变量
                                "output": {0: "batch_size"}})
