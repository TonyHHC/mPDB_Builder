import os
import sys
import argparse
import glob

from opencc import OpenCC

############################################################################################
# main
if __name__ == '__main__':

    # 初始化 OpenCC converter
    cc = OpenCC('s2tw')

    # 讀參數
    parser = argparse.ArgumentParser(
        prog='chineseConvert',
        description='簡繁中文轉換程式'
    )
    
    parser.add_argument('txtSourceDir', help='請輸入原始文字檔目錄')
    parser.add_argument('ouputDir', help='轉換完畢輸出的目錄')

    args = parser.parse_args()

    # 檢查原始文字檔目錄合理性
    if not os.path.isdir(args.txtSourceDir):
        print('Error!! 原始文字檔目錄不存在')
        sys.exit(-1)

    # 檢查轉換完畢輸出的目錄合理性
    if not os.path.isdir(args.ouputDir):
        try:
            os.mkdir(args.ouputDir) 
        except:
            print('Error!! 無法建立轉換完畢輸出的目錄')
            sys.exit(-1)

    # 開始轉換
    srcFiles = glob.glob(f"{args.txtSourceDir}\\*.txt")

    for eachFile in srcFiles:
        with open(eachFile, 'r', encoding='utf-8') as f:
            content = cc.convert(f.read())

        with open(f'{args.ouputDir}\\{os.path.basename(eachFile)}', 'w', encoding='utf-8') as f:
            f.write(content)

        print(f'==> 完成轉換 {args.ouputDir}\\{os.path.basename(eachFile)}')

    # 結束
    print('\n')
