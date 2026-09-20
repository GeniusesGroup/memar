/* For license and copyright information please see the LEGAL file in the code repository */

package ft

import (
	er "libgo/error"
	"libgo/protocol"
)

const domainEnglish = "Sabz.City"
const domainPersian = "شهرسبز"

// Errors
var (
	ErrFinancialTransactionBadSociety = er.New("urn:giti:financial-transaction.protocol:error:bad-society").SetDetail(protocol.LanguageEnglish, domainEnglish, "Financial Transaction Bad Society",
		"Can't proccess request that from and to other different societies!",
		"",
		"").Save()

	ErrFinancialTransactionBadUser = er.New("urn:giti:financial-transaction.protocol:error:bad-user").SetDetail(protocol.LanguageEnglish, domainEnglish, "Financial Transaction Bad User",
		"Can't proccess request that from or to user ID is not same with active user!",
		"",
		"").Save()

	ErrFinancialTransactionBalance = er.New("urn:giti:financial-transaction.protocol:error:balance").SetDetail(protocol.LanguageEnglish, domainEnglish, "Financial Transaction Balance",
		"Financial transaction canceled due to user don't has enough balance",
		"",
		"").
		SetDetail(protocol.LanguagePersian, domainPersian, "مالی - عدم موجودی کافی",
			"درخواست انتقال مالی به دلیل عدم موجودی کاربر فعلی امکان پذیر نمی باشد",
			"",
			"").Save()
)
