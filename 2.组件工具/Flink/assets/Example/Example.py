# 使用 StreamTableEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings, DataTypes
from pyflink.table.udf import udf
import json,re,base64
from urllib import parse


# 解析 IP库的代码
from os.path import abspath, dirname
import struct
import socket

def ip_to_string(ip):
    """
    整数IP转化为IP字符串
    :param ip:
    :return:
    """
    return str(ip >> 24) + '.' + str((ip >> 16) & 0xff) + '.' + str((ip >> 8) & 0xff) + '.' + str(ip & 0xff)

def string_to_ip(s):
    """
    IP字符串转换为整数IP
    :param s:
    :return:
    """
    (ip,) = struct.unpack('I', socket.inet_aton(s))
    return ((ip >> 24) & 0xff) | ((ip & 0xff) << 24) | ((ip >> 8) & 0xff00) | ((ip & 0xff00) << 8)

class IPCz:
    # 数据文件路径
    __database_file = dirname(abspath(__file__)) + '/data/qqwry.dat'
    __cur_start_ip = None
    __cur_end_ip_offset = None
    __cur_end_ip = None

    def __init__(self):
        self.__f_db = open(self.__database_file, "rb")
        bs = self.__f_db.read(8)
        (self.__first_index, self.__last_index) = struct.unpack('II', bs)
        self.__index_count = int((self.__last_index - self.__first_index) / 7 + 1)

    def get_version(self):
        """
        获取版本信息，最后一条IP记录 255.255.255.0-255.255.255.255 是版本信息
        :return: str
        """
        s = self.get_ip_address(0xffffff00)
        return s

    def __get_area_addr(self, offset=0):
        if offset:
            self.__f_db.seek(offset)
        bs = self.__f_db.read(1)
        (byte,) = struct.unpack('B', bs)
        if byte == 0x01 or byte == 0x02:
            p = self.__get_long3()
            if p:
                return self.__get_offset_string(p)
            else:
                return ""
        else:
            self.__f_db.seek(-1, 1)
            return self.__get_offset_string(offset)

    def __get_addr(self, offset):
        """
        获取offset处记录区地址信息(包含国家和地区)
        如果是中国ip，则是 "xx省xx市 xxxxx地区" 这样的形式
        (比如:"福建省 电信", "澳大利亚 墨尔本Goldenit有限公司")
        :param offset:
        :return:str
        """
        self.__f_db.seek(offset + 4)
        bs = self.__f_db.read(1)
        (byte,) = struct.unpack('B', bs)
        if byte == 0x01:  # 重定向模式1
            country_offset = self.__get_long3()
            self.__f_db.seek(country_offset)
            bs = self.__f_db.read(1)
            (b,) = struct.unpack('B', bs)
            if b == 0x02:
                country_addr = self.__get_offset_string(self.__get_long3())
                self.__f_db.seek(country_offset + 4)
            else:
                country_addr = self.__get_offset_string(country_offset)
            area_addr = self.__get_area_addr()
        elif byte == 0x02:  # 重定向模式2
            country_addr = self.__get_offset_string(self.__get_long3())
            area_addr = self.__get_area_addr(offset + 8)
        else:  # 字符串模式
            country_addr = self.__get_offset_string(offset + 4)
            area_addr = self.__get_area_addr()
        return country_addr + " " + area_addr

    def __set_ip_range(self, index):
        offset = self.__first_index + index * 7
        self.__f_db.seek(offset)
        buf = self.__f_db.read(7)
        (self.__cur_start_ip, of1, of2) = struct.unpack("IHB", buf)
        self.__cur_end_ip_offset = of1 + (of2 << 16)
        self.__f_db.seek(self.__cur_end_ip_offset)
        buf = self.__f_db.read(4)
        (self.__cur_end_ip,) = struct.unpack("I", buf)

    def get_ip_address(self, ip):
        """
        通过ip查找其地址
        :param ip: (int or str)
        :return: str
        """
        if type(ip) == str:
            ip = string_to_ip(ip)
        L = 0
        R = self.__index_count - 1
        while L < R - 1:
            M = int((L + R) / 2)
            self.__set_ip_range(M)
            if ip == self.__cur_start_ip:
                L = M
                break
            if ip > self.__cur_start_ip:
                L = M
            else:
                R = M
        self.__set_ip_range(L)
        # version information, 255.255.255.X, urgy but useful
        if ip & 0xffffff00 == 0xffffff00:
            self.__set_ip_range(R)
        if self.__cur_start_ip <= ip <= self.__cur_end_ip:
            address = self.__get_addr(self.__cur_end_ip_offset)
        else:
            address = "未找到该IP的地址"
        return address

    def get_ip_range(self, ip):
        """
        返回ip所在记录的IP段
        :param  ip
        :return: str
        """
        if type(ip) == str:
            ip = string_to_ip(ip)
        self.get_ip_address(ip)
        return ip_to_string(self.__cur_start_ip) + ' - ' + ip_to_string(self.__cur_end_ip)

    def __get_offset_string(self, offset=0):
        """
        获取文件偏移处的字符串(以'\0'结尾)
        :param offset: 偏移
        :return: str
        """
        if offset:
            self.__f_db.seek(offset)
        bs = b''
        ch = self.__f_db.read(1)
        (byte,) = struct.unpack('B', ch)
        while byte != 0:
            bs += ch
            ch = self.__f_db.read(1)
            (byte,) = struct.unpack('B', ch)
        return bs.decode('gbk')

    def __get_long3(self, offset=0):
        """
        3字节的数值
        :param offset:
        :return:
        """
        if offset:
            self.__f_db.seek(offset)
        bs = self.__f_db.read(3)
        (a, b) = struct.unpack('HB', bs)
        return (b << 16) + a



