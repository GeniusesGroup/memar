/* For license and copyright information please see the LEGAL file in the code repository */

package bank

import (
	"../price"
	"../protocol"
)

var BankAccountMediaType = mediatype.New("domain/bank-account.protocol+syllab").
	SetInfo(protocol.Software_PreAlpha, 1599291620, "").
	SetDetail(protocol.LanguageEnglish, "Bank Account",
		`store users bank account to distinguish user balances in desire indexes`,
		[]string{}).
	Expired(0, nil)
	
// Account ---Read locale description in AccountStructure---
type Account struct {
	RequestID   [16]byte // user-request domain
	UserID      [16]byte `index-hash:"ObjectID"`
	IBAN        [34]byte `index-hash:"ObjectID"` // International Bank Account Number
	CardNumber  [16]byte `index-hash:"ObjectID"` // fixed size card number without any dash e.g. 1234-1234-1234-1234
	Currency    price.Currency
	CardHexSHA1 [40]byte `index-hash:"UserID"` // fixed size string
	Status      protocol.FinancialAccountStatus
}

type account []byte
