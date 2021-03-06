[![Build Status](https://travis-ci.com/SudoSharma/bimpm_implementation.svg?branch=master)](https://travis-ci.com/SudoSharma/bimpm_implementation)

# BiMPM Implementation in PyTorch
This is a PyTorch implementation of the Bilateral Multi-Perspective Matching for Natural Language Sentences (BiMPM) paper by <em>Wang et al.</em>, which can be found [here](https://arxiv.org/pdf/1702.03814v3.pdf).

## Model Architecture 

<p align="center">
    <img width="500" src="https://github.com/SudoSharma/bimpm_implementation/blob/master/media/bimpm.png"/>
</p>

# Performance 
You can check out my experiments and notes in this [research log](https://docs.google.com/spreadsheets/d/1UqBz1QnXBHKpaYxcI38w2EzEXhXgYLEy6qiaKFdFePw/edit#gid=0). 
## Sentence Similarity
Data: [Quora](https://drive.google.com/file/d/0B0PlTAo--BnaQWlsZl9FZ3l1c28/view) 

| Models        | Accuracy   | 
|--------------|:----------:|
| Original Baseline | 88.2 |
| **Reimplementation** | **86.7** |  

## Natural Language Inference
Data: [SNLI](https://nlp.stanford.edu/projects/snli/)

| Models        |  Accuracy   | 
|--------------|:----------:|
| Original Baseline	| 86.9 |    
| **Reimplementation** | **85.2** |  

# Requirements
## Environment
The `setup.sh` script will create an `bimpm` conda environment for the CPU or GPU. It requires you to specify the specific distribution of Anaconda you have on your computer or VM, so please be sure to edit this in the script. Run the script with the following command:

    ./setup.sh

Note that in order to create a GPU environment, you must run the following command:

    ./setup.sh --gpu

## System
- OS: Ubuntu 16.04 LTS (64 bit)
- GPU: 1 x NVIDIA Tesla P100 

# Instructions
You'll have to download the Quora data on your own, since I'm not including it in this repository, but SNLI data comes packaged with TorchText, so don't worry about this. Once you've downloaded your data, you'll have to create a directory structure that looks a little bit like this:

    $ tree -I __pycache__ -F -n
    .
    ├── app_data/
    │   ├── args.pkl
    │   └── sample_queries.csv
    ├── data/
    │   └── quora/
    │       ├── dev.tsv
    │       ├── test.tsv
    │       ├── toy_dev.tsv
    │       ├── toy_test.tsv
    │       ├── toy_train.tsv
    │       └── train.tsv
    ├── evaluate.py
    ├── LICENSE.md
    ├── media/
    │   └── bimpm.png
    ├── model/
    │   ├── bimpm.py
    │   ├── __init__.py
    │   ├── layers.py
    │   └── utils.py
    ├── README.md
    ├── research/
    │   ├── configs/
    │   │   ├── xp_0.0_args.json
    │   │   ├── xp_0.1_args.json
    │   │   ├── xp_0.2_args.json
    │   │   ├── xp_1.0_args.json
    │   │   └── xp_2.0_args.json
    │   ├── ideas.md
    │   └── output/
    │       ├── xp_0.0_output.txt
    │       ├── xp_0.1_output.txt
    │       ├── xp_0.2_output.txt
    │       ├── xp_1.0_output.txt
    │       └── xp_2.0_output.txt
    ├── runs/
    ├── saved_models/
    ├── setup.sh*
    ├── train.py
    ├── train.sh*
    └── travis/
        ├── install.sh*
        ├── travis_dev.tsv
        ├── travis_test.tsv
        └── travis_train.tsv

Note that the above tree includes a few additional folders you will have to create once you clone the repository. 

To train the model with default parameters, you can execute the **train.sh** shell script as such:

    ./train.sh

The outputs of this script are a `train.out` file containing any output to stdout and stderr, and a `train_pid.txt` file you can use to kill the background process, using the following command:

    kill -9 `cat train_pid.txt`

## Training

    usage: train.py [-h] [-s] [-t] [-e 0.0] [-grad-clip 100] [-batch-size 64]
                    [-char-input-size 20] [-char-hidden-size 50]
                    [-data-type quora] [-dropout 0.1] [-epoch 10]
                    [-hidden-size 100] [-lr 0.001] [-num-perspectives 20]
                    [-print-interval 500] [-word-dim 300]

    Train and store the best BiMPM model in a cycle.

        Parameters
        ----------
        shutdown : bool, flag
            Shutdown system after training (default is False).
        travis : bool, flag
            Run tests on small dataset (default is False).
        experiment : str, optional
            Name of the current experiment (default is '0.0').
        grad_clip : int, optional
            Amount by which to clip the gradient (default is 100).
        batch_size : int, optional
            Number of examples in one iteration (default is 64).
        char_input_size : int, optional
            Size of character embedding (default is 20).
        char_hidden_size : int, optional
            Size of hidden layer in char lstm (default is 50).
        data_type : {'Quora', 'SNLI'}, optional
            Choose either SNLI or Quora (default is 'quora').
        dropout : int, optional
            Applied to each layer (default is 0.1).
        epoch : int, optional
            Number of passes through full dataset (default is 10).
        hidden_size : int, optional
            Size of hidden layer for all BiLSTM layers (default is 100).
        lr : int, optional
            Learning rate (default is 0.001).
        num_perspectives : int, optional
            Number of perspectives in matching layer (default is 20).
        print_interval : int, optional
            How often to write to tensorboard (default is 500).
        word_dim : int, optional
            Size of word embeddings (default is 300).

        Raises
        ------
        RuntimeError
            If any data source other than SNLI or Quora is requested.

        

    optional arguments:
      -h, --help            show this help message and exit
      -s, --shutdown        shutdown system after training
      -t, --travis          use small testing dataset
      -e 0.0, --experiment 0.0
                            name of experiment
      -grad-clip 100        [100]
      -batch-size 64        [64]
      -char-input-size 20   [20]
      -char-hidden-size 50  [50]
      -data-type quora      use quora or snli
      -dropout 0.1          [0.1]
      -epoch 10             [10]
      -hidden-size 100      [100]
      -lr 0.001             [0.001]
      -num-perspectives 20  [20]
      -print-interval 500   [500]
      -word-dim 300         [300]

## Evaluation 

    $ python evaluate.py --help

    usage: evaluate.py [-h] [-s] [-t] [-a] [-batch-size 64]
                       [-char-input-size 20] [-char-hidden-size 50]
                       [-data-type quora] [-dropout 0.1] [-epoch 10]
                       [-hidden-size 100] [-lr 0.001] [-num-perspectives 20]
                       [-print-interval 500] [-word-dim 300]
                       model_path

    Print the best BiMPM model accuracy for the test set in a cycle.

        Parameters
        ----------
        shutdown : bool, flag
            Shutdown system after training (default is False).
        travis : bool, flag
            Run tests on small dataset (default is False)
        app : bool, flag
            Whether to evaluate queries from bimpm app (default is False).
        model_path : str
            A path to the location of the BiMPM trained model.
        batch_size : int, optional
            Number of examples in one iteration (default is 64).
        char_input_size : int, optional
            Size of character embedding (default is 20).
        char_hidden_size : int, optional
            Size of hidden layer in char lstm (default is 50).
        data_type : {'Quora', 'SNLI'}, optional
            Choose either SNLI or Quora (default is 'quora').
        dropout : int, optional
            Applied to each layer (default is 0.1).
        epoch : int, optional
            Number of passes through full dataset (default is 10).
        hidden_size : int, optional
            Size of hidden layer for all BiLSTM layers (default is 100).
        lr : int, optional
            Learning rate (default is 0.001).
        num_perspectives : int, optional
            Number of perspectives in matching layer (default is 20).
        word_dim : int, optional
            Size of word embeddings (default is 300).

        Raises
        ------
        RuntimeError
            If any data source other than SNLI or Quora is requested.

        

    positional arguments:
      model_path

    optional arguments:
      -h, --help            show this help message and exit
      -s, --shutdown        shutdown system after training
      -t, --travis          use small testing dataset
      -a, --app             evaluate user queries from app
      -batch-size 64        [64]
      -char-input-size 20   [20]
      -char-hidden-size 50  [50]
      -data-type quora      use quora, snli, or app
      -dropout 0.1          [0.1]
      -epoch 10             [10]
      -hidden-size 100      [100]
      -lr 0.001             [0.001]
      -num-perspectives 20  [20]
      -print-interval 500   [500]
      -word-dim 300         [300]

# References
1. Wang, Zhiguo, Wael Hamza, and Radu Florian. "Bilateral Multi-Perspective Matching for Natural Language Sentences." Proceedings of the Twenty-Sixth International Joint Conference on Artificial Intelligence, July 14, 2017. Accessed October 10, 2018. doi:10.24963/ijcai.2017/579. 
