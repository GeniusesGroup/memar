//go:build lang_eng

/* For license and copyright information please see the LEGAL file in the code repository */

package errs

import (
	"memar/protocol"
)

const domainEnglish = "Price"

func init() {
	ErrBadCurrency.SetDetail(protocol.LanguageEnglish, domainEnglish, "Bad Currency",
		"Not supported or bad currency selected!",
		"",
		"",
		nil)
	ErrInvalidTerminalID.SetDetail(protocol.LanguageEnglish, domainEnglish, "Invalid TerminalID",
		"Provided TerminalID not valid",
		"",
		"",
		nil)
	ErrNotEnoughBalance.SetDetail(protocol.LanguageEnglish, domainEnglish, "Not Enough Balance",
		"Transaction canceled due to user don't has enough balance",
		"",
		"",
		nil)
}
