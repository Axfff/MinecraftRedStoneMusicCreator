from PIL import Image,ImageDraw,ImageFont




def inputImage(filename):
    image_ = Image.open(filename)
    image = image_.convert('L')
    image_.close()
    return image




def getUsefulPoints(image,mark=150):
    points = []
    for x in range(image.width):
        for y in range(image.height):
            # print(image.getpixel((x,y)))
            if image.getpixel((x,y)) < mark :
                points.append((x,y))
                # print('t')

    min_x,min_y,max_x,max_y = 10000000,10000000,-10000000,-10000000
    for p in points:
        # print(p)
        min_x = min(p[0],min_x)
        min_y = min(p[1],min_y)
        max_x = max(p[0],max_x)
        max_y = max(p[1],max_y)
    trueW = max_x - min_x
    trueH = max_y - min_y
    # print(min_x,min_y,max_x,max_y)
    # print(trueW,trueH)

    for i in range(len(points)):
        points[i] = (
            points[i][0] - min_x - trueW//2 ,
            points[i][1] - min_y - trueH//2
        )

    return points




def creatCommand(x,y,particleName,size):
    speed = 100
    command = 'particle {} ~12 ~15 ~-0 {} {} {} {}'.format(particleName,speed,-1*y,x,size)
    return command




def creatFunction(functionName,points,particleName='endRod',size=0.01):
    particleCount = 0
    with open('%s.mcfunction'%functionName,'w') as f:
        for p in points:
            particleCount += 1
            command = creatCommand(p[0],p[1],particleName,size)
            f.write(command + '\n')
    print(particleCount)



def summomLightning(functionName,pos,lenth):
    with open('%s.mcfunction' % functionName, 'w') as f:
        for i in range(lenth):
            command1 = 'summon minecraft:lightning_bolt ~%s ~%s ~%s'%(pos[0]+i , pos[1] , pos[2])
            command2 = 'summon minecraft:lightning_bolt ~%s ~%s ~%s' %(pos[0]+i, pos[1], -1*pos[2])
            f.write(command1 + '\n')
            f.write(command2 + '\n')




def isChinese(text):
    if text >= u'\u4e00' and text <= u'\u9fa5':
        return True
    else:
        return False



def drawTexts(text):
    image = Image.new('L',(2000,400),255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("simhei", 20)

    num = 0
    posy = 10
    for t in text:
        if t == '$':
            posy += 22
            num = 0
            continue
        if isChinese(t):
            plusx = 19
        else:
            plusx = 8
        draw.text((40+plusx*num , posy),t,0,font)
        num+=1
    image.show()
    return image





if __name__ == '__main__':
    # creatFunction('AuthorName',getUsefulPoints(drawTexts(' BilibiliI$阿小飞飞飞')),size=0.02)
    # drawTexts('BilibiliI$阿小飞飞飞')
    # summomLightning('summonLightning',(-5,-10,4),50)

    # creatFunction('TitleImage',getUsefulPoints(inputImage('titlebws.jpg')))
    creatFunction('TitleImage', getUsefulPoints(drawTexts('新年快乐')))