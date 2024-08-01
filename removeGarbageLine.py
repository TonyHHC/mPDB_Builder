import os
import sys
import argparse
import glob

############################################################################################
# main
if __name__ == '__main__':

    # 讀取 garbageWord 定義
    with open('.\\garbageWords.lst', 'r', encoding='utf-8') as file:
        garbageWords = file.read().splitlines()

    # 讀參數
    parser = argparse.ArgumentParser(
        prog='removeGarbageLine',
        description='將文字檔中不必要的行刪除掉'
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

    # 開始刪除
    srcFiles = glob.glob(f"{args.txtSourceDir}\\*.txt")

    for eachFile in srcFiles:
        print(f'處理 {args.ouputDir}\\{os.path.basename(eachFile)}')

        with open(eachFile, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines(True)

        firstLine = lines[0]
        chapterNumber = firstLine.split()[0]

        filtered_lines = []
    
        for i, line in enumerate(lines):
            bAppend = True
            if any(garbageWord in line for garbageWord in garbageWords):
                bAppend = False

            # 有時網路文章前幾行一直會出現重複章節名稱，所以刪除它
            if (0 < i <= 5) and (chapterNumber in line):
                bAppend = False

            if bAppend:
                filtered_lines.append(line)
            else:
                print(f'==> 刪除 {line.strip()}')

            

        with open(f'{args.ouputDir}\\{os.path.basename(eachFile)}', 'w', encoding='utf-8') as f:
            f.writelines(filtered_lines)

    # 結束
    print('\n')
