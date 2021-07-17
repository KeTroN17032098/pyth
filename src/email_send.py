import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 세션생성, 로그인
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('위의 세팅된 gmail계정', '위의 16글자 비밀번호')

# 제목, 본문 작성
msg = MIMEMultipart()
msg['Subject'] = '제목'
msg.attach(MIMEText('본문', 'plain'))

# 파일첨부 (파일 미첨부시 생략가능)
attachment = open('파일명', 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= " + filename)
msg.attach(part)

# 메일 전송
s.sendmail("보내는 메일계정", "받는 메일계정", msg.as_string())
s.quit()