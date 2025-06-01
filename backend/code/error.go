package code

/**
状态码规范：
错误为五位数状态码，成功：0

101xx用于用户鉴权相关错误
*/

type Error struct {
	Code    int
	Message string
}

type CustomErrors struct {
	InternalError Error
	NotFound      Error
	BadRequest    Error

	// 登录
	IncorrectEmailOrPassword Error
	FailedToGenerateToken    Error

	// 中间件
	AuthorizationHeaderIsRequired Error
	TokenIsRequired               Error
	InvalidToken                  Error

	// 注册
	InvalidEmailAddress               Error
	FailedToCheckEmail                Error
	EmailAlreadyRegistered            Error
	FailedToEncryptPassword           Error
	FailedToGenerateVerificationToken Error
}

var Errors = CustomErrors{

	InternalError: Error{Code: 10001, Message: ""},
	NotFound:      Error{Code: 10002, Message: ""},
	BadRequest:    Error{Code: 10003, Message: ""},

	IncorrectEmailOrPassword: Error{Code: 10101, Message: "api.courses.incorrectEmailOrPassword"},
	FailedToGenerateToken:    Error{Code: 10102, Message: "api.courses.failedToGenerateToken"},

	AuthorizationHeaderIsRequired: Error{Code: 10103, Message: "api.auth.authorizationHeaderIsRequired"},
	TokenIsRequired:               Error{Code: 10104, Message: "api.auth.tokenIsRequired"},
	InvalidToken:                  Error{Code: 10105, Message: "api.auth.invalidToken"},

	InvalidEmailAddress:               Error{Code: 10106, Message: "api.auth.invalidEmailAddress"},
	FailedToCheckEmail:                Error{Code: 10107, Message: "api.auth.failedToCheckEmail"},
	EmailAlreadyRegistered:            Error{Code: 10108, Message: "api.auth.emailAlreadyRegistered"},
	FailedToEncryptPassword:           Error{Code: 10109, Message: "api.auth.failedToEncryptPassword"},
	FailedToGenerateVerificationToken: Error{Code: 10110, Message: "api.auth.failedToGenerateVerificationToken"},
}
