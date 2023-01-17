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
    KIND_OF_CASE = [
        ('黒の組織','黒の組織'),
        ('恋愛','恋愛'),
        ('警察関係','警察関係'),
        ('KID','KID'),
        ('FBI', 'FBI'),
        ('赤井家', '赤井家')
    ]

    number = models.IntegerField(primary_key=True)
    complement = models.TextField(blank=True, null=True)
    kind = models.CharField(max_length=30, blank=True, null=True, choices=KIND_OF_CASE)

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
    content = models.TextField(null=True)

    ### 他のテーブルとの関連
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, default=1)

    ### object 自体の表示方法を指定
    def __str__(self):
        return f'{self.content[0:15]} ...'


class Character(models.Model):
    AFFILIATION = [
        ('帝丹小学校', '帝丹小学校'), # 左が表示、右が選択肢
        ('帝丹高校', '帝丹高校'),
        ('東都大学', '東都大学'),
        ('黒の組織', '黒の組織'),
        ('毛利家', '毛利家'),
        ('警察', '警察'),
        ('FBI', 'FBI'),
        ('SIS', 'SIS'),
        ('NOC', 'NOC'),
        ('赤井家', '赤井家')
    ]

    PROFESSION = [
        ('小学生','小学生'),
        ('高校生','高校生'),
        ('警察官','警察官'),
        ('探偵','探偵'),
        ('FBI捜査官', 'FBI捜査官'),
    ]
    name = models.CharField(max_length=30)
    belong_to = models.CharField(max_length=30, choices=AFFILIATION)
    profession = models.CharField(max_length=30, null=True, choices=PROFESSION)
    skill = models.CharField(blank=True, null=True, max_length=200)
    complement = models.TextField(blank=True, null=True)
    # 付与する情報の例。
    # 登場の仕方（実際に登場するのではなく、会話中で名前が出てくる。思考や回想シーンの中で登場する。）
    # 同一人物の紹介。
    # 等々。
    
    ### 他のテーブルとの関連
    chapter = models.ManyToManyField(Chapter)
    event_related_to = models.ManyToManyField(Event, blank=True)

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
    
    