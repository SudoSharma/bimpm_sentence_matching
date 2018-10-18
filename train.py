import os
import copy
from time import gmtime, strftime
from collections import namedtuple
import plac

import torch
from torch import nn, optim
from tensorboardX import SummaryWriter

from model.bimpm import BiMPM
from model.utils import SNLI, Quora, Sentence
from test import test


def main(batch_size=64,
         char_dim=20,
         char_hidden_size=50,
         data_type=(['SNLI', 'Quora']),
         dropout=0.1,
         epoch=10,
         gpu=True,
         hidden_size=100,
         lr=0.001,
         num_perspectives=20,
         print_interval=500,
         word_dim=300):
    args = locals()

    if args.data_type == 'SNLI':
        print("Loading SNLI data...")
        model_data = SNLI(args)
    elif args.data_type == 'Quora':
        print("Loading Quoradata...")
        model_data = Quora(args)
    else:
        raise RuntimeError(
            'Data source other than SNLI or Quora was provided.')

    args['char_vocab_size'] = len(model_data.char_vocab)
    args['word_vocab_size'] = len(model_data.TEXT.vocab)
    args['class_size'] = len(model_data.LABEL.vocab)
    args['max_word_len'] = model_data.max_word_len
    args['args'] = strftime('%H:%M:%S', gmtime())

    args = namedtuple('args', args.keys())(*args.values())

    print("Starting training...")
    best_model = train(args, model_data)

    if not os.path.exists('saved_models'):
        os.makedirs('save_models')
    torch.save(best_model.state_dict(),
               f'saved_models/bimpm_{args.data_type}_{args.model_time}.pt')

    print("Finished training...")


def train(args, model_data):
    model = BiMPM(args, model_data)
    if args.gpu:
        model.cuda(args.gpu)

    parameters = (p for p in model.parameters() if p.requires_grad)
    optimizer = optim.Adam(parameters, lr=args.lr)
    criterion = nn.CrossEntropyLoss()

    writer = SummaryWriter(log_dir='runs/' + args.model_time)

    model.train()
    train_loss = 0
    max_valid_acc, max_test_acc = 0, 0

    iterator = model_data.train_iter
    for i, batch in enumerate(iterator):
        if not model_data.keep_training(iterator):
            break
        p, q = Sentence(batch, model_data, args.data_type).generate(args.gpu)

        preds = model(p, q)

        optimizer.zero_grad()
        batch_loss = criterion(preds, batch.label)
        train_loss += batch_loss.data[0]
        batch_loss.backward()
        optimizer.step()

        if (i + 1) % args.print_interval == 0:
            valid_loss, valid_acc = test(model, args, model_data, mode='valid')
            test_loss, test_acc = test(model, args, model_data)
            c = (i + 1) // args.print_interval

            writer.add_scalar('loss/train', train_loss, c)
            writer.add_scalar('loss/valid', valid_loss, c)
            writer.add_scalar('acc/valid', valid_acc, c)
            writer.add_scalar('loss/test', test_loss, c)
            writer.add_scalar('acc/test', test_acc, c)

            print(
                f'train_loss: {train_loss:.3f}\n',
                f'valid_loss: {valid_loss:.3f}\n',
                f'test_loss: {test_loss:.3f}\n',
                f'valid_acc: {valid_acc:.3f}\n',
                f'test_acc: {test_acc:.3f}',
                sep='')

            if valid_acc > max_valid_acc:
                max_valid_acc = valid_acc
                max_test_acc = test_acc
                best_model = copy.deepcopy(model)

            train_loss = 0
            model.train()

    print(
        f'max_valid_acc: {max_valid_acc:.3f}\n',
        f'max_test_acc: {max_test_acc:.3f}',
        sep='')
    writer.add_graph(best_model, (p, q))
    writer.close()

    return best_model


if __name__ == '__main__':
    plac.call(main)
