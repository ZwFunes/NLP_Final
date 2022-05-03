from allennlp.data.data_loaders import MultiProcessDataLoader
from convert_2_fields import UnscopedLogicalFormDatasetReader
from allennlp.data.vocabulary import Vocabulary
from allennlp.data.samplers.bucket_batch_sampler import BucketBatchSampler


def first_k_batches(loader, k): # showing the result of first k batches, basically print a tensor
    iter = 1
    print(f'showing the first {k} batches for the loader')
    print(f'----------------------------------------------------')
    for batch in loader:
        print(iter)
        print(batch)
        iter += 1
        if iter > k:
            print(f'----------------------------------------------------')
            print(f'first {k} batches complete [loader test]')
            break


def loader_test(b_size, filepath, test_size):
    reader = UnscopedLogicalFormDatasetReader()
    loader = MultiProcessDataLoader(reader, filepath, batch_sampler=BucketBatchSampler(batch_size=b_size, sorting_keys=['tokens']))
    vocab = Vocabulary.from_instances(reader.read(filepath))
    loader.index_with(vocab)
    first_k_batches(loader, test_size)
