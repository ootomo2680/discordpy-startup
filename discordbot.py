import discord
from discord.ext import commands
import os
import random
import cv2
import numpy as np
import re
import unicodedata
import pandas as pd
import codecs as cd

token = "Njg1MTgxMTU3NTc0MzExOTc0.XmE8jQ._u3dNhxVAuxMRPlb2w11IeJaBaA"
prefix = '$'
client = discord.Client()
'''
df0 = pd.read_csv('0.csv')
df0 = pd.read_csv('0.csv')
df0 = pd.read_csv('0.csv')
df0 = pd.read_csv('0.csv')
df0 = pd.read_csv('0.csv')
df0 = pd.read_csv('0.csv')
'''



helpmessage = ( '```\n'
                '0.ヘルプ:\n'
                '  $help          コマンド一覧を表示\n'
                '1.モミール:\n'
                '  $dm{N}         無作為に選ばれたコスト{N}のクリーチャー(NEO, サイキック, 禁断を含む)を表示\n'
                '  $gr{N}         無作為に選ばれたGRクリーチャーを{N}枚表示({N}は省略可)\n'
                '  $st{N}         無作為に選ばれた「S・トリガー」を持つ呪文を{N}枚表示({N}は省略可)\n'
                '  $rule          デュエマモミールのルール(暫定)を表示\n'
                '2.TRPG:\n'
                '  ${N}d{M}       {M}面ダイスを{N}回振る\n'
                '  $fumble        ファンブル表を振る\n'
                '  $hencho        変調表を振る\n'
                '  $kanjo         感情表を振る\n'
                '  $scene         シーン表を振る\n'
                '  $senjo         戦場表を振る\n'
                '```\n'
                )

def dice(dice_size):
    num = np.random.randint(1, int(dice_size))
    return num

def simple_dice(dice_size, dice_num):
    dice_val = np.array([], dtype=np.int64)
    for i in range(dice_num):
        dice_val = np.append(dice_val, dice(dice_size))
    return dice_val

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                                        for im in im_list]
    return cv2.hconcat(im_list_resize)

def dmomir(arg):
    """無作為に選ばれたコスト<arg>のクリーチャー(NEO, サイキック, 禁断を含む)を表示"""
    # with cd.open(str(arg)+'.csv', "r", "Shift-JIS", "ignore") as csv_file:
        # df = pd.read_table(csv_file, delimiter=",",names=["name","type","img","civ","pow","cost","race","abl"])
    df = pd.read_csv(str(arg)+'.csv', encoding='utf_8_sig')
    s = df.sample()
    print(s)
    name = str(s['name'].values[0])
    typ = str(s['type'].values[0])
    img = str(s['img'].values[0])
    civ = str(s['civ'].values[0])
    cost = str(s['cost'].values[0])
    power = str(s['pow'].values[0])
    race = str(s['race'].values[0])
    abl = s['abl'].values[0]
    info = '{0} [{1}] ({2}) {3}\n{4} -- {5}\n```{6}```'.format(name,civ,cost,typ,race,power,abl)
    return info,img
    
def trigger():
    """無作為に選ばれた「S・トリガー」を持つ呪文を<arg>枚表示"""
    df = pd.read_csv('st.csv', encoding='utf_8_sig')
    s = df.sample()
    print(s)
    name = str(s['name'].values[0])
    img = str(s['img'].values[0])
    civ = str(s['civ'].values[0])
    cost = str(s['cost'].values[0])
    race = str(s['race'].values[0])
    abl = s['abl'].values[0]
    info = '{0} [{1}] ({2})\n```{3}```'.format(name,civ,cost,abl)
    return info,img

def gr():
    """無作為に選ばれたGRクリーチャーを<arg>枚表示"""
    df = pd.read_csv('gr.csv', encoding='utf_8_sig')
    s = df.sample()
    print(s)
    name = str(s['name'].values[0])
    typ = str(s['type'].values[0])
    img = str(s['img'].values[0])
    civ = str(s['civ'].values[0])
    cost = str(s['cost'].values[0])
    power = str(s['pow'].values[0])
    race = str(s['race'].values[0])
    abl = s['abl'].values[0]
    info = '{0} [{1}] ({2}) {3}\n{4} -- {5}\n```{6}```'.format(name,civ,cost,typ,race,power,abl)
    return info,img

