import os
import sys
import argparse
import array

############################################################################################

# 將字串編碼為 UTF-16 編碼的數組
def String2UTF16(tgtString):
	utf16_encoded = tgtString.encode('utf-16')
	utf16_encoded_no_bom = utf16_encoded[2:] if utf16_encoded.startswith(b'\xff\xfe') else utf16_encoded
	
	return utf16_encoded_no_bom

def UTF162String(tgtArray):
	# 将數組轉換為 Uint16 數組
	uint16_array = array.array('H', tgtArray)
	# 將 Uint16 數組解碼為字串
	tgtString = uint16_array.tobytes().decode('utf-16')
	
	return tgtString

def putStringByUTF16(byteArray, tgtString, index):
    unicode_bytes = String2UTF16(tgtString)
    byteArray[index:index+len(unicode_bytes)] = unicode_bytes

def putStringByUTF8(byteArray, tgtString, index):
    unicode_bytes = tgtString.encode('utf-8')
    byteArray[index:index+len(unicode_bytes)] = unicode_bytes

def putInt(byteArray, tgtValue, size, index):
    byteArray[index:index+size] = tgtValue.to_bytes(size, 'big')

def getLineFromTXT(txtContent, lineNumber):
    tmp = UTF162String(txtContent).splitlines()
    return tmp[lineNumber-1]

def normalizeTXT(txtContent):
    lines = txtContent.splitlines()

    # 去除所有空白行（包括只包含空白字符的行）
    lines = [line for line in lines if line.strip()]

    formatted_lines = []

    # 添加第一行
    formatted_lines.append(lines[0].strip())

    if len(lines) > 1:
        # 添加兩個空白行
        formatted_lines.append('')
        formatted_lines.append('')

        # 添加第二行及後續行，並在每行之前添加兩個空白
        for i, line in enumerate(lines[1:]):
            formatted_lines.append('  ' + line.strip())
            # 在每行之間添加一個空白行
            formatted_lines.append('')

    formatted_content = '\n'.join(formatted_lines)
    return formatted_content



############################################################################################

############################################################################################
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
    fileLists = []
    for i in range(args.startIndex, args.endIndex+1):
        if os.path.isfile(f'{args.txtSourceDir}\\{i}.txt'):
            iRecords += 1
            fileLists.append(f'{args.txtSourceDir}\\{i}.txt')

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

    # 讀取所有 txt 檔
    txtContents = []
    for eachFile in fileLists:
        with open(eachFile, 'r', encoding='utf-8') as f:
            content = normalizeTXT(f.read())
            txtContents.append(String2UTF16(content))

    #print(txtContents)    

    # 初始化 Headers
    headers = bytearray(78)
    putStringByUTF16(headers, args.authorName, 0)
    headers[35] = 2
    putStringByUTF8(headers, 'BOOK', 60)
    putStringByUTF8(headers, 'MTIU', 64)
    putInt(headers, (iRecords+2), 2, 76)

    '''
    tmp = bytes(headers[0:34+1]).decode('utf-8').strip('\x00')
    print(tmp)
    tmp = bytes(headers[64:67+1]).decode('utf-8')
    print(tmp)
    tmp = int.from_bytes(headers[76:78], 'big')
    print(tmp)
    '''
    
    # 第一筆資料
    datas_1 = bytearray(b'\x20\x20\x20\x20\x20\x20\x20\x20')
    datas_1.extend(bytearray(8))
    datas_1.extend(String2UTF16(args.bookName))
    datas_1.extend(bytes([27, 0, 27, 0, 27, 0]))
    datas_1.extend(bytearray(str(iRecords), 'ascii'))
    datas_1.extend(bytes([27, 0]))

    for i, txtContent in enumerate(txtContents):
        chapterCaption = getLineFromTXT(txtContent, 1).strip()
        datas_1.extend(String2UTF16(chapterCaption))
        if i < (len(txtContents)-1):
            datas_1.extend(bytes([13, 0, 10, 0]))

    #print(datas_1)

    # 每筆資料的起始位置及屬性
    eachDataPos = bytearray((iRecords+2)*8)

    iIndex = 0
    iLastPos = 78 + ((iRecords+2)*8)
    putInt(eachDataPos, iLastPos, 4, iIndex)

    iIndex += 8
    iLastPos += len(datas_1)
    putInt(eachDataPos, iLastPos, 4, iIndex)

    for txtContent in txtContents:
        iIndex += 8
        iLastPos += len(txtContent)
        putInt(eachDataPos, iLastPos, 4, iIndex)
    
    #print(eachDataPos)

    # 第 N+2 筆資料
    data_N2 = bytearray(b'\xff\xff')

    # 開始建立 UPDB 檔案
    strOutputPath = args.ouputDir+f'\\{args.bookName}.updb'
    with open(strOutputPath, 'wb') as updb:
        # 輸出 header
        updb.write(headers)

        # 輸出 每筆資料的起始位置及屬性
        updb.write(eachDataPos)

        # 輸出 第一筆資料
        updb.write(datas_1)

        # 輸出 N 筆資料
        for txtContent in txtContents:
            updb.write(txtContent)

        # 輸出 第 N+2 筆資料
        updb.write(data_N2)

    # 結束
    print(f'\n完成建立 {strOutputPath}\n')
