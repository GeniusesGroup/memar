//go:build lang_per

/* For license and copyright information please see the LEGAL file in the code repository */

package lang

import (
	"memar/detail"
	"memar/protocol"
)

const domainPersian = "زبان"

func init() {
	ErrBadLanguage.SetDetail(detail.New(lang_p.LanguagePersian, domainPersian).
		SetName("").
		SetAbbreviation("").
		SetAliases([]string{}).
		SetSummary("زبان بد").
		SetOverview("زبان انتخاب شده صحیح نمی باشد یا توسط نرم افزار پشتیبانی نمی شود").
		SetUserNote("").
		SetDevNote("").
		SetTAGS([]string{})
	)
}
