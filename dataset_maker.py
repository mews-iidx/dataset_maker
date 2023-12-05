import argparse

parser = argparse.ArgumentParser()

parser.add_argument('img_dir', type=str)
parser.add_argument('anno_dir', type=str)
parser.add_argument('--train_rate', type=float, default=0.8)
parser.add_argument('--val_rate', type=float, default=0.1)
parser.add_argument('--test_rate', type=float, default=0.1)

args = parser.parse_args()


if __name__ =='__main__':

	print(args.test_rate)

