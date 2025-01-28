package config

import (
	"crypto/tls"
	"fmt"
	"net"
	"net/smtp"

	"github.com/spf13/viper"
)

var SmtpAuth smtp.Auth

// ConnectSMTP 初始化 SMTP 认证
func ConnectSMTP() {
	SmtpAuth = smtp.PlainAuth(
		"",
		viper.GetString("email.email"),
		viper.GetString("email.password"),
		viper.GetString("email.host"),
	)
}

// SendVerifyEmail 发送验证邮件
func SendVerifyEmail(to string, token string) {
	// 构造邮件头
	header := make(map[string]string)
	header["From"] = fmt.Sprintf("AI Online School<%s>", viper.GetString("email.email"))
	header["To"] = to
	header["Subject"] = "Email Verification"
	header["Content-Type"] = "text/html; charset=UTF-8"

	// 构造邮件内容
	message := ""
	for k, v := range header {
		message += fmt.Sprintf("%s: %s\r\n", k, v)
	}
	htmlBody := fmt.Sprintf(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Welcome to AI Online School!</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      background-color: #F7FAFC;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
      padding: 20px;
      color: #2D3748;
    }
    .email-container {
      max-width: 600px;
      margin: 0 auto;
      background-color: #FFFFFF;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header {
      background: linear-gradient(to right, #4299E1, #805AD5);
      padding: 40px 20px;
      text-align: center;
      color: #FFFFFF;
    }
    .header img {
      width: 120px;
      height: auto;
      margin-bottom: 24px;
    }
    .header h1 {
      font-size: 2.5em;
      margin-bottom: 16px;
      font-weight: 700;
    }
    .content {
      padding: 40px 24px;
      text-align: center;
    }
    .content h2 {
      font-size: 1.8em;
      margin-bottom: 20px;
      color: #2B6CB0;
    }
    .content p {
      font-size: 1.1em;
      line-height: 1.6;
      margin-bottom: 28px;
      color: #4A5568;
    }
    .button-container {
      text-align: center;
      margin: 32px 0;
    }
    .verify-button {
      background-color: #4299E1;
      color: #FFFFFF;
      padding: 16px 32px;
      text-decoration: none;
      font-size: 1.1em;
      border-radius: 8px;
      font-weight: 600;
      display: inline-block;
      transition: background-color 0.3s ease;
    }
    .verify-button:hover {
      background-color: #3182CE;
    }
    .founders-section {
      background-color: #F7FAFC;
      padding: 24px;
      margin-top: 32px;
      border-radius: 8px;
    }
    .founders-section h3 {
      color: #2B6CB0;
      margin-bottom: 16px;
      font-size: 1.4em;
    }
    .founder {
      margin-bottom: 12px;
      font-size: 1em;
      color: #4A5568;
    }
    .footer {
      background-color: #F7FAFC;
      padding: 24px;
      text-align: center;
      font-size: 0.9em;
      color: #718096;
    }
    @media (max-width: 600px) {
      .header h1 {
        font-size: 2em;
      }
      .content h2 {
        font-size: 1.5em;
      }
      .verify-button {
        padding: 14px 28px;
        font-size: 1em;
      }
    }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <img src="https://your-logo-url.com/logo.png" alt="AI Online School Logo">
      <h1>Welcome to AI Online School!</h1>
    </div>
    
    <div class="content">
      <h2>Thank You for Joining Us!</h2>
      <p>We're excited to have you join our innovative AI-powered learning platform. To begin your personalized learning journey, please verify your email address by clicking the button below.</p>
      
      <div class="button-container">
        <a href="http://localhost:1298/auth/verify?token=%s" class="verify-button">Verify Your Email</a>
      </div>
      
      <p>If you did not sign up for AI Online School, please ignore this email or contact our support team.</p>

      <div class="founders-section">
        <h3>Meet Our Founders</h3>
        <div class="founder">Jiace Zhao - CEO & AI Research Lead</div>
        <div class="founder">Di Huang - CTO & Backend Platform Architecture</div>
      </div>
    </div>
    
    <div class="footer">
      <p>&copy; 2024 AI Online School. All rights reserved.</p>
      <p>This is an automated message, please do not reply to this email.</p>
    </div>
  </div>
</body>
</html>`, token)

	message += "\r\n" + htmlBody

	// 使用 TLS 发送邮件
	err := sendMailTLS(
		viper.GetString("email.host")+":"+viper.GetString("email.port"),
		SmtpAuth,
		viper.GetString("email.email"),
		[]string{to},
		[]byte(message),
	)
	if err != nil {
		fmt.Println("verify email to "+to+" was sent failed:", err)
	} else {
		fmt.Println("verify email to " + to + " was sent successfully!")
	}
}

// 使用 TLS 发送邮件
func sendMailTLS(addr string, auth smtp.Auth, from string, to []string, msg []byte) error {
	// 分解地址和端口
	host, _, err := net.SplitHostPort(addr)
	if err != nil {
		return fmt.Errorf("invalid email: %v", err)
	}

	// 建立 TLS 连接
	conn, err := tls.Dial("tcp", addr, &tls.Config{
		InsecureSkipVerify: true, // 可以根据需要设置为 false，强制验证证书
		ServerName:         host,
	})
	if err != nil {
		return fmt.Errorf("failed to connect TLS: %v", err)
	}

	client, err := smtp.NewClient(conn, host)
	if err != nil {
		return fmt.Errorf("failed to create SMTP client: %v", err)
	}
	defer func(client *smtp.Client) {
		err := client.Quit()
		if err != nil {
			fmt.Printf("failed to close SMTP client: %v", err)
		}
	}(client)

	// 验证身份
	if err = client.Auth(auth); err != nil {
		return fmt.Errorf("failed to verify SMTP: %v", err)
	}

	// 设置发件人和收件人
	if err = client.Mail(from); err != nil {
		return fmt.Errorf("failed to set sender: %v", err)
	}
	for _, addr := range to {
		if err = client.Rcpt(addr); err != nil {
			return fmt.Errorf("failed to set recipient: %v", err)
		}
	}

	// 发送邮件数据
	writer, err := client.Data()
	if err != nil {
		return fmt.Errorf("failed send data: %v", err)
	}
	_, err = writer.Write(msg)
	if err != nil {
		return fmt.Errorf("failed to write content of email: %v", err)
	}
	err = writer.Close()
	if err != nil {
		return fmt.Errorf("failed to close write: %v", err)
	}

	return nil
}
