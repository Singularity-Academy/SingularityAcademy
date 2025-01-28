package config

import (
	"crypto/tls"
	"fmt"
	"net"
	"net/smtp"

	"github.com/spf13/viper"
)

var SmtpAuth smtp.Auth

// 初始化 SMTP 认证
func ConnectSMTP() {
	SmtpAuth = smtp.PlainAuth(
		"",
		viper.GetString("email.email"),
		viper.GetString("email.password"),
		viper.GetString("email.host"),
	)
}

// 发送验证邮件
func SendVerifyEmail(to string, token string) {
	// 构造邮件头
	header := make(map[string]string)
	header["From"] = viper.GetString("email.email")
	header["To"] = to
	header["Subject"] = "Email Verification"
	header["Content-Type"] = "text/html; charset=UTF-8"

	// 构造邮件内容
	message := ""
	for k, v := range header {
		message += fmt.Sprintf("%s: %s\r\n", k, v)
	}
	htmlBody := fmt.Sprintf("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Welcome to Krypoto School!</title>\n  <style>\n    /* Basic Reset */\n    * {\n      margin: 0;\n      padding: 0;\n      box-sizing: border-box;\n    }\n    body {\n      background-color: #f4f4f4;\n      font-family: 'Arial, sans-serif';\n      padding: 20px;\n    }\n    .email-container {\n      max-width: 600px;\n      margin: 0 auto;\n      background-color: #ffffff;\n      border-radius: 8px;\n      overflow: hidden;\n      box-shadow: 0 4px 6px rgba(0,0,0,0.1);\n    }\n    .header {\n      background-image: url('https://your-image-url.com/header-background.jpg'); /* Replace with your header background image URL */\n      background-size: cover;\n      background-position: center;\n      padding: 40px 20px;\n      text-align: center;\n      color: #ffffff;\n    }\n    .header img {\n      width: 100px;\n      height: auto;\n      margin-bottom: 20px;\n    }\n    .header h1 {\n      font-size: 2.5em;\n      margin-bottom: 10px;\n    }\n    .content {\n      padding: 30px 20px;\n      text-align: center;\n      color: #333333;\n    }\n    .content h2 {\n      font-size: 1.8em;\n      margin-bottom: 15px;\n    }\n    .content p {\n      font-size: 1em;\n      line-height: 1.6;\n      margin-bottom: 25px;\n    }\n    .button-container {\n      text-align: center;\n      margin-bottom: 30px;\n    }\n    .verify-button {\n      background-color: #28a745;\n      color: #ffffff;\n      padding: 15px 25px;\n      text-decoration: none;\n      font-size: 1em;\n      border-radius: 5px;\n      transition: background-color 0.3s ease;\n    }\n    .verify-button:hover {\n      background-color: #218838;\n    }\n    .footer {\n      background-color: #f4f4f4;\n      padding: 20px;\n      text-align: center;\n      font-size: 0.9em;\n      color: #777777;\n    }\n    .footer p {\n      margin-bottom: 10px;\n    }\n    .social-icons a {\n      margin: 0 10px;\n      display: inline-block;\n    }\n    .social-icons img {\n      width: 24px;\n      height: 24px;\n    }\n    /* Responsive Design */\n    @media (max-width: 600px) {\n      .header h1 {\n        font-size: 2em;\n      }\n      .content h2 {\n        font-size: 1.5em;\n      }\n      .verify-button {\n        padding: 12px 20px;\n        font-size: 0.9em;\n      }\n    }\n  </style>\n</head>\n<body>\n  <div class=\"email-container\">\n    <!-- Header Section -->\n    <div class=\"header\">\n      <img src=\"https://your-image-url.com/logo.png\" alt=\"Krypoto School Logo\"> <!-- Replace with your logo URL -->\n      <h1>Welcome to Krypoto School!</h1>\n    </div>\n    \n    <!-- Content Section -->\n    <div class=\"content\">\n      <h2>Thank You for Joining Us!</h2>\n      <p>We're thrilled to have you on board. To get started, please verify your email address by clicking the button below. This helps us ensure the security of your account and provide you with the best learning experience.</p>\n      \n      <!-- Verification Button -->\n      <div class=\"button-container\">\n        <a href=\"http://localhost:1298/auth/verify?token=%s\" class=\"verify-button\">Verify Your Email</a>\n      </div>\n      \n      <p>If you did not sign up for Krypoto School, please ignore this email or contact our support team.</p>\n    </div>\n    \n    <!-- Footer Section -->\n    <div class=\"footer\">\n      <p>&copy; 2025 Krypoto School. All rights reserved.</p>\n      <div class=\"social-icons\">\n        <a href=\"https://facebook.com/krypotoschool\" target=\"_blank\">\n          <img src=\"https://your-image-url.com/facebook-icon.png\" alt=\"Facebook\">\n        </a>\n        <a href=\"https://twitter.com/krypotoschool\" target=\"_blank\">\n          <img src=\"https://your-image-url.com/twitter-icon.png\" alt=\"Twitter\">\n        </a>\n        <a href=\"https://instagram.com/krypotoschool\" target=\"_blank\">\n          <img src=\"https://your-image-url.com/instagram-icon.png\" alt=\"Instagram\">\n        </a>\n      </div>\n    </div>\n  </div>\n</body>\n</html>", token)

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
