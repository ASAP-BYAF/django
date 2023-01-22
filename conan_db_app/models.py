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

class CaseKind(models.Model):
    name = models.CharField(max_length=30)

    ### object 自体の表示方法を指定
    def __str__(self):
        return self.name

class Case(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    complement = models.TextField(blank=True, null=True)

    ### 他のテーブルとの関連
    kind = models.ManyToManyField(CaseKind, blank=True)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'Case.{self.number} : {self.name}'

    ### 並び順を指定
    class Meta:
        ordering = ('number',)

class Chapter(models.Model):
    name = models.CharField(max_length=30)
    number_in_volume = models.IntegerField()
    number_in_all = models.IntegerField()
    complement = models.TextField(blank=True, null=True)

    ### 他のテーブルとの関連
    volume = models.ForeignKey(Volume, on_delete=models.PROTECT, default=1)
    case = models.ForeignKey(Case, on_delete=models.PROTECT, default=1)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'Volume.{self.volume.number} - File.{self.number_in_volume} : {self.name}'

    ### 並び順を指定
    class Meta:
        ordering = ('number_in_all',)

class Event(models.Model):
    content = models.TextField(null=True)

    ### 他のテーブルとの関連
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, default=1)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'{self.content[0:15]} ...'

class Affiliation(models.Model):
    name = models.CharField(max_length=30)

    ### object 自体の表示方法を指定
    def __str__(self):
        return self.name

class Profession(models.Model):
    name = models.CharField(max_length=30)

    ### 他のテーブルとの関連
    affiliation = models.ForeignKey(Affiliation, on_delete=models.PROTECT, blank=True, null=True)

    ### object 自体の表示方法を指定
    def __str__(self):
        if self.affiliation:
            return f'{self.affiliation.name} -- {self.name}'
        else:
            return f'None -- {self.name}'


class Character(models.Model):
    name = models.CharField(max_length=30)
    skill = models.CharField(blank=True, null=True, max_length=200)
    complement = models.TextField(blank=True, null=True)
    # 付与する情報の例。
    # 登場の仕方（実際に登場するのではなく、会話中で名前が出てくる。思考や回想シーンの中で登場する。）
    # 同一人物の紹介。
    # 等々。
    
    ### 他のテーブルとの関連
    chapter = models.ManyToManyField(Chapter)
    event_related_to = models.ManyToManyField(Event, blank=True)
    belong_to = models.ManyToManyField(Affiliation)
    profession = models.ManyToManyField(Profession, blank=True)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'<ID = {self.id}> {self.name}'

    ### 並び順を指定
    class Meta:
        ordering = ('id',)

class Question(models.Model):
    KIND_OF_QUESTION=[
        ( 'question', '問題'),
        ( 'questionnaire', 'アンケート'),
    ]

    JENRE_OF_QUESTION=[
        ( 'conan', '名探偵コナン関係'),
        ( 'others', 'それ以外'),
    ]

    NUMBER_OF_ANSWER_OPTION=[
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
    ]
    
    kind = models.CharField(max_length=20, blank=False, null=False, choices=KIND_OF_QUESTION, default='question')
    jenre = models.CharField(max_length=20, blank=False, null=False, choices=JENRE_OF_QUESTION, default='conan') 
    content = models.TextField(blank=False, null=False)
    n_option = models.IntegerField(blank=False, null=False, choices=NUMBER_OF_ANSWER_OPTION)
    option1 = models.TextField(blank=False, null=False) 
    option2 = models.TextField(blank=False, null=False)
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)
    option5 = models.TextField(blank=True, null=True)
    
    