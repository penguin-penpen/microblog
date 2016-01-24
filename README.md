app/:
    应用程序包
static/:
    静态文件如图片、JS文件、样式文件
templates/:
    模版文件

-在html中，动态内容在{{...}}中，{{%...%}}中为控制语句，用jinja2模板引擎解析。
-数据存放在views.py中，不是模板中。

-数据库迁移： 把应用程序数据库的任何改变看作一次迁移。
-脚本看起来很复杂，其实际上做的并不多。SQLAlchemy-migrate 迁移的方式就是比较数据库(在本例中从 app.db 中获取)与我们模型的结构(从文件 app/models.py 获取)。两者间的不同将会被记录成一个迁移脚本存放在迁移仓库中。迁移脚本知道如何去迁移或撤销它，所以它始终是可能用于升级或降级一个数据库。

然而在使用上面的脚本自动地完成迁移的时候也不是没有问题的，我见过有时候它很难识别新老格式的变化。为了让 SQLAlchemy-migrate 容易地识别出变化，我绝不会重命名存在的字段，我仅限于增加或者删除模型或者字段，或者改变已存在字段的类型。当然我一直会检查生成的迁移脚本，确保它是正确。

*在新增一个功能时，先考虑需要的扩展。