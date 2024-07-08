import discord
from discord.ext import tasks
state = "None"
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True    # Enable guild intents
intents.members = True   # Enable member intents

client = discord.Client(intents=intents)

class Slot:
    def __init__(self,name,price,roleid):
        self.name=name
        self.price=price
        self.roleId=roleid

class Shop:
    def __init__(self):
        self.slots=[]
    def addSlot(self,name,price,roleid):
        self.slots.append(Slot(name,price,roleid))

class User:
    def __init__(self,name,id,bal):
        self.bal,self.name,self.id = bal,name,id
        self.workCD=0
        self.inventory=[]
    def subtractBal(self,val,nm):
        if self.bal >=val:
            self.bal-=val
            return [f"Вы приобрели: {nm}!",True]
        if self.bal <val:
            return [f"Не достаточно стредств для приобретения {nm}!",False]
    def addBal(self,val):
        self.bal+=val
    def workStartCd(self):
        self.workCD = 1500
class DB:
    def __init__(self):
        self.users=[]
    def addUser(self,name,id,bal):
        self.users.append(User(name,id,bal))


RED=0
BLUE=1
_IDS=(1259231988263419925,
      1259232356963979304,)
shoplist = open('shopList','r')
txt = shoplist.read()
nTxt = ""
hasPace=False
for i in txt:
    if i=="\n" and not hasPace:
        hasPace=True
        nTxt+=i
    if i!="\n":
        hasPace=False
        nTxt+=i
List=nTxt.split('\n')
if List[-1] == '':
    List.pop(-1)
shop = Shop()
name=""
price=""
roleid=""
state=0
for i in List:
    if i[-1] == ":" and state==0:
        name=""
        price=""
        roleid=""
        state=1
        continue
    if state==1:
        newtxt = i.split("=",1)
        name=newtxt[1]
        state=2
        continue
    if state==2:
        newtxt = i.split("=",1)
        price=newtxt[1]
        state=3
        continue
        
    if state==3:
        newtxt = i.split("=",1)
        roleid=newtxt[1]
        state=4
    if state==4:
        state=0
        shop.addSlot(name,price,roleid)
        continue
        
for i in shop.slots:
    print(i.name,i.price,i.roleId)

dblist = open('db','r')
txt = dblist.read()
nTxt = ""
hasPace=False
for i in txt:
    if i=="\n" and not hasPace:
        hasPace=True
        nTxt+=i
    if i!="\n":
        hasPace=False
        nTxt+=i
List=nTxt.split('\n')
if List[-1] == '':
    List.pop(-1)
users = DB()
name=""
id=""
bal=""
state=0
for i in List:
    if i[-1] == ":" and state==0:
        name=""
        id=""
        bal=""
        state=1
        continue
    if state==1:
        newtxt = i.split("=",1)
        name=newtxt[1]
        state=2
        continue
    if state==2:
        newtxt = i.split("=",1)
        id=newtxt[1]
        state=3
        continue
        
    if state==3:
        newtxt = i.split("=",1)
        bal=int(newtxt[1])
        state=4
    if state==4:
        state=0
        users.addUser(name,id,bal)
        continue
                
for i in users.users:
    print(i.name,i.bal,i.id)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    checkCooldowns.start()

@client.event
async def on_message(message):
    global state
    if message.channel.id == 1259233635933098096:
        embedshop = discord.Embed(
            title="Магазин Ролей",
            description="Это магазин где вы можете покупать роли.",
            color=discord.Color.blue()
        )

        for i in shop.slots:
            embedshop.add_field(name=f"{i.name}", value=f"{i.price}$\n*Чтобы купить, отправьте в чат команду:*\n$buy {i.roleId}", inline=False)
        if message.author == client.user:
            return
        if message.content.startswith('$shop'):
            await message.channel.send(embed=embedshop)
            return
        hasProbels=False
        for i in message.content:
            if i == " ":
                hasProbels=True
        if hasProbels:
            text = message.content.lower()
            newText = ""
            hasSpace=False
            for i in text:
                if i==" " and not hasSpace:
                    hasSpace=True
                    newText+=i
                elif i!=" ":
                    hasSpace=False
                    newText+=i

            table = newText.split(' ')
            if table[0] == "$buy":
                isuser=False
                for i in users.users:
                    if int(i.id) == message.author.id:
                        isuser=True
                if not isuser:
                    users.addUser(message.author.name,str(message.author.id),0)
                    isuser=True
                if isuser:
                    
                    for i in users.users:
                        if int(i.id) == message.author.id:
                            for d in shop.slots:
                                if d.roleId==table[1]:
                                    result = i.subtractBal(int(d.price),d.name)
                                    
                                    if result[1] == True:
                                        embedbought = discord.Embed(
                                            title=f"Вы купили {d.name}!",
                                            description=f"Ваш баланс: {i.bal}",
                                            color=discord.Color.green()
                                        )
                                        await message.channel.send(embed=embedbought)
                                        rl=message.guild.get_role(int(d.roleId))
                                        await message.author.add_roles(rl)
                                    elif result[1] == False:
                                        embednotBought = discord.Embed(
                                            title=f"Недостаточно средств для покупки {d.name}!",
                                            description=f"Ваш баланс: {i.bal}",
                                            color=discord.Color.red()
                                        )
                                        await message.channel.send(embed=embednotBought)
            
            if table[0] == "$sendmoney":
                
                isuser=False
                for i in users.users:
                    if int(i.id) == message.author.id:
                        isuser=True
                if not isuser:
                    users.addUser(message.author.name,str(message.author.id),0)
                    isuser=True
                isuser2=False
                for i in users.users:
                    if i.id == table[1]:
                        isuser2=True
                if not isuser2:
                    userr = message.guild.get_member(int(table[1]))
                    users.addUser(userr,table[1],0)
                    isuser2=True
                if isuser and isuser2:
                    
                    for i in users.users:
                        if int(i.id) == message.author.id:
                            for d in users.users:
                                if d.id == table[1] and int(d.id) != message.author.id:
                                    result = i.subtractBal(int(table[2]),"ss")
                                    d.addBal(int(table[2]))
                                    if result[1]:
                                        embedBought = discord.Embed(
                                            title=f"Успешно передали {d.name}, {table[2]}$!",
                                            description=f"Ваш баланс: {i.bal}",
                                            color=discord.Color.green()
                                        )
                                        await message.channel.send(embed=embedBought)
                                    if not result[1]:
                                        embednotBought = discord.Embed(
                                            title=f"Недостаточно средств для перевода {d.name}, {table[2]}$!",
                                            description=f"Ваш баланс: {i.bal}",
                                            color=discord.Color.red()
                                        )
                                        await message.channel.send(embed=embednotBought)
            if table[0]=="$clear":
                await message.delete()
                if message.author.guild_permissions.manage_messages:
                    await message.channel.purge(limit=int(table[1])+1)
                    embedWorked = discord.Embed(
                        title=f"Успешно удалено {table[1]} сообщений!",
                        color=discord.Color.green()
                    )
                    await message.channel.send(embed=embedWorked)
                    return
                else:
                    embednotWorked = discord.Embed(
                        title=f"У вас нету прав!",
                        color=discord.Color.red()
                    )
                    await message.channel.send(embed=embednotWorked)
                    return
        if message.content.startswith('$work'):
            isuser=False
            for i in users.users:
                if int(i.id) == message.author.id:
                    isuser=True
            if not isuser:
                users.addUser(message.author.name,str(message.author.id),0)
                isuser=True
            if isuser:
                for i in users.users:
                    if int(i.id) == message.author.id and i.workCD == 0:
                        i.workStartCd()
                        from random import randint
                        work=randint(5,17)
                        i.addBal(work)
                        embedWorked = discord.Embed(
                            title=f"Вы поработали и заработали {work}!",
                            color=discord.Color.green()
                        )
                        await message.channel.send(embed=embedWorked)
                    elif int(i.id) == message.author.id and i.workCD >0:
                        embednotWorked = discord.Embed(
                            title=f"Подождите ещё {i.workCD} перед работой!",
                            color=discord.Color.red()
                        )
                        await message.channel.send(embed=embednotWorked)

@tasks.loop(seconds=1)
async def checkCooldowns():
    for i in users.users:
        if i.workCD>0:
            i.workCD-=1
        elif i.workCD<=0:
            i.workCD=0
@checkCooldowns.before_loop
async def before_checkCooldowns():
    await client.wait_until_ready()  # Wait until the bot is ready

client.run('MTI1OTgzMTQ2OTU1MTkxNTA5OA.G-LPOy.ifNsockbHi0791VdSF0bWGhoW8KpM_3hU7Bl8w')
dbSaveTexts = []
for i in users.users:
    dbSaveTexts.append(f"user:\nname={i.name}\nid={i.id}\nbal={i.bal}\n")
dbFileSAveText=""
for i in dbSaveTexts:
    dbFileSAveText+=i
filesave = open('db','w')
filesave.write(dbFileSAveText)