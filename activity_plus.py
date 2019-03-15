

class zhijiang():
    def __init__(self,p):
        self.p=p

class manjian():
    def __init__(self,m,j):
        self.m=m
        self.j=j

class zhekou():
    def __init__(self,zhekou,maxm,m=1):
        self.zhekou=zhekou
        self.maxm=maxm
        self.m=m
class coupon():
    def __init__(self,m,face=0.0,discount=None,max=None,plus=True):
        self.m=m
        self.face=face
        self.discount=discount
        self.maxm=max
        self.plus=plus

def duce_math(money,price=6.0,plus_zj_mjzk = True):


    zj1 = zhijiang(1.2)

    # mj1 = manjian(10, 8.5)
    mj1 = manjian(m=300, j=61)
    mj2 = manjian(m=10, j=5)


    zk1 = zhekou(0.5, 15,m=5)
    zk2 = zhekou(0.4, 400,m=400)


    coupon1 = coupon(1, face=29.5, plus=False)
    coupon4 = coupon(50, discount=0.8, max=30, plus=False)

    coupon2 = coupon(1, face=9.1, plus=True)
    coupon3 = coupon(1, discount=0.2, max=50, plus=True)

    # 直降
    duce_zj = money / price * zj1.p

    # 满减
    if (money >= mj1.m):
        duce_mj1 = mj1.j
    else:
        duce_mj1 = 0

    if (money >= mj2.m):
        duce_mj2 = mj2.j
    else:
        duce_mj2 = 0
    duce_mj=max(duce_mj1,duce_mj2)

    # 折扣
    if(money>=zk1.m):
        duce_zk1 = min(money * zk1.zhekou, zk1.maxm)
    else:
        duce_zk1 = 0

    if (money >= zk2.m):
        duce_zk2 = min(money * zk2.zhekou, zk2.maxm)
    else:
        duce_zk2 = 0

    duce_zk=max(duce_zk1,duce_zk2)


    duce_mjzk = max(duce_mj, duce_zk)

    if (plus_zj_mjzk):
        duce_act = duce_mjzk + duce_zj
    else:
        duce_act = max(duce_mjzk, duce_zj)

    if (money >= 1):
        duce_coupon_plus1 = coupon2.face
        duce_coupon_plus2 = min(coupon3.discount * money, coupon3.maxm)
        duce_coupon_plus = max(duce_coupon_plus1, duce_coupon_plus2)

        duce_coupon_alone1 = coupon1.face

        if(money>=50):
            duce_coupon_alone2 = min(coupon4.discount * money, coupon4.maxm)
        else:
            duce_coupon_alone2=0
        duce_coupon_alone = max(duce_coupon_alone1, duce_coupon_alone2)

    else:
        duce_coupon_plus = 0
        duce_coupon_alone = 0

    duce_act_coupon = duce_act + duce_coupon_plus
    duce = max(duce_act_coupon, duce_coupon_alone)
    print('***************************',money,'*******************************')
    print('duce_zj:',duce_zj)
    print('duce_mj:',duce_mj)
    print('duce_zk:',duce_zk)
    print('duce_mjzk:',duce_mjzk)
    print('duce_coupon_plus:',duce_coupon_plus)
    print('duce_act_coupon:', duce_act_coupon)
    print('duce_coupon_alone:', duce_coupon_alone)




if __name__=='__main__':
    '''
    0   6.53
    90# 8.49
    92  6
    95  7.55
    98  7.2
    
    '''
    money_list=[1,10,20,30,50,100,200,300,400]
    for money in money_list:
        duce_math(price=6,money=money,plus_zj_mjzk=True)











