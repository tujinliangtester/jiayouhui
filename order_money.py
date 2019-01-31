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


# 油站活动，满减或每升直降
def site_price(order_id):
    s = 'select * from pit_oil_site_activity ' \
        'where site_id=' + str(site_id) + ' and product_type_id=' + str(product_type_id) + \
        ' and start_time>=\'' + str(create_time) + '\' and end_time<=\'' + str(create_time) + '\''
    list = ms.ExecQuery(s)
    tmp_list = [0]

    for i in list:
        # discount_money_per_litre
        if (i[7] == 1):
            site_money = i[9] * org_oil_litre
            tmp_list.append(site_money)

        # discount_fullcut
        elif (org_amt >= i[10]):
            site_money = i[11]
            tmp_list.append(site_money)

    return max(tmp_list)


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

if __name__ == '__main__':
    tmp_order0 = [18822532,
                  18822531,
                  18822530,
                  18822529,
                  18822528,
                  18822527,
                  18822526,
                  18822525,
                  18822524,
                  18822523,
                  18822522,
                  18822521,
                  18822520,
                  18822519,
                  18822518,
                  18822517,
                  18822516,
                  18822515,
                  18822514,
                  18822513,
                  18822512,
                  18822511,
                  18822510,
                  18822509,
                  18822508,
                  18822507,
                  18822506,
                  18822505,
                  18822504,
                  18822503,
                  18822502,
                  18822501,
                  18822500,
                  18822499,
                  18822498,
                  18822497,
                  18822496,
                  18822495,
                  18822494,
                  18822493,
                  18822492,
                  18822491,
                  18822490,
                  18822489,
                  18822488,
                  18822487,
                  18822486,
                  18822485]
    tmp_order1 = com_select('pit_oil_order','id')


    tmp_list = []
    for order_id in tmp_order1:
        org_price = order_detail('org_price')
        org_oil_litre = order_detail('org_oil_litre')
        site_id = order_detail('site_id')
        product_type_id = order_detail('product_type_id')
        org_amt = order_detail('org_amt')

        # 修改字符，去掉多余的时间字符
        create_time = str( order_detail('create_time')).split('.')[0]

        tmp_list.append(site_price(order_id))
    print('---------------------------------------')
    print(tmp_list)
    print(max(tmp_list))
