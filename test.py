from orange.mail import *
from orange import *

with MailClient(host='smtp.163.com',
                      user='hunto@163.com',
                      passwd='gnmomhlggcovzdph') as client:
    mail=client.Mail(sender='hunto@163.com',
           to='huangtao@czbank.com',
           subject='郑州分行测试情况总结',
           body='<h2>你好！</h2>'\
'<p>这是一个不错的文件</p>')
    mail.add_file('d:\\他们.xlsx')
    mail.post()
    print('发送邮件成功')

