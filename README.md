# uPDB (Unicode) 檔規格

1. PDB是源自Palm作業系統的一個單一檔案，簡易資料庫。
2. 每一個PDB檔含N筆不定長度的資料(record)。
3. PDB檔最前面當然要有個Header，定義本資料庫的特性。
4. 因資料長度非固定，無法計算位置。所以Header之後，是各筆資料所在的位置，可以用來讀資料及計算每筆資料的長度。
5. 之後，就是一筆一筆的資料，沒什麼大學問可言。

6. 檔案的前78個bytes，是Header[0..77]：
    + Header[0..34] 舊版是放書名，新版是放作者。可以不理。
    + Header[35] 是 2，舊版是 1。可以不理。
    + Header[36..43] 是為 Palm 而加的兩個日期，可以不理。
    + Header[44..59] 都是 0。可以不理。
    + Header[60..63] 是 "BOOK"。可以不理。
    + Header[64..67] 是判別的關鍵，PDB 是 "MTIT"，uPDB 是"MTIU"。
    + Header[68..75] 都是 0。可以不理。
    + Header[76..77] 是 record數 = N (章數) 加2 (目錄及書籤)。
7. 每筆資料的起始位置及屬性，依Palm的規格是8個bytes，前4個bytes是位置，後4個bytes是0。一共有 (N+2) * 8 bytes。
8. 第一筆資料定義書的屬性，是 8 個空白字元、書名、章數及目錄：
    + 8 個空白btyes，可以不理；
    + 之後接書名是 Unicode 碼，後接三個 ESC(即 27,0)；
    + 之後接章數 (ASCII string)，後接一個 ESC (27, 0)；
    + 之後接目錄，各章之標題是以 CR(13,0) NL(10,0) 分隔。
9. 再來是 N 筆資料，每筆是一章的內容，PDB 檔是 Big5 碼(是null-terminated string，最後一個byte是0)，uPDB檔是 Unicode 碼。
10. 第 N+2 筆資料是書籤，預設是 -1。可以不理。  

*註：以上內容來自好讀網站之有關 '新版 uPDB (Unicode) 及 PDB (Big5) 檔規格' 說明'*

*註：uPDB 的 Unicode 編碼是 UTF-16 编碼的字節數组*

# 使用方式

語法

    usage: builder [-h] bookName authorName txtSourceDir startIndex endIndex ouputDir

    uPDB 格式電子書建立程式

    positional arguments:
        bookName      請輸入書名
        authorName    請輸入作者
        txtSourceDir  請輸入原始文字檔目錄
        startIndex    從第幾個 txt 檔開始建立
        endIndex      截止的 txt 檔編號
        ouputDir      輸出的 mPDB 檔路徑

    options:
        -h, --help    show this help message and exit

範例

    python builder.py '聖堂一' '骷髏精靈' 'D:\Project\Tony\Python\重新下載聖堂\final' '1' '202' 'D:\Temp'

    python builder.py '聖堂二' '骷髏精靈' 'D:\Project\Tony\Python\重新下載聖堂\final' '203' '406' 'D:\Temp'
    
    python builder.py '聖堂三' '骷髏精靈' 'D:\Project\Tony\Python\重新下載聖堂\final' '407' '645' 'D:\Temp'
    
    python builder.py '聖堂四' '骷髏精靈' 'D:\Project\Tony\Python\重新下載聖堂\final' '646' '979' 'D:\Temp'
