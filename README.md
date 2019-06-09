# 小明
小明是一个可运行于Windows、Linux等平台的基于语音交互的虚拟个人助理，目前为止它具备背诵古诗、天气查询、文本翻译、
百科知识、新闻查询、联系人管理、笔记、代发微信消息和时钟功能。本文介绍如何在Linux平台下安装配置和使用该系统，
其他平台上的安装配置过程也基本一致，在此不多做介绍。

![](https://raw.githubusercontent.com/dwniaoniao/Xiaoming/ui/img/test.png?token=AHB4P6EAXP3QVT7R6C4W2JK47UJV4)
## 使用前配置
### 解决依赖
开始配置本系统前，应确保正确安装MariaDB和Python3，扬声器和麦克风工作正常，并连接至因特网。然后打开终端，运行如下的
命令安装所需的依赖：
```
cd VPA
pip install -r requirement.txt
```

### 数据库配置
参考以下步骤创建该系统使用的数据库，导入表结构和所需数据：

#### 创建数据库：
以下使用SQL语句创建一个名为XIAOMING的数据库：
```
CREATE DATABASE XIAOMING；
```
#### 导入各表结构和所需数据：
```
cd VPA/database
cat *.sql > database.sql
mysql -u root -p XIAOMING < database.sql
```
#### 修改系统连接至数据库的方式：
进入VPA/database目录，修改文件DBOperation.py，把其中包含的以下3行：
```
user = 'root'
password = 'password'
database = 'XIAOMING'
```

改为已创建数据库实际的用户名、密码和数据库名。比如用户名为user，密码为12345678，数据库名为XM，
修改完成后如下：
```
user = 'user'
password = '12345678'
database = 'XM'

```
### 配置百度语音API 
参考以下的SQL语句，把百度语音API的AppID、API Key、Secret Key（如何获取可参考<https://ai.baidu.com/tech/speech>）
插入到已创建数据库中的baiduSpeech表:
```
INSERT INTO baiduSpeech VALUE ('your AppID','your API Key','your Secret Key');

```
### 配置百度通用翻译API
把百度通用翻译API的AppID、Secret Key（参考<http://api.fanyi.baidu.com/api/trans/product/index>）插入到已创建数据库中的baiduTranslate表：
```
INSERT INTO baiduTranslate VALUE ('your AppID','your API Key');
```
### 配置和风天气API
把和风天气API的API Key（参考<https://www.heweather.com/>）插入到已创建数据库中的heWeather表：
```
INSERT INTO heWeather VALUE ('your API Key');
```
### 试运行
到此为止，系统应该能够正常运行，打开终端，进入主目录VPA，运行vpa.py应该可以启动该系统，若出现错误，请
检查以上安装配置的步骤。系统启动之后会弹出一个身份验证的对话框，第一次使用时可以新建一个用户，以后可以
继续使用这个用户账号。身份验证通过后可以使用该系统提供的各种功能，当主界面下方的标签变为绿色时可以按
Enter键开始讲话，向系统提出服务请求。

## 各功能说明
### 背诵古诗 
可以让系统随机播放一首诗，如“来首诗”；或让它播放某个诗人的一首诗，如“来首李白的诗”。
### 天气查询
可以查询你所在城市的天气，如“现在的天气怎么样”；或查询某一城市的天气，如“北京的天气怎么样”。
### 文本翻译
可以直接向系统提问某句用汉语表示的话用英语如何表达，如“‘你好’用英语怎么说”；或进行自由翻译，如
当系统识别到“自由翻译”等命令时，弹出一个包含两个文本框窗口，一个文本框可以输入源语言文本，另一个文本框
显示翻译完成的目标语言文本。支持的语言列表可参考<http://api.fanyi.baidu.com/api/trans/product/apidoc>。
### 百科知识
可以请求系统解释某一词条，如“解释人工智能”。
### 新闻查询
让系统播放最近几条新闻，只需像这样说“有什么新闻吗”或“播放新闻”等。
### 联系人管理
创建联系人可以说“创建联系人”，此时会弹出一个窗口以输入联系人信息；查看所有联系人可以说“查看联系人”；删除某个
联系人可以说“删除名为...的联系人”。
### 笔记
类似联系人管理功能，可以创建、查看和删除笔记，除此之外还运行导出笔记，只需说“导出笔记”，所有的笔记保存为一个txt
文件存放于VPA/notes目录下。
### 代发微信消息
可以向某一联系人发送微信消息，只需这样说“发微信告诉...说...”。
### 时钟功能
可以询问当前的时间，如“现在几点”；或开始倒计时，如“开始一分钟倒计时”。
