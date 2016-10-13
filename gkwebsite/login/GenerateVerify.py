#encoding=utf-8
# 创建画布需要导入`Image`包
from random import randint
from PIL import Image
# 创建画笔需要导入`ImageDraw`包
from PIL import ImageDraw
# 导入字体需要导入`ImageFont`包
from PIL import ImageFont
# 导入StringIO模块
from StringIO import StringIO

import os

def gnrtyzm(width, height):
    # 验证码中的字符长度
    wordsCount = 4
    # 图片宽度
    width = int(width)
    # 图片高度
    height = int(height)
    # 字体大小设置
    size = int(min(width / wordsCount, height) / 1.5)
    bgColor = (randint(200, 255), randint(200, 255), randint(200, 255))  # 随机背景色（浅色）
    '''
    # 用到了Image的new函数
    # 第一个参数是颜色通道，这里使用了RGB通道，还有其他的一些通道，如CMYK之类的，但不用管
    # 第二个参数是由宽高组成的元组，数字
    # 第三个参数是图片的背景色，这里用rgb的颜色显示，例如( 255, 255, 255)，注意这是元组
    '''
    # 创建图像
    img = Image.new('RGB', (width, height), bgColor)
    '''
    # 用到了ImageFont的truetype函数，可以自动查询电脑中的字体
    # 第一个参数是字体名字
    # 第二个参数是字体大小
    # 注意这个是windows系统下默认的字体，其他系统自己找
    '''
    # 导入字体
    font = ImageFont.truetype(os.getcwd()+'/login/static/assets/fonts/mnfqh.otf', size)
    '''
    # 用到了`ImageDraw 的 Draw 函数
    # 有且只有一个参数，就是之前创建的画布
    '''
    # 创建画笔
    draw = ImageDraw.Draw(img)
    text = '1234567890ABCDEFGHIJKLMNPQRSTUVWXYZ'
    yzmString = ''
    for i in range(wordsCount):
        textColor = (randint(0, 160), randint(0, 160), randint(0, 160))
        left = width * i / wordsCount + (width / 4 - size) / 2
        top = (height - size) / 2
        '''
            # 写字需要使用`draw`的`text`方法
            # 第一个参数是一个坐标轴元组，分别是距离左边和上边的距离
            # 第二个参数是要写的字（字符串）
            # 后面的两个参数分别是字体和字体颜色
        '''
        randAlphabet = text[randint(0, len(text) - 1)]
        yzmString = yzmString + randAlphabet
        draw.text((left, top), randAlphabet, font=font, fill=textColor)

    for i in range(15):
         textColor = (255, 255, 255)
         left = randint(0, width)
         top = randint(0, height)
         draw.text((left, top), '*', font=font, fill=textColor)

    for i in range(5):
        linecolor = (randint(0, 160), randint(0, 160), randint(0, 160))
        line = (randint(0, width), randint(0, height), randint(0, width), randint(0, height))
        '''
            # 画线条需要使用`draw`的`line`方法
            # 第一个参数是包含了两个坐标的元组，分别是线条一头一尾的坐标
            # 后面的参数是线条的颜色
        '''
        draw.line(line, fill=linecolor)

    del draw
    # 建立一个缓存对象
    mstream = StringIO()
    # 将图片保存到内存中
    img.save(mstream, 'jpeg')
    # 返回内存中的图片
    return mstream.getvalue(), yzmString





