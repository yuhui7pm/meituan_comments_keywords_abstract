import base64
import zlib
# from config import urlParam

# 自己生成的url
testUrl = 'https://st.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%B1%95%E5%A4%B4&cataId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=&uuid=9d970503-048b-4298-8c6c-2f25b17eec77&platform=1&partner=126&originUrl=https%3A%2F%2Fst.meituan.com%2Fmeishi%2F&riskLevel=1&optimusCode=10&_token=eJxdkNtuozAURX+l4pUqtgkx0DfSQEhakkIgt2oegJDgcMtgAw2j+fexq1ErVfKR9l7ePj72H6lZnKSnBwShAeHjg9SlDbcSGsERlrhnVOxONJUvpCsIahwmP6gCdU7jZjvj+B1NMO+kIOPXJ/QFe0dYtOd3cPjf6FgYRRX1GV2IpJQxdqNPAFA2KlPC2qgaJXUJuKYZAWImSaTLQKSFyr9U9KXYN3PFe8QxSi6V0OmyL64B6/rB9C5AXq3ydIeVZDoLd6WZ78axra0hCSfIuZnrbN92qryZXTzZIubyOXUCXBwOh7feURujS16ue1M/I2Xl41frrXhpSaOpYaEN85MHHL0/fvzeqMFiYtXyVGUROc5qv8ObU4Wqa1ec7rSvMt2zgZtby3tXrfWqLnzPj6mxzlwfbSPW2o7ldHWcR7e+BuMhe5XxNoGE+kmltuRuN7ZGXf73shFBEPfoHJ/dYfcxh+NgH7NrmM1Jib15FFqDLf39B0rCj6c='
basicUrl = 'https://st.meituan.com/meishi/api/poi/getPoiList?'
paramUrl = 'cityName=%E6%B1%95%E5%A4%B4&cataId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=&uuid=9d970503-048b-4298-8c6c-2f25b17eec77&platform=1&partner=126&originUrl=https%3A%2F%2Fst.meituan.com%2Fmeishi%2F&riskLevel=1&optimusCode=10&'
token_ = 'eJxdkNtuozAURX+l4pUqtgkx0DfSQEhakkIgt2oegJDgcMtgAw2j+fexq1ErVfKR9l7ePj72H6lZnKSnBwShAeHjg9SlDbcSGsERlrhnVOxONJUvpCsIahwmP6gCdU7jZjvj+B1NMO+kIOPXJ/QFe0dYtOd3cPjf6FgYRRX1GV2IpJQxdqNPAFA2KlPC2qgaJXUJuKYZAWImSaTLQKSFyr9U9KXYN3PFe8QxSi6V0OmyL64B6/rB9C5AXq3ydIeVZDoLd6WZ78axra0hCSfIuZnrbN92qryZXTzZIubyOXUCXBwOh7feURujS16ue1M/I2Xl41frrXhpSaOpYaEN85MHHL0/fvzeqMFiYtXyVGUROc5qv8ObU4Wqa1ec7rSvMt2zgZtby3tXrfWqLnzPj6mxzlwfbSPW2o7ldHWcR7e+BuMhe5XxNoGE+kmltuRuN7ZGXf73shFBEPfoHJ/dYfcxh+NgH7NrmM1Jib15FFqDLf39B0rCj6c='
# 从美团获取的url
meituanUrl = 'https://st.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%B1%95%E5%A4%B4&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=&uuid=dbedded4-dad6-46c2-b3ed-3505a7eb2c51&platform=1&partner=126&originUrl=https%3A%2F%2Fst.meituan.com%2Fmeishi%2F&riskLevel=1&optimusCode=10&_token=eJx1j09zqjAUxb9LtmUEAgF0pguoUlAYDCKinS4UoyB%2FlBCV0ul3b5znW7zFW51zf%2FfMuck3oO4ejGRJGkqSAG6EghGQB9JAAwJgLd8gXUWaoUJdh0MBpP8wwzCgAHY0HoPRh6woqgBV5fNBQg7%2BEMMYfgpPq3ILH6FHxuURkDF2aUei2LJBRXJ23daD9FyJ3LdZLvI3%2FCcAeEMV8QauxVO3T2V%2FZ5%2F%2FhVe0%2BbHmjkzv5WkJZ%2FfCxBkR83OddnN0dk0dYmqGHbpPmiaeeYuEOFpFraNyHHtfljqNoNOnfXOIetLfZ5O1S6Cf%2B2cRz6mO3wI92KNDPyQWK%2FXipBZUZvFXWESbapWssxe8s%2BHGdbrqgKJpUkb1ix2slhsSrKy5isIsraKSXMe4rx0%2Fy2FOmJNEVVK8zXHcwXAb3JSrJl0wskqbLpuFeEN47WFtsvCO14ln8nPK2vaDWWvncozb3ful6Wi4P5wke1qbr6%2Fg5xc76ZOf'
meituanBasic = 'https://st.meituan.com/meishi/api/poi/getPoiList?'
meituanParam = 'cityName=%E6%B1%95%E5%A4%B4&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=&uuid=dbedded4-dad6-46c2-b3ed-3505a7eb2c51&platform=1&partner=126&originUrl=https%3A%2F%2Fst.meituan.com%2Fmeishi%2F&riskLevel=1&optimusCode=10&'
meituanToken = 'eJx1j09zqjAUxb9LtmUEAgF0pguoUlAYDCKinS4UoyB%2FlBCV0ul3b5znW7zFW51zf%2FfMuck3oO4ejGRJGkqSAG6EghGQB9JAAwJgLd8gXUWaoUJdh0MBpP8wwzCgAHY0HoPRh6woqgBV5fNBQg7%2BEMMYfgpPq3ILH6FHxuURkDF2aUei2LJBRXJ23daD9FyJ3LdZLvI3%2FCcAeEMV8QauxVO3T2V%2FZ5%2F%2FhVe0%2BbHmjkzv5WkJZ%2FfCxBkR83OddnN0dk0dYmqGHbpPmiaeeYuEOFpFraNyHHtfljqNoNOnfXOIetLfZ5O1S6Cf%2B2cRz6mO3wI92KNDPyQWK%2FXipBZUZvFXWESbapWssxe8s%2BHGdbrqgKJpUkb1ix2slhsSrKy5isIsraKSXMe4rx0%2Fy2FOmJNEVVK8zXHcwXAb3JSrJl0wskqbLpuFeEN47WFtsvCO14ln8nPK2vaDWWvncozb3ful6Wi4P5wke1qbr6%2Fg5xc76ZOf'
uuuuuuuuuuuu = 'eJx1j09zqjAUxb9LtmUEAgF0pguoUlAYDCKinS4UoyB/lBCV0ul3b5znW7zFW51zf/fMuck3oO4ejGRJGkqSAG6EghGQB9JAAwJgLd8gXUWaoUJdh0MBpP8wwzCgAHY0HoPRh6woqgBV5fNBQg7+EMMYfgpPq3ILH6FHxuURkDF2aUei2LJBRXJ23daD9FyJ3LdZLvI3/CcAeEMV8QauxVO3T2V/Z5//hVe0+bHmjkzv5WkJZ/fCxBkR83OddnN0dk0dYmqGHbpPmiaeeYuEOFpFraNyHHtfljqNoNOnfXOIetLfZ5O1S6Cf+2cRz6mO3wI92KNDPyQWK/XipBZUZvFXWESbapWssxe8s+HGdbrqgKJpUkb1ix2slhsSrKy5isIsraKSXMe4rx0/y2FOmJNEVVK8zXHcwXAb3JSrJl0wskqbLpuFeEN47WFtsvCO14ln8nPK2vaDWWvncozb3ful6Wi4P5wke1qbr6/g5xc76ZOf'
def decode_token(token):
    # base64解码
    token_decode = base64.b64decode(token.encode())
    # 二进制解压
    token_string = zlib.decompress(token_decode)
    return token_string

decode1 = decode_token(meituanToken)
print('对原始ajax请求解密一次：',decode1)

