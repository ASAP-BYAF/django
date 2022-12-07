from django.db import models

# Create your models here.

class Volume(models.Model):
    number = models.IntegerField(primary_key=True)
    complement = models.TextField(blank=True, null=True)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'Volume.{self.number}'

    ### 並び順を指定
    class Meta:
        ordering = ('number',)

class Case(models.Model):
    number = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100) # 事件内容：自殺、他殺、誘拐、暗号解読、など
    cause_of_death = models.CharField(max_length=100, blank=True, null=True)
    number_of_victim = models.IntegerField(blank=True, null=True)
    number_of_perpetrator = models.IntegerField(blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)
    motivation = models.CharField(max_length=100, blank=True, null=True)
    complement = models.TextField(blank=True, null=True)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'Case.{self.number}'

    ### 並び順を指定
    class Meta:
        ordering = ('number',)

class Chapter(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField()
    complement = models.TextField(blank=True, null=True)

    ### 他のテーブルとの関連
    volume = models.ForeignKey(Volume, on_delete=models.PROTECT, default=1)
    case = models.ForeignKey(Case, on_delete=models.PROTECT, default=1)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'Volume.{self.volume.number} - File.{self.number} : {self.name}'

    ### 並び順を指定
    class Meta:
        ordering = ('number',)

class Event(models.Model):
    content = models.TextField(blank=True, null=True)

    ### 他のテーブルとの関連
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, default=1)

class Character(models.Model):
    MALE = '男'
    FEMALE = '女'
    UNKNOWN = '不明'
    JENDER_LIST=[
        (MALE, '男'),
        (FEMALE, '女'),
        (UNKNOWN, '不明'),
    ]
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=2,
                              choices=JENDER_LIST)
    age = models.IntegerField(blank=True, null=True) # 約何歳や何歳以上したい場合は、 complement に記載。
    birthday = models.DateField(blank=True, null=True)
    profession = models.CharField(max_length=50)
    complement = models.TextField(blank=True, null=True)
    # 付与する情報の例。
    # 登場の仕方（実際に登場するのではなく、会話中で名前が出てくる。思考や回想シーンの中で登場する。）
    # 同一人物の紹介。
    # 等々。
    
    ### 他のテーブルとの関連
    chapter = models.ManyToManyField(Chapter)
    case_solved_by = models.ManyToManyField(Case)
    event_related_to = models.ManyToManyField(Event)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'<ID = {self.id}> {self.name}'

    ### 並び順を指定
    class Meta:
        ordering = ('id',)
