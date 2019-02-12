# 项目：标准程序库
# 模块：发送电子邮件
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-10-26 10:25

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.charset import Charset
from orange.utils.debug import ensure
from orange.shell import Path
from orange import deprecate
import smtplib
import io


def encode(filename):
    return Charset('utf8').header_encode(filename) \
        if any(map(lambda x: ord(x) > 127, filename)) else filename


def sendmail(*messages):
    '''发送邮件'''
    with MailClient() as client:
        for message in messages:
            message.post(client)


def tsendmail(*args):
    '''采用线程发送邮件'''
    from threading import Thread
    Thread(target=sendmail, args=args).start()


def mail_config(**conf):
    MailClient.config = conf.copy()


class MailClient(smtplib.SMTP):
    '''构造邮件客户端，使用方法如下：
       client=MailClient(host,user,passwd)
    '''
    config = {}   # 用于配置发送邮件的想着参数，如：host,user,passwd

    def __init__(self, host=None, user=None, passwd=None, *args, **kw):
        host = host or self.config.get('host')
        user = user or self.config.get('user')
        passwd = passwd or self.config.get('passwd')
        super().__init__(host, *args, **kw)
        self.login(user, passwd)

    def Mail(self, *args, **kw):
        m = Mail(*args, client=self, **kw)
        if m.sender is None:
            m.sender = self.config.get('sender')
        return m


class Mail:
    '''创建电子邮件，使用方法如下：
    mail=Mail(sender,to,subject,body,cc,bcc)
    添加图片：
    mail.add_image(filename,cid)
    添加文件附件：
    mail.add_file(filename)
    通过流附加文件：
    mail.add_fp(fp,filename)
    发送邮件：
    mail.post(client)
    '''

    def __init__(self, sender=None, to=None, subject=None, body=None,
                 cc=None, bcc=None, client=None):
        '''初始化邮件'''
        self.attachments = []
        self.subject = subject
        self.to = to
        self.sender = sender
        self.body = body
        self.cc = cc
        self.bcc = bcc
        self.client = client

    @property
    def message(self):
        '''获取邮件的MESSAGE属性'''
        body = self.body
        subtype = 'html' if body.startswith(
            '<')and body.endswith('>') else 'plain'
        body = MIMEText(body, subtype, 'utf-8')
        if self.attachments:
            msg = MIMEMultipart()
            msg.attach(body)
            for attachment in self.attachments:
                msg.attach(attachment)
        else:
            msg = body
        msg['Subject'] = self.subject
        msg['To'] = self.to
        msg['Sender'] = self.sender
        if self.cc:
            msg['Cc'] = self.cc
        if self.bcc:
            msg['Bcc'] = self.bcc
        return msg

    def __str__(self):
        return self.message.as_string()

    def add_fp(self, fp, filename):
        if callable(fp):
            with io.BytesIO() as _fp:
                fp(_fp)
                _fp.seek(0)
                msg = MIMEApplication(_fp.read())
                msg.add_header('content-disposition', 'attachment',
                               filename=encode(filename))
                self.attachments.append(msg)

    def attach(self, filename):
        file = Path(filename)
        msg = MIMEApplication(file.read_bytes())
        msg.add_header('content-disposition', 'attachment',
                       filename=encode(file.name))
        self.attachments.append(msg)

    add_file = attach

    def add_image(self, filename, cid=None):
        msg = MIMEImage(Path(filename).read_bytes())
        if cid:
            msg.add_header('Content-ID', f'<{cid}>')
            msg.add_header('X-Attachment-Id', cid)
            msg.add_header('content-disposition', 'inline',
                           filename=encode(Path(filename).name))
        self.attachments.append(msg)

    def post(self, mailclient=None):
        mailclient = mailclient or self.client
        if mailclient:
            mailclient.send_message(self.message)


if __name__ == '__main__':
    body = '''<html>
    <body>你在快乐的跳吗？<br/>
    年轻的心，因此而动.
    <img src="cid:fengche"/>
    </body></html>'''

    mail_config(host='smtp.163.com', user='hunto@163.com',
                passwd='Huangtao1978')
    with MailClient() as client:
        s = client.Mail(sender='黄涛 <hunto@163.com>',
                        to='张三 <huang.t@live.cn> , 李四 <huangtao.sh@icloud.com> , 李起 <hunto@163.com>',
                        subject='春天来了，你在这里等着我回来',
                        body=body)
        s.attach('~/假期参数表20180101.xlsx')
        s.add_image('~/风车.png', cid='fengche')
        s.post()
