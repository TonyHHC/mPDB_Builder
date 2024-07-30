import os
import sys
import codecs
import argparse

def putString(byteArray, tgtString, index):
    unicode_bytes = tgtString.encode('utf-8')
    byteArray[index:index+len(unicode_bytes)] = unicode_bytes

def putInt(byteArray, tgtValue, size, index):
    headers[index:index+size] = tgtValue.to_bytes(size, 'big')

# main
if __name__ == '__main__':

    # 讀參數
    parser = argparse.ArgumentParser(
        prog='builder',
        description='uPDB 格式電子書建立程式'
    )
    
    parser.add_argument('bookName', help='請輸入書名')
    parser.add_argument('authorName', help='請輸入作者')
    parser.add_argument('txtSourceDir', help='請輸入原始文字檔目錄')
    parser.add_argument('startIndex', help='從第幾個 txt 檔開始建立', type=int)
    parser.add_argument('endIndex', help='截止的 txt 檔編號', type=int)
    parser.add_argument('ouputDir', help='輸出的 mPDB 檔目錄', default='./')

    args = parser.parse_args()

    # 檢查原始文字檔目錄合理性
    if not os.path.isdir(args.txtSourceDir):
        print('Error!! 原始文字檔目錄不存在')
        sys.exit(-1)

    iRecords = 0
    for i in range(args.startIndex, args.endIndex+1):
        if os.path.isfile(f'{args.txtSourceDir}\\{i}.txt'):
            iRecords += 1

    if iRecords <= 0:
        print('Error!! 找不到指定範圍內的 txt 檔')
        sys.exit(-1)

    # 檢查輸出的 mPDB 檔路徑合理性
    if not os.path.isdir(args.ouputDir):
        try:
            os.mkdir(args.ouputDir) 
        except:
            print('Error!! 無法建立輸出的 mPDB 檔目錄')
            sys.exit(-1)

    # 初始化 Headers
    headers = bytearray(78)
    putString(headers, args.authorName, 0)
    headers[35] = 2
    putString(headers, 'BOOK', 60)
    putString(headers, 'MTIU', 64)
    putInt(headers, (iRecords+2), 2, 76)
    
    print(headers)

    '''
    tmp = bytes(headers[0:34+1]).decode('utf-8').strip('\x00')
    print(tmp)
    tmp = bytes(headers[64:67+1]).decode('utf-8')
    print(tmp)
    tmp = int.from_bytes(headers[76:78], 'big')
    print(tmp)
    '''
    
    #