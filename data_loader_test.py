from allennlp.data.data_loaders import MultiProcessDataLoader
from convert_2_fields import UnscopedLogicalFormDatasetReader

filepath = 'ulf-1.0.json'

x = UnscopedLogicalFormDatasetReader()
'''
y = x.read(filepath)
for i in y:
    print(i)
'''
y = MultiProcessDataLoader(x, filepath, batch_size=5)

print(x)