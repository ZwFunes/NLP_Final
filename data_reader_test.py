from convert_2_fields import UnscopedLogicalFormDatasetReader


def reader_test(filepath, k):
    x = UnscopedLogicalFormDatasetReader()
    y = x.read(filepath)
    iter = 0
    print(f'showing the first {k} instances for the reader')
    while iter < k:
        print(iter+1)
        x = next(y)
        print(x)
        meta_field = x.fields['metadata']
        # separately printing out the metadata field, since it is not included in __repr__
        print(f'meta field info:')
        print(meta_field.metadata)
        iter += 1
    print(f'the first {k} instances are complete [reader test]')

#reader_test('ulf-1.0.json', 3)
#    filepath = 'ulf-1.0.json'