@udf(result_type=DataTypes.STRING())
def get_ipinfo(ipstr):
    try:
      ip_address_rangge = IPCz().get_ip_address(ipstr)
      return ip_address_rangge
    except Exception as e:
      raise e


@udf(result_type=DataTypes.STRING())
def get_token(token):
    try:
      if len(token) > 32 and token.startswith('jlc'):
        return base64.b64decode(parse.unquote(token)[3:])[::-1][:32].decode()
      elif len(token) == 28:
        return token

      tmp = re.findall(r'userId=([\w]{32})',parse.unquote(token))
      if tmp:
        return tmp[0]
      tmp = re.findall(r'token=([\w=]*)',parse.unquote(token))
      if tmp:
        tmp_str = tmp[0]
        if tmp_str.startswith('jlc'):
          return str(base64.b64decode(tmp_str[3:])[::-1][:32]).decode()
    except Exception as e:
      pass



def log_processing():
    env_settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
    t_env = StreamTableEnvironment.create(environment_settings=env_settings)
    
    # specify connector and format jars
    t_env.get_config().get_configuration().set_string("pipeline.jars", "file:///Users/liuhongwei/.m2/repository/org/apache/flink/flink-connector-kafka_2.11/1.12.0/flink-connector-kafka_2.11-1.12.0.jar;" + \
                                                                       "file:///Users/liuhongwei/.m2/repository/net/sf/json-lib/json-lib/2.3/json-lib-2.3-jdk15.jar;" + \
                                                                       "file:///Users/liuhongwei/.m2/repository/org/apache/kafka/kafka-clients/2.4.1/kafka-clients-2.4.1.jar;" + \
                                                                       "file:///Users/liuhongwei/.m2/repository/com/aliyun/flink-connector-clickhouse/1.12.0/flink-connector-clickhouse-1.12.0.jar;" + \
                                                                       "file:///Users/liuhongwei/.m2/repository/org/apache/flink/flink-connector-jdbc_2.11/1.12.0/flink-connector-jdbc_2.11-1.12.0.jar;" + \
                                                                       "file:///Users/liuhongwei/.m2/repository/mysql/mysql-connector-java/8.0.20/mysql-connector-java-8.0.20.jar" )
    
    t_env.get_config().get_configuration().set_string("parallelism.default", "1")

    source_ddl = """
            CREATE TABLE kafka_table(
                `appKey` STRING,
                `tranceId` STRING,
                `userAgent` STRING,
                `userId` STRING,
                `token` STRING,
                `sessionId` STRING,
                `referer` STRING,
                `referrer` STRING,
                `pageUrl` STRING,
                `module` STRING,
                `subModule` STRING,
                `content` STRING,
                `stime` BIGINT,
                `docType` STRING,
                `goPageUrl` STRING,
                `ipAddress` STRING,
                `appVersion` STRING,
                `tempUid` STRING,
                `model` STRING,
                `packageName` STRING,
                `traceId` STRING,
                `reqTime` STRING,
                `reqUrl` STRING,
                `respTime` STRING,
                `respCode` STRING,
                `pageType` STRING,
                `openTime` STRING,
                `closeTime` STRING,
                `currentTime` STRING,
                `loadTime` STRING,
                `proctime` AS PROCTIME(),
                `eventTime` AS TO_TIMESTAMP(FROM_UNIXTIME(stime/1000, 'yyyy-MM-dd HH:mm:ss')),
                WATERMARK FOR eventTime AS eventTime - INTERVAL '5' SECOND 
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'markTopic',
              'properties.bootstrap.servers' = 'kafka01.tp.base.phd2.jianlc.jlc:9091,kafka02.tp.base.phd2.jianlc.jlc:9091',
              'properties.group.id' = 'test_3',
              'scan.startup.mode' = 'latest-offset', 
              'format' = 'json'
            )
            """

