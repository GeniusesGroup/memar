//go:build lang_eng

/* For license and copyright information please see the LEGAL file in the code repository */

package captcha

import (
	"libgo/protocol"
)

const domainEnglish = "Captcha"

func init() {
	ErrNotFound.SetDetail(protocol.LanguageEnglish, domainEnglish, "Not Found",
		"Captcha not exist, Try new one",
		"",
		"",
		nil)

	ErrExpired.SetDetail(protocol.LanguageEnglish, domainEnglish, "Expired",
		"Captcha Expired, Try new one",
		"",
		"",
		nil)

	ErrAnswerNotValid.SetDetail(protocol.LanguageEnglish, domainEnglish, "Answer Not Valid",
		"Given answer for captcha not valid, Try again",
		"",
		"",
		nil)

	ErrNotSolved.SetDetail(protocol.LanguageEnglish, domainEnglish, "Not Solved",
		"Captcha not solved yet, Solve it before use it to prove human being",
		"",
		"",
		nil)
}
