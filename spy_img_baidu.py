# -*- coding: utf-8 -*-  
import urllib2  
import re  
import os  
import sys  
import argparse

reload(sys)  
sys.setdefaultencoding("utf-8")  

  
'''
spy imgs by chrome, search keywords by www.baidu.com
spy imgs: 20 pages* 60 imgs= 1200 imgs (default)

'''
def spy_operation(nameFile, saveDir, save_num=1200, page_nums=20):
    
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"  
    headers = {'User-Agent':user_agent} 

    nameList = []
    with open(nameFile, "r") as fr:
        for line in fr:
            name = line.strip()
            if len(name) <= 0:
                continue
            nameList.append(name)
    
    for name in nameList:
        if not os.path.exists(os.path.join(saveDir, name)):
            os.makedirs(os.path.join(saveDir, name))

        imgs_nums = 0
        for i in range(page_nums):
            try:
                spy_nums = i*60
                url = "http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=" + name.replace(' ','%20') + "&cg=girl&rn=60&pn="+ str(spy_nums)
                req = urllib2.Request(url, headers=headers)   
                res = urllib2.urlopen(req)
                page = res.read()
                img_srcs = re.findall('"objURL":"(.*?)"', page, re.S)  
                print("name: {}, page: {}, img nums: {}".format(name, i+1, len(img_srcs)))
            except:
                print("{} spy error".format(name))
        
            for src in img_srcs:
                # print src
                img_type = src.split("?")[0].split(".")[-1]
                if img_type not in ["jpg", "jpeg", "png", "JPEG"]:
                    print("src type err: {}".format(src))
                    continue

                imgName = name + "_" + str(imgs_nums) + "." + img_type
                # print imgName
                savePath = os.path.join(saveDir, name, imgName)
                with open(savePath, "w") as fw:
                    try:
                        print("Downloading {}".format(imgName))
                        req = urllib2.Request(src, headers=headers)
                        img = urllib2.urlopen(src, timeout=20)
                        fw.write(img.read())
                    except:
                        print("save err download: {}".format(src))
                
                imgs_nums += 1
                if imgs_nums >= save_num:
                    break
            if imgs_nums >= save_num:
                break
    


if __name__ == '__main__':  

    parse = argparse.ArgumentParser(description="Download imgs")

    parse.add_argument('--input', required=True, type=str, help='name list file input')
    parse.add_argument('--output', required=True, type=str, help='imgs save dir')
    parse.add_argument('--save_nums', required=False, type=int, default=1200, help='the nums your want to spy')

    args = parse.parse_args()
    
    spy_operation(args.input, args.output, args.save_nums)
    print('download all imgs')
