> 前排吐槽:  软件抓包属实恶心，登陆的时候magisk被检测的话直接强制退出，代理网络环境也会强制退出

工具：
curl2python : https://curlconverter.com/python/


## "我去图书馆"首页地址获取办法

某大校园首页关闭网络点击“我去图书馆”，得到“网页无法打开”，后面链接即为首页地址，**每次退出重新登陆后此地址会改变**

![](https://s3.bmp.ovh/imgs/2022/10/25/8f0d87a2e9282909.png)

## server酱SendKey



link: https://sct.ftqq.com/sendkey



## 期望图书馆房间和期望位置列表



运行getHomeAndSeat.py函数配置loginUrl即可获得



![](https://s3.bmp.ovh/imgs/2022/10/25/777c46c21bdc3211.png)

eg:

```
libId=10550
seatKeyList=["11,18", '52,13', '52,14', '52,15', '52,13']
```



## 腾讯云函数定时触发

link: https://serverless.cloud.tencent.com/start?c=scf

> 具体配置不作赘述
>
> ```
> cron表达式 ：0 30 7 * * * *
> ```
>
> 表示 每一天7：30触发



## 效果：

<img src="https://s3.bmp.ovh/imgs/2022/10/25/59248c527eb593bc.png" style="zoom: 25%;" />

<img src="https://s3.bmp.ovh/imgs/2022/10/25/bbb100949e6aa4a3.png" style="zoom:25%;" />