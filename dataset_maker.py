import argparse
import random
import shutil
import yaml
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument('--img_dir', type=str, required=True)
parser.add_argument('--anno_dir', type=str, required=True)
parser.add_argument('--out_dir', type=str, default='./dataset')
parser.add_argument('--train_rate', type=float, default=0.8)
parser.add_argument('--eval_rate', type=float, default=0.1)
parser.add_argument('--test_rate', type=float, default=0.1)

args = parser.parse_args()

def gen_yaml(train_dir, eval_dir, test_dir, classes_txt):
    f = open(classes_txt, 'r')
    lines = f.readlines()
    class_dict = {}
    for idx, line in enumerate(lines):
        class_dict[idx] = line.rstrip()
    d = {
        'train' :str(train_dir.resolve()),
        'eval': str(eval_dir.resolve()),
        'test': str(test_dir.resolve()),
        'names': class_dict,
	}

    # train_dirからdataset dir を取得
    dataset_yaml = open(train_dir.parent / 'custom_dataset.yaml', 'w')
    dataset_yaml.write(yaml.dump(d))
    

def copy_files(anno_files, output_dir):

    for anno_file in anno_files:
        # anno_file から画像名を取得
        ## ex: 入力が /path/to/anno/1.txtとすると
        ## path全体からpathだけ取得 ex: /path/to/anno
        print('anno_file.parent', anno_file.parent)
        ## path全体から名前だけ取得 ex: 1.txt
        print('anno_file.name', anno_file.name)

        ## /path/to/anno/1.txt の場合、画像名は /path/to/img/1.? である
        # 1. ファイル名を取得 ex: 1.txt
        filename = anno_file.name
  
        # 2. 拡張子を除く  1
        filename = anno_file.stem
        # print(filename)

        # 4. 画像を取得 ex: /path/to/img/1.* のファイル群がimgs に入る
        imgs =  IMG_DIR.glob(f'{filename}.*')
        imgs = list(imgs)

        # 5. imgs 1.jpg, 1.pngとか名前が複数ある場合は使用しない
        if  len(imgs) != 1:
            continue

        # 6. imgs は要素数1であるため、画像は１つ　よってリストから画像を取得
        img_file = imgs[0]

        # 7. img, ann が存在することを確認 なければ落ちる
        assert img_file.exists() and anno_file.exists()

        print(anno_file, img_file)
        shutil.copy(anno_file, output_dir)
        shutil.copy(img_file, output_dir)


if __name__ =='__main__':
    #　引数チェック
    # print(args.img_dir)
    # print(args.anno_dir)
    # print(args.out_dir)
    # print(args.train_rate)
    # print(args.eval_rate)
    # print(args.test_rate)
 
    # Path objectに変換
    IMG_DIR = Path(args.img_dir)
    ANN_DIR = Path(args.anno_dir)

    OUT_DIR = Path(args.out_dir)
    TRAIN_DIR = OUT_DIR / 'train'
    EVAL_DIR = OUT_DIR / 'eval'
    TEST_DIR = OUT_DIR / 'test'
    for dir in [TRAIN_DIR, EVAL_DIR, TEST_DIR]:
        dir.mkdir(exist_ok=True, parents=True)
        

    # アノテーションされているファイルの取得
    # ファイルがある＝アノテーションされている
    # 例 こんなPath 型がlistに入る
    # anno_files[0] : /path/to/anno/1.txt
    # anno_files[1] : /path/to/anno/2.txt
    # anno_files[2] : /path/to/anno/3.txt
    anno_files = list(ANN_DIR.glob('*.txt'))

    random.shuffle(anno_files)

    files_count = len(anno_files)
    
    train_count = int(files_count * args.train_rate)
    eval_count = int(files_count * args.eval_rate)
    test_count = files_count - (train_count + eval_count)
    
    train_files = anno_files[:train_count]
    eval_files = anno_files[train_count:train_count+eval_count]
    test_files = anno_files[train_count+eval_count:]
    copy_files(train_files, TRAIN_DIR )
    copy_files(eval_files, EVAL_DIR)
    copy_files(test_files, TEST_DIR)

    class_txt = IMG_DIR / 'classes.txt'
    gen_yaml(TRAIN_DIR, EVAL_DIR, TEST_DIR, class_txt)
