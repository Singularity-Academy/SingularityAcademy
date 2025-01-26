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
	htmlBody := fmt.Sprintf("<a href=\"http://localhost:1298/auth/verify?token=%s\">click to verify your email</a>", token)
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