# 'scan.startup.mode' = 'earliest-offset', 
# 'scan.startup.mode' = 'latest-offset',

# docType,
# SPLIT_INDEX(ipAddress,',',0) ipAddress, 
# get_iplocal(ipAddress,'city_name') ipLocal,
# packageName 


    query_sql = """
        select 
          stime,
          appkey,
          userid,
          token,
          sessionid,
          traceid,
          referer,
          pageurl,
          COALESCE(module1,pageurl,referer) module1,
          COALESCE(submodule,module1,pageurl,referer) submodule,
          content,
          itemid,
          channel,
          packagename,
          useragent,
          ipaddress,
          SPLIT_INDEX(get_ipinfo(ipaddress), ' ',0) iplocal,
          SPLIT_INDEX(get_ipinfo(ipaddress), ' ',1) ipoperator
        from 
        (select 
          from_unixtime(stime/1000) stime,
          `appKey` appkey,
          COALESCE(userId, get_token(token), get_token(pageUrl), get_token(referrer),get_token(reqUrl)) userid, 
          `token`,
          `sessionId` sessionid,
          COALESCE(traceId, tranceId, tempUid) traceid,
          SPLIT_INDEX(SPLIT_INDEX(COALESCE(referer,referrer), '?', 0),'#',0) as referer,
          SPLIT_INDEX(SPLIT_INDEX(COALESCE(pageUrl,reqUrl), '?', 0),'#',0) as pageurl,
          case when `module` = '' then null else `module` end module1,
          case when subModule = '' then null else subModule end submodule,
          `content` content,
          COALESCE(
            REGEXP_EXTRACT(COALESCE(pageUrl,reqUrl),'(productId|goodsId|seckillId|id|type|orderSn|search)=([\\w%]+)',2),
            REGEXP_EXTRACT(content,'(productId)=([^\"^\}^&^\?^#\s]+)',2),
            REGEXP_EXTRACT(content,'\"(productId|id|SeckillId|goodsId|categoryId|referer|search|searchText|value|orderSn|logisticsId|orderId|sort|type|url)\":(\"?)([^,^\}^\"\s]+)(\"?)',3),
            REPLACE(content,'\n','')) as itemid,
          COALESCE(REGEXP_EXTRACT(COALESCE(pageUrl,reqUrl),'(channel)=([\\w%]+)',2),
            REGEXP_EXTRACT(content,'\"(channel)\":(\"?)([^,^\}^\"\s]*)(\"?)',3)) as channel,
          SPLIT_INDEX(ipAddress,',',0) ipaddress,
         packageName packagename,
         userAgent useragent
        from kafka_table 
        where COALESCE(pageUrl,`module`,subModule,referer,referrer,reqUrl) is not null) t
        where userid is not null
        """