def rule():
    """デュエマモミールのルール(暫定)を表示"""
    return ("```"
            "■プレイヤーは自分のメインステップ中に一度，カードを1枚捨て，マナゾーンのカードを好きな数タップしてもよい。\n"
            " そうしたら，コストがそれと同じ数の進化でないクリーチャーを無作為に選び，コストを支払ったものとして召喚する。\n"
            " このようにしてバトルゾーンに出たサイキック・クリーチャーを裏返すことはできない。\n"
            "■プレイヤーがGR召喚をする時，かわりにすべてのGRクリーチャーから無作為に選び，召喚する(GR召喚として扱う)。\n"
            "■バトルゾーンのクリーチャーがゲーム中にバトルゾーン以外のゾーンに行った場合，消滅する。これはルール上の処理として行う。\n"
            "■手札と山札とマナゾーンと墓地とシールドゾーンにあるカードのコストと効果とカードタイプと名前は無視される(コストを参照する場合は0とする)。\n"
            "■ゲーム開始時，山札の上から5枚をシールドとして置く時，かわりに3枚(←要調整)をシールドとして置く。\n"
            " ただし、シールドゾーンにあるカードを手札に加える時、かわりに無作為に選ばれたS・トリガーを持つ呪文として扱ってもよい。\n"
            "```"
            )

def rush():
    """ランダムにカードを抽選"""
    path = './rush'
    dirs = os.listdir(path)    
    fl = random.choice(dirs)
    image = '{0}/{1}'.format(path, fl)
    return image


def kanjo():
    """感情表を振る"""
    i = random.randrange(1,7,1)
    num_to_kanjo = {1:"1: 共感/不信", 2:"2: 友情/怒り", 3:"3: 愛情/妬み", 4:"4: 忠誠/侮蔑", 5:"5: 憧憬/劣等感", 6:"6: 狂信/殺意"}
    val = num_to_kanjo[i]
    return val

def senjo():
    """戦場表を振る(括弧内は効果)"""
    i = random.randrange(1,7,1)
    num_to_senjo = {1:"1: 平地\n特になし", 2:"2: 水中\n回避判定-2", 3:"3: 高所\nファンブル時接近戦ダメージ1点", 
                    4:"4: 悪天候\n攻撃忍法の間合+1", 5:"5: 雑踏\nファンブル値+1", 
                    6:"6: 極地\nラウンド終了時GMは1D6を振る。戦闘開始時からの経過ラウンド以下の目が出たとき接近戦ダメージを1点受ける。この戦場から脱落したときランダムに変調を受ける)"}
    val = num_to_senjo[i]
    return val

def hencho():
    """変調表を振る"""
    i = random.randrange(1,7,1)
    num_to_hencho ={1:"1: 故障\n忍具が使用不能になる(累積しない)\n各サイクル終了時《絡繰術》で判定し成功で解除", 
                    2:"2: マヒ\n修得している特技一つをランダムに選び，使用不能にする(特技の数だけ累積)\n各サイクル終了時《身体操術》で判定し成功ですべて解除", 
                    3:"3: 重傷\n命中・情報・感情判定を行うたび接近戦ダメージ1点(累積しない)\n各サイクル終了時《生存術》で判定し成功で解除", 
                    4:"4: 行方不明\nメインフェイズ中自分以外のシーンに登場不可(累積しない)\n各サイクル終了時《経済力》で判定し成功で解除", 
                    5:"5: 忘却\n獲得している【感情】一つをランダムに選び，持っていないものとして扱う(【感情】の数だけ累積)\n各サイクル終了時《記憶術》で判定し成功ですべて解除", 
                    6:"6: 呪い\n修得している忍法一つをランダムに選び，修得していないものとして扱う(忍法の数だけ累積)\n各サイクル終了時《呪術》で判定し成功ですべて解除"}
    val = num_to_hencho[i]
    return val

def fumble():
    """ファンブル表を振る"""
    i = random.randrange(1,7,1)
    num_to_kanjo = {1:"1: 何か調子がおかしい。そのサイクルの間、すべての行為判定にマイナス１の修正がつく。", 
                    2:"2: しまった！　好きな忍具を１つ失ってしまう。", 
                    3:"3: 情報が漏れる！　このゲームであなたが獲得した【秘密】は、他のキャラクター全員の知るところとなる。", 
                    4:"4: 油断した！　術の制御に失敗し、好きな【生命力】を１点失う。", 
                    5:"5: 敵の陰謀か？　罠にかかり、ランダムに選んだ変調１つを受ける。変調は、変調表で決定すること。", 
                    6:"6: ふう。危ないところだった。特に何も起こらない。"}
    val = num_to_kanjo[i]
    return val

def scene():
    """シーン表を振る"""
    x = np.sum(simple_dice(6,2))
    if x == 2:
        val = "2: 血の匂いがあたりに充満している。何者かの戦いがあった気配。いや？まだ戦いは続いているのだろうか？"
    elif x == 3:
        val = "3: これは……夢か？　もう終わったはずの過去。しかし、それを忘れることはできない。"
    elif x == 4:
        val = "4: 眼下に広がる街並みを眺める。ここからなら街を一望できるが……。"
    elif x == 5:
        val = "5: 世界の終わりのような暗黒。暗闇の中、お前達は密やかに囁く。"
    elif x == 6:
        val = "6: 優しい時間が過ぎていく。影の世界のことを忘れてしまいそうだ。"
    elif x == 7:
        val = "7: 清廉な気配が漂う森の中。鳥の囀りや、そよ風が樹々を通り過ぎる音が聞こえる。"
    elif x == 8:
        val = "8: 凄まじい人混み。喧噪。影の世界のことを知らない無邪気な人々の手柄話や無駄話が騒がしい。"
    elif x == 9:
        val = "9: 強い雨が降り出す。人々は、軒を求めて、大慌てて駆けだしていく。"
    elif x == 10:
        val = "10: 大きな風が吹き荒ぶ。髪の毛や衣服が大きく揺れる。何かが起こりそうな予感……"
    elif x == 11:
        val = "11: 酔っぱらいの怒号。客引きたちの呼び声。女たちの嬌声。いつもの繁華街の一幕だが。"
    elif x == 12:
        val = "12: 太陽の微笑みがあなたを包み込む。影の世界の住人には、あまりにまぶしすぎる。"
    return val

@client.event
async def on_ready():
    print('Logged in')
    print('-----')

@client.event
async def on_message(message):
    # 開始ワード
    if message.content.startswith(prefix):
        # 送り主がBotではないか
        if client.user != message.author:
            msg = message.content.lstrip(prefix)
            #dmomir
            if msg.startswith('dm'):
                info = msg.lstrip('dm ')
                if info.isdecimal():
                    data = dmomir(info)
                    await message.channel.send(message.author.mention + '\n' + re.sub(r'\\n','\n',data[0]), file=discord.File(data[1]))
            elif msg.startswith('st'):
                info = msg.lstrip('st ')
                if info == '':
                    data = trigger()
                    await message.channel.send(message.author.mention + '\n' + re.sub(r'\\n','\n',data[0]), file=discord.File(data[1]))
                elif info.isdecimal():
                    data = trigger()
                    s = data[0]
                    im1 = imread(data[1])
                    for i in range(int(info)-1):
                        data = trigger()
                        s = s + data[0]
                        im2 = imread(data[1])
                        im1 = hconcat_resize_min([im1, im2])
                    cv2.imwrite('data/triggers.jpg', im1)
                    await message.channel.send(message.author.mention + '\n' + re.sub(r'\\n','\n',s), file=discord.File('data/triggers.jpg'))
            elif msg.startswith('gr'):
                info = msg.lstrip('gr ')
                if info == '':
                    data = gr()
                    await message.channel.send(message.author.mention + '\n' + re.sub(r'\\n','\n',data[0]), file=discord.File(data[1]))
                elif info.isdecimal():
                    data = gr()
                    s = data[0]
                    im1 = imread(data[1])
                    for i in range(int(info)-1):
                        data = gr()
                        s = s + data[0]
                        im2 = imread(data[1])
                        im1 = hconcat_resize_min([im1, im2])
                    cv2.imwrite('data/grs.jpg', im1)
                    await message.channel.send(message.author.mention + '\n' + re.sub(r'\\n','\n',s), file=discord.File('data/grs.jpg'))
            elif msg.startswith('rule'):
                await message.channel.send(rule())
            elif msg.startswith('rush'):
                info = msg.lstrip('rush ')
                if info == '':
                    await message.channel.send(message.author.mention, file=discord.File(rush()))
                elif info.isdecimal():
                    im1 = cv2.imread(rush())
                    for i in range(int(info)-1):
                        im2 = cv2.imread(rush())
                        im1 = hconcat_resize_min([im1, im2])
                    cv2.imwrite('data/rushs.jpg', im1)
                    await message.channel.send(message.author.mention, file=discord.File('data/rushs.jpg'))
            #trpg
            elif msg.startswith('kanjo'):
                await message.channel.send(message.author.mention + ' ' + kanjo())
            elif msg.startswith('senjo'):
                await message.channel.send(message.author.mention + ' ' + senjo())
            elif msg.startswith('hencho'):
                await message.channel.send(message.author.mention + ' ' + hencho())
            elif msg.startswith('fumble'):
                await message.channel.send(message.author.mention + ' ' + fumble())
            elif msg.startswith('scene'):
                await message.channel.send(scene())
            #help
            elif msg.startswith('help'):
                await message.channel.send(helpmessage)
            #dice
            else:
                info = re.split('\D+', message.content)
                print(info)
                if info:
                    if info[1].isdecimal() and info[2].isdecimal():
                        dice_num = int(info[1])
                        dice_size = int(info[2])
                        val = simple_dice(dice_size, dice_num)
                        await message.channel.send(message.author.mention + ' ' + str(dice_num) + 'd' + str(dice_size) + ': ' + str(val) + ' = ' + '**[' + str(np.sum(val)) + ']**')

client.run(token)


    
