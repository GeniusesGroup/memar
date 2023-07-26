//go:build lang_eng

/* For license and copyright information please see the LEGAL file in the code repository */

package errors

import (
	"memar/detail"
	"memar/protocol"
)

const domainEnglish = "OTP"

func init() {
	ErrWrongNumber.SetDetail(protocol.LanguageEnglish, domainEnglish, "Wrong Number",
		"Given OTP number is wrong and can't prove due to expired or bad one!",
		"",
		"",
		nil)
}
