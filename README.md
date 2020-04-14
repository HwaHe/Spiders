# Spiders
一些突然兴起写的爬虫，这里会对各爬虫需要注意的地方进行说明 <br>
* douban_top250.py
---
用requests库和re爬取豆瓣top250的电影榜单并写入文件  
  1. 带上`headers`，否则`response`的`status_code`为418(I'm a teapot)
  2. 每页电影的html中有些标签的class属性为空，抓取到的html和chrome中看到的element不一致。
  3. 最后一页的电影中有些电影没有quote部分，需要单独处理（abstract_str)
  4. 并行写进文件时要加资源锁，否则会出现乱码



