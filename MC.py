from mcpi.minecraft import Minecraft as Mc
import mcpi.block as Block
from mcpi.vec3 import Vec3
import midiRead,threading,time


# 连接到游戏
mc = Mc.create()




def createRoad(position,direction,distanse,material):
    if direction == 'x':
        EndPosDifference = Vec3(distanse-1,0,0)
    elif direction == '-x':
        EndPosDifference = Vec3(-1*distanse+1,0,0)
    elif direction == 'z':
        EndPosDifference = Vec3(0,0,distanse-1)
    elif direction == '-z':
        EndPosDifference = Vec3(0,0,-1*distanse+1)

    EndPos = position + EndPosDifference
    #print(position,EndPos)
    mc.setBlocks(position,EndPos,material)
    time.sleep(0.01)




def placeDiscontinuously(position,direction,distance,command):
    #Translate command into list
    sequence = []
    for block in command:
        times = 0
        if type(command[block]) == list:
            times = command[block][0]
        elif type(command[block]) == int:
            times = command[block]

        for ts in range(times):
            sequence.append(block)
    sequenceLength = len(sequence)
    # print(sequenceLength,sequence)

    for num in range(distance):
        if direction == 'x':
            NowPos = position + Vec3(num,0,0)
        elif direction == '-x':
            NowPos = position + Vec3(-1*num,0,0)
        elif direction == 'z':
            NowPos = position + Vec3(0,0,num)
        elif direction == '-z':
            NowPos = position + Vec3(0,0,-1*num)

        if not sequence[num % sequenceLength]:
            continue
        try:
            NBT = command[sequence[num%sequenceLength]][1]
            mc.setBlockWithNBT(NowPos,sequence[num%sequenceLength],'',NBT)
        except:
            mc.setBlock(NowPos, sequence[num % sequenceLength])
        # print(sequence[num%sequenceLength])




def placeRepeater(position,direction,disstance,tick,gapLength):
    if direction == 'x':
        cbPos = position + Vec3(-1, 0, 0)
        directionValue = 1
    elif direction == '-x':
        cbPos = position + Vec3(1, 0, 0)
        directionValue = 3
    elif direction == 'z':
        cbPos = position + Vec3(0, 0, -1)
        directionValue = 2
    elif direction == '-z':
        cbPos = position + Vec3(0, 0, 1)
        directionValue = 0

    repeaterTags = []
    repeaterCount = 1
    while tick > 4:
        repeaterTags.append(12+directionValue)
        tick -= 4
        repeaterCount += 1
    repeaterTags.append((tick-1)*4 + directionValue)

    unitLength = repeaterCount + gapLength
    repeaterTagPointer = 0
    for num in range(disstance):
        if (num % unitLength)+1 <= repeaterCount:
            nowRepeaterTag = repeaterTags[repeaterTagPointer%repeaterCount]
            repeaterTagPointer += 1
        else:
            continue

        if direction == 'x':
            cmdPos = '~%s ~ ~'%(num+1)
        elif direction == '-x':
            cmdPos = '~-%s ~ ~'% (num+1)
        elif direction == 'z':
            cmdPos = '~ ~ ~%s'% (num+1)
        elif direction == '-z':
            cmdPos = '~ ~ ~-%s'% (num+1)

        command = 'setblock %s unpowered_repeater %s'%(cmdPos,nowRepeaterTag)
        mc.setBlocks(cbPos,cbPos + Vec3(0, 1, 0), Block.AIR)
        mc.setBlockWithNBT(cbPos, Block.COMMAND_BLOCK, '',
                       '{Command:"%s"}'%command)
        time.sleep(0.05)
        mc.setBlock(cbPos+Vec3(0,1,0),Block.REDSTONE_BLOCK)
        time.sleep(0.05)





def createBase(position,direction,distance,gapMaterial,instrumentMaterial,NoteBGap,IsPlaceRepeater,bottom=None):
    createRoad(position - Vec3(0, 2, 0), direction, distance,bottom)
    placeDiscontinuously(position - Vec3(0, 1, 0), direction, distance, {gapMaterial: 1, instrumentMaterial: 1})
    placeDiscontinuously(position, direction, distance, {None: 1, NoteBGap: 1}) # REDSTONE_LAMP_INACTIVE
    if IsPlaceRepeater :
        placeRepeater(position, direction, distance, 1, 1)




def placeNoteblock (position,direction,sequence):
    num = -1
    for note in sequence:
        num += 2
        if direction == 'x':
            posDifference = Vec3(num,0,0)
        elif direction == '-x':
            posDifference = Vec3(-1*num,0,0)
        elif direction == 'z':
            posDifference = Vec3(0,0,num)
        elif direction == '-z':
            posDifference = Vec3(0,0,-1*num)

        if note == None:
            continue
        NBT = '{note:%s}'%note
        mc.setBlockWithNBT(position+posDifference , Block.NOTEBLOCK , '' , NBT)






if __name__ == '__main__':

    BottomBlock = None  #Block.WOOL_RED
    InstrumentBlock = Block.ICE_PACKED   #Block.CLAY  #Block.WOOL #Block.DIRT  #Block.GOLD_BLOCK  #Block.ICE_PACKED
    GapBlock = Block.CONCRETE_BLOCK_RED
    NoteblockGap = Block.CONCRETE_BLOCK_RED  #Block.REDSTONE_LAMP_INACTIVE  #Block.CONCRETE_BLOCK_RED
    # GapBlock = Block.AIR
    # NoteblockGap = Block.AIR
    IsPlaceRepeater = 0
    MidiName = 'Main02_3'

    pos = mc.player.getPos()       # 获取玩家坐标
    print('player position get')
    threading.Thread(target= lambda: createBase(pos,'x',1081,GapBlock,InstrumentBlock,NoteblockGap,IsPlaceRepeater,BottomBlock )).start()
    threading.Thread(target= lambda: placeNoteblock(pos,'x',midiRead.createSequence('%s.mid'%MidiName) )).start()

     # placeRepeater(pos, 'x', 500, 1, 1)