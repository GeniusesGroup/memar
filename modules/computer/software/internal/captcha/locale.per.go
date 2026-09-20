//go:build lang_per

/* For license and copyright information please see the LEGAL file in the code repository */

package captcha

import (
	"libgo/protocol"
)

const domainPersian = "کپچا"

func init() {
	ErrNotFound.SetDetail(protocol.LanguagePersian, domainPersian, "یافت نشد",
		"کپچای مورد نظر یافت نشد، یکی دیگر را امتحان کنید",
		"",
		"",
		nil)

	ErrExpired.SetDetail(protocol.LanguagePersian, domainPersian, "منقضی شده است",
		"کپچای مورد نظر منقضی شده است، یکی دیگر را امتحان کنید",
		"",
		"",
		nil)

	ErrAnswerNotValid.SetDetail(protocol.LanguagePersian, domainPersian, "جواب غیر صحیح",
		"جواب ارسالی برای کپچای مورد نظر صحیح نمی باشد، دوباره تلاش کنید",
		"",
		"",
		nil)

	ErrNotSolved.SetDetail(protocol.LanguagePersian, domainPersian, "حل نشده است",
		"قبل از ارسال درخواست با اشاره به این کپچا شما می بایستی کپچا را حل کنید",
		"",
		"",
		nil)
}