# where (pageUrl is not null or `module` is not null or `subModule` is not null or referer is not null or referrer is not null ) 



    clickhouse_sql = f"""
        CREATE TABLE updaterecord(
          `stime` STRING,
          `appkey` STRING,
          `userid` STRING,
          `token` string,
          `sessionid` string,
          `traceid` string,
          `referer` STRING,
          `pageurl` STRING,
          `module1` string,
          `submodule` string,
          `content` string,
          `item` string,
          `channel` string,
          `ipaddress` string,
          `packagename` string,
          `useragent` string 
        ) WITH (
            'connector' = 'clickhouse',
            'url' = 'clickhouse://10.103.27.163:8123',
            'username' = 'root',
            'password' = 'xB4UnYZd',
            'database-name' = 'markpoint',        /* ClickHouse 数据库名，默认为 default */
            'table-name' = 'updaterecord'     /* ClickHouse 数据表名 */

        )
    """

    kafka_sink_sql = f"""
        CREATE TABLE kafka_sink (
          `stime` STRING,
          `appkey` STRING,
          `userid` STRING,
          `token` string,
          `sessionid` string,
          `traceid` string,
          `referer` STRING,
          `pageurl` STRING,
          `module1` string,
          `submodule` string,
          `content` string,
          `item` string,
          `channel` string,
          `packagename` string,
          `useragent` string,
          `ipaddress` string,
          `iplocal` string,
          `ipoperator` string
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'markTopic1',
            'properties.bootstrap.servers' = 'kafka01.tp.base.phd2.jianlc.jlc:9091,kafka02.tp.base.phd2.jianlc.jlc:9091',
            'properties.group.id' = 'test_3',
            'format' = 'json'
        )
    """

# 'sink.batch-size' = '1000',         /* batch 大小 */
# 'sink.flush-interval' = '1000',     /* flush 时间间隔 */
# 'sink.max-retries' = '3',           /* 最大重试次数 */
# 'sink.ignore-delete' = 'true'       /* 忽略 DELETE 并视 UPDATE 为 INSERT */

    # query_sql = """
    #   select
    #     referer,
    #     pageUrl,
    #     
    #   from 
    #   (select
    #     appKey,
    #     case when `module` is null or `module` = '' then null else `module` end module1,
    #     case when subModule is null or subModule = '' then null else subModule end subModule
    #   from source_table 
    #   where 
    #   ) tmp1
    # """


    sink_ddl = f"""
      CREATE TABLE print_table(
        `stime` STRING,
        `appkey` STRING,
        `userid` STring,
        `token` string,
        `sessionid` string,
        `traceid` string,
        `referer` STRING,
        `pageurl` STRING,
        `module1` string,
        `submodule` string,
        `content` string,
        `item` string,
        `channel` string,
        `ipaddress` string,
        `packagename` string,
        `useragent` string 
        ) WITH (
          'connector' = 'print'
        )
    """

    # 
    # 
    # 
#  
      
      

    t_env.create_temporary_function("get_token", get_token)
    t_env.create_temporary_function("get_ipinfo", get_ipinfo) 

    t_env.execute_sql(source_ddl)
    # t_env.execute_sql(sink_ddl)
    t_env.execute_sql(kafka_sink_sql)
    
    

    t_env.sql_query(query_sql) \
        .insert_into("kafka_sink")
    t_env.execute('to_markpoint1')

    # t_result = t_env.execute_sql(query_sql)
    # t_result.print()
    
    # source_t = t_env.from_path("source_table")
    # result = source_t.filter(source_t.appKey == "YSHAppAndroidIOSH5") \
    #   .window(Slide.over(lit(1).minutes) \
    #     .every(lit(1).minutes) \
    #     .on(source_t.user_action_time).alias("w")) \
    #     .group_by(source_t.token, source_t.appKey, col("w")) \
    #       .select(source_t.token, source_t.appKey, col("w").start.alias("stime"), source_t.token.count.alias("nums"))
    
    # result.execute_insert("sink_table").wait()


if __name__ == '__main__':
    log_processing()