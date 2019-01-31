import sql_server

ms = sql_server.MSSQL(host="192.168.10.32:1433", user="test", pwd="85442791", db="Ytny")

# order_id=input('输入order_id')
org_price = 0
org_oil_litre = 0
site_id = 0
product_type_id = 0
org_amt = 0
create_time = 0




# 平台优惠
'''
平台价格设置表格，油分类-油产品-省市区-油站：获取折扣价格时，条件越具体，优先级越高。
   优先级别从高到低为：
   1.油站+油产品
   2.油站+油分类(汽、柴油)
   3.省市区+油产品
   4.省市区+油分类
   5.省市+油产品
   6.省市+油分类
   7.省+油产品
   8.省+油分类
   9.油产品
   10.油分类
'''
def platform_price(order_id):
    s = 'select site_id,product_type_id,product_category from pit_oil_order where id=' + str(order_id)
    list = ms.ExecQuery(s)
    col = list[0][0]
    product_type_id = list[0][1]
    product_category = list[0][2]

    s = 'select id,district_id,city_id,province_id from pit_drp_site where id=' + str(col)
    site = ms.ExecQuery(s)

    # 1.油站+油产品
    s = 'select * from pit_oil_platform_price where site_id=' + str(site[0][0]) + ' and product_type_id=' + str(
        product_type_id) + ' and status=1'
    pit_oil_platform_price = ms.ExecQuery(s)

    # 2.油站+油分类(汽、柴油)
    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price where site_id=' + str(site[0][0]) + ' and product_category=' + str(
            product_category) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    # 3.省市区+油产品
    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price ' \
            'where district_id=' + str(site[0][1]) + ' and city_id= ' + str(site[0][2]) + ' and province_id=' + str(
            site[0][3]) + \
            ' and product_type_id=' + str(product_type_id) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    # 4.省市区+油分类
    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price ' \
            'where district_id=' + str(site[0][1]) + ' and city_id= ' + str(site[0][2]) + ' and province_id=' + str(
            site[0][3]) + \
            ' and product_category=' + str(product_category) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    # 5.
    # 省市 + 油产品
    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price ' \
            'where city_id= ' + str(site[0][2]) + ' and province_id=' + str(site[0][3]) + \
            ' and product_type_id=' + str(product_type_id) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    # 6.
    # 省市 + 油分类
    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price ' \
            'where city_id= ' + str(site[0][2]) + ' and province_id=' + str(site[0][3]) + \
            ' and product_category=' + str(product_category) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    # 7.
    # 省 + 油产品
    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price ' \
            'where  province_id=' + str(site[0][3]) + \
            ' and product_type_id=' + str(product_type_id) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    # 8.
    # 省 + 油分类
    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price ' \
            'where  province_id=' + str(site[0][3]) + \
            ' and product_category=' + str(product_category) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    # 9.
    # 油产品

    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price ' \
            'where  product_type_id=' + str(product_type_id) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    # 10.
    # 油分类
    if (len(pit_oil_platform_price) == 0):
        s = 'select * from pit_oil_platform_price ' \
            'where  product_category=' + str(product_category) + ' and status=1'
        pit_oil_platform_price = ms.ExecQuery(s)

    platform_discount_list = []
    # 有多条适用优惠设置，取最大优惠？
    for tmp_price in pit_oil_platform_price:
        if (tmp_price[7] == 1):
            discount_money = org_price * tmp_price[8] / 100 * org_oil_litre
            platform_discount_list.append(discount_money)
        else:
            discount_money = tmp_price[9] * org_oil_litre
            platform_discount_list.append(discount_money)
    return max(platform_discount_list)


# 油站活动，满减且每升直降  注意，如果是每升直降，则会影响加油升数，在优惠中不会再叠加了，
# 而满减，则是直接从加油金额中减去
def site_price(order_id):
    s = 'select * from pit_oil_site_activity ' \
        'where site_id=' + str(site_id) + ' and product_type_id=' + str(product_type_id) + \
        ' and start_time<=\'' + str(create_time) + '\' and end_time>=\'' + str(create_time) + '\''
    list = ms.ExecQuery(s)
    tmp_list = [0]

    for i in list:
        # discount_money_per_litre 验证加油升数是否正确
        if (i[7] == 1):
            org_oil_litre_site=org_amt/(org_price-i[9])
            if(org_oil_litre-org_oil_litre_site<0.0001):
                print('加油升数正常')
            else:
                print(org_oil_litre_site,'org_oil_litre_site')
                print(org_oil_litre_site,'org_oil_litre_site')
                exit('加油升数异常')
        # discount_fullcut
        elif (org_amt >= i[10]):
            site_money = i[11]
            tmp_list.append(site_money)

    return max(tmp_list)


def member_marketing(province_id,city_id,district_id):
    s='select * from  pit_oil_platform_activity where product_type_ids='+str(product_type_id)+\
      ' and start_time<='+str(create_time)+' and end_time>='+str(create_time) +\
      ' and limit_min_spend_money<='+str(org_amt)
    list=ms.ExecQuery(s)
    tmp_list=[]
    for i in list:
        if(len(i[14])!=0 ):
            if(province_id not in i[14]):
                continue
            elif(len(i[15]!=0)):
                if(city_id not in i[15]):
                    continue
                elif(len(i[17])!=0):
                    if(district_id not in i[17]):
                        continue
        #1立减 2折扣(如9.5折)
        if(i[6]==1):
            tmp_list.append(i[9])
        else:
            money=




def order_detail(col):
    s = 'select ' + col + ' from pit_oil_order where id=' + str(order_id)
    list = ms.ExecQuery(s)
    return list[0][0]


def com_select(table,col):
    s='select top 1000' + col + ' from '+table

    list=ms.ExecQuery(s)
    tmp_list=[]
    for i in list:
        tmp_list.append(i[0])
    return tmp_list

def site_detail(col,site_id):
    s = 'select ' + col + ' from pit_drp_site where id=' + str(site_id)
    list = ms.ExecQuery(s)
    return list[0][0]


if __name__ == '__main__':
    tmp_order0 = [18822826]
    # tmp_order1 = com_select('pit_oil_order','id')


    tmp_list = []
    for order_id in tmp_order0:
        #order
        org_price = order_detail('org_price')
        org_oil_litre = order_detail('org_oil_litre')
        site_id = order_detail('site_id')
        product_type_id = order_detail('product_type_id')
        org_amt = order_detail('org_amt')

        #site
        province_id=site_detail('province_id',site_id)
        city_id=site_detail('city_id',site_id)
        district_id=site_detail('district_id',site_id)


        # 修改字符，去掉多余的时间字符
        create_time = str( order_detail('create_time')).split('.')[0]
        dic_reduce={}
        dic_reduce['site']=site_price(order_id)
        dic_reduce['platform']=platform_price(order_id)
        tmp_list.append(dic_reduce)
    print('---------------------------------------')
    print(tmp_list)
