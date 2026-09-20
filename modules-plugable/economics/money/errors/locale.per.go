//go:build lang_per

/* For license and copyright information please see the LEGAL file in the code repository */

package errs

import (
	"memar/protocol"
)

const domainPersian = "ارزش"

func init() {
	ErrBadCurrency.SetDetail(protocol.LanguagePersian, domainPersian, "ارز بد",
		"ارز انتخاب شده صحیح نمی باشد یا توسط نرم افزار پشتیبانی نمی شود",
		"",
		"",
		nil)
	ErrInvalidTerminalID.SetDetail(protocol.LanguagePersian, domainPersian, "شماره پایانه اشتباه",
		"شماره پایانه مورد نظر صحیح نمی باشد",
		"",
		"",
		nil)
	ErrNotEnoughBalance.SetDetail(protocol.LanguagePersian, domainPersian, "عدم موجودی کافی",
		"موجودی کیف پول کاربر برای انجام درخواست مورد نظر کافی نیست",
		"",
		"",
		nil)
}
