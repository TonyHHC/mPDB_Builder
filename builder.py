import os
import sys
import codecs
import argparse



# main
if __name__ == '__main__':

    # 讀參數
    parser = argparse.ArgumentParser(
        prog='builder',
        description='uPDB 格式電子書建立程式'
    )
    
    parser.add_argument('bookName', help='請輸入書名')
    parser.add_argument('authorName', help='請輸入作者')
    parser.add_argument('txtSourceDir', help='請輸入原始文字檔目錄', type=int)
    parser.add_argument('startIndex', help='從第幾個 txt 檔開始建立', type=int)
    parser.add_argument('endIndex', help='截止的 txt 檔編號', type=int)
    parser.add_argument('ouputDir', help='輸出的 mPDB 檔路徑', default='./')

    args = parser.parse_args()

    # 檢查原始文字檔目錄合理性
    if not os.path.isdir(args.txtSourceDir):
        print('Error!! 原始文字檔目錄不存在')
        sys.exit(-1)

    #
    print('hello')