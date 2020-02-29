from django.db import models


# Create your models here.
class Mission(models.Model):
    missionname = models.CharField("任务名称", max_length=100, null=False)
    missiontype = models.CharField("任务类别", max_length=1)
    missionstate = models.CharField("任务状态", max_length=4)
    usercompany = models.CharField("需求提交公司", max_length=50)
    username = models.CharField("需求提交用户", max_length=50)
    usertel = models.CharField("用户电话", max_length=20)
    receivetime = models.DateField("接收需求时间", auto_now_add=True)
    missionlevel = models.CharField("需求等级", max_length=1)
    remark = models.CharField("备注", max_length=1000, null=True)
    usertestdate = models.DateField("用户测试日期", null=True)
    phdate = models.DateField("上线归档日期", null=True)

    def __str__(self):
        return "任务名称：%s 任务类别：%s 任务状态：%s 需求提交公司：%s 需求提交用户：%s 用户电话：%s" \
               " 接收需求时间：%s 需求等级：%s 备注：%s 用户测试日期：%s 上线归档日期：%s" % (
                   self.missionname, self.missiontype, self.missionstate,
                   self.usercompany, self.username, self.usertel,
                   self.receivetime, self.missionlevel,
                   self.remark, self.usertestdate, self.phdate)

    class Meta:
        db_table = 'mission'


class Log(models.Model):
    missionid = models.ForeignKey(Mission)
    # 0000删除 0100录入，0200需求分析已分配，0300需求分析已完成，0400开发任务已分配
    # 0500开发完成，0600测试完成，0700用户测试完成，0800需求已上线
    missionstate = models.CharField('任务状态', max_length=4)
    logerid = models.IntegerField('操作人')
    logdate = models.DateTimeField('日志记录时间', auto_now_add=True)

    class Meta:
        db_table = 'log'


class File(models.Model):
    missionid = models.ForeignKey(Mission)
    file = models.FileField(upload_to='files')
    filename = models.CharField('文件名称', max_length=100)
    uploader = models.IntegerField('上传人')
    uploaddate = models.DateField('上传时间', auto_now_add=True)

    class Meta:
        db_table = 'file'


class Code(models.Model):
    codetype = models.CharField('类型', max_length=10)
    value = models.CharField('码值', max_length=10)
    words = models.CharField('文字', max_length=50)

    class Meta:
            db_table = 'code'
