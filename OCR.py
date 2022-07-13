
import ddddocr

def ddocr(file):
    try:
        ocr = ddddocr.DdddOcr()
        with open(file, 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        return res
    except:
        print("获取验证码失败，请继续！")



