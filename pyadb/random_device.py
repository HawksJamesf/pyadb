
import random
macs = ['d8:9b:3b:6d:71:a5', 'd8:9b:3b:6d:72:c4', '88:f5:6e:06:6d:7a',
        '70:3a:51:88:f3:91', '80:ad:16:5d:58:38', '9c:99:a0:5c:63:a5',
        'f8:e7:a0:8c:ed:a5',
        '24:79:f3:a5:ef:31', 'c0:2e:25:da:a4:8f']
table = {'38e7a0': 'vivo/V1911A/PD1911', '2479f3': 'OPPO/PCAM10/PCAM10', '002e25': 'OPPO/PCGM00/PCGM00',
         '389a78': 'HONOR/YAL-AL00/YAL-AL00', '189b3b': 'HUAWEI/POT-AL00a/POT-AL00a', '08f56e': 'HUAWEI/MAR-AL00/MAR-AL00',
         '303a51': 'xiaomi/Redmi Note 7/lavender', '00ad16': 'xiaomi/MI 5X/tiffany', '1c99a0': 'Xiaomi/MI 4LTE/cancro_wc_lte'}


def parse_mac(mac_bytes: bytes = None, mac_str: str = 0):
    '''
    MAC地址共48位（6个字节），以十六进制表示。第1Bit为广播地址(0)/群播地址(1)，第2Bit为广域地址(0)/区域地址(1)。前3~24位由IEEE决定如何分配给每一家制造商，且不重复，后24位由实际生产该网络设备的厂商自行指定且不重复。
    vivo/V1911A/PD1911:f8:e7:a0:8c:ed:a5
    vivo厂商：3-24位固定值：0x38E7A0
    HONOR/YAL-AL00/AL-AL00:f8:9a:78:50:2f:7e
    HONOR厂商：3-24位固定值:0x389a78
    '''
    mac = None
    if mac_bytes:
        mac = bytearray(mac_bytes)
    elif mac_str:
        mac = bytearray([int(e, base=16)
                         for e in mac_str.strip().split(':')])
    if mac is None:
        return None

    m3 = mac[:3]
    first_bit = m3[0] >> 7
    second_bit = (m3[0] >> 6) & 0b01
    m3[0] &= 0b00111111
    dom = m3.hex()
    dom_name = table.get(dom)
    m3_6 = mac[3:6]

    return first_bit, second_bit, (dom_name, dom), m3_6.hex()


def random_mac(origin: str):
    m3 = origin.strip()[:8]
    random_num4 = random.randint(0, 0xff)
    random_num5 = random.randint(0, 0xff)
    random_num6 = random.randint(0, 0xff)
    mac = '%s:%02x:%02x:%02x' % (
        m3, random_num4, random_num5, random_num6)
    return mac


def random_imei(origin: str):
    '''
    [imei info](https://www.imei.info/)
    [imei wiki](https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity)
    [imei ppt](https://www.gsma.com/latinamerica/wp-content/uploads/2018/06/GSMA-TAC-Allocation-and-IMEI-Training-Guide-Programming-Rules-v1.0.pdf)
    [imei gsma](https://web.archive.org/web/20170911150130/https://www.gsma.com/newsroom/wp-content/uploads/2012/06/ts0660tacallocationprocessapproved.pdf)
    [oppo check imei](https://www.oppo.com/cn/service/phonecheck)
    [vivo check imei](https://www.vivo.com.cn/service/authenticityCheck/query)
                AA	-	BB	BB	BB	-	CC	CC	CC	       D or EE
    Old IMEI	TAC	            |FAC	Serial number	D = Check Digit (CD) (Optional)
    New IMEI	TAC
    Old IMEISV	TAC	            |FAC	                EE = Software Version Number (SVN)
    New IMEISV	TAC

    NNXXXX YY ZZZZZZ A
    vivo/PD1911/V1911A
    imeis: {'86-921104-303595-8', '86-921104-303594-1'}

    OPPO/PCGM00/PCGM00
    imei: {'86-974704-205025-8', '86-974704-205024-1'}
    OPPO/PCGM00/PCGM00
    imei: {'86-974704-204978-9', '86-974704-204979-7'}

    OPPO/PCAM10/PCAM10
    imei: {'86-292804-944520-7', '86-292804-944521-5'}
    OPPO/PCAM10/PCAM10
    imei: {'86-292804-944518-1', '86-292804-944519-9'}

    HUAWEI/POT-AL00a/POT-AL00a
    imei: {'86-862904-872932-8', '86-862904-870563-3'}

    同一种model的设备，前8位(tac)是一样的,但是后6位(sn)却不能相同
    不同的model，前8位(tac)不能相同

    数字检查： Luhn algorithm
    - Starting from the right, double every other digit (e.g., 7 → 14).
    - Sum the digits (e.g., 14 → 1 + 4).
    - Check if the sum is divisible by 10.

    '''
    def luhn_algorithm(seq: list) -> str:
        ret = 0
        for i in range(len(seq)-1, -1, -1):
            if i % 2 == 0:
                ret += seq[i]
            else:
                n = seq[i] * 2
                if n >= 10:
                    ret += (n//10 + n % 10)
                else:
                    ret += n

        check_digist = (ret//10*10+10)-ret
        return check_digist

    def recursing(tac):
        def random_sn():
            r = '%s' % random.randint(100000, 999999)
            sn = [int(r[i])
                  for i in range(0, len(r))]
            return sn
        new_imei = list()
        new_imei.extend(tac)
        new_imei.extend(random_sn())
        check_digist = luhn_algorithm(new_imei)
        if check_digist != 0:
            new_imei.append(check_digist)
            return new_imei
        return recursing(tac)
    tac = [int(origin[i]) for i in range(0, len(origin))][:8]

    new_imei = recursing(tac)
    s = ''
    for e in new_imei:
        s += str(e)
    return s


def random_android_id(origin: str):
    pass


def random_ip(origin: str):
    pass


def random_battery(origin: str):
    pass


def random_location(origin: str):
    pass


def main():
    print('='*20)
    print(parse_mac(mac_bytes=bytes(
        [0xf8, 0x9a, 0x78, 0x50, 0x2f, 0x7e])))
    for m in macs:
        print(parse_mac(mac_str=m))
    print('='*20)
    for m in macs:
        print('origin mac:', m, 'new:', random_mac(m))
    # for m in imeis:
    print('origin imei ', '869747042050258',
          'new:', random_imei('869747042050258'))


if __name__ == '__main__':
    main()