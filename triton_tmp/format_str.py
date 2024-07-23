import os
str = 'zhang {}'
str1 = str.format('libia')
# print(str1)

print(str.format('xiaobaidu'))

log_file_name = str1 + '_{}.log'
base_path = "/workspace/triton_bak"

log_path = str1 + os.path.join(base_path, log_file_name)

print(log_path.format('fp16'))
