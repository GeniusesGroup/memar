/* For license and copyright information please see the LEGAL file in the code repository */

package fap

import (
	"memar/protocol"

	fcp "org/modules/financial-currency/protocol"
	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AccountID() FinancialAccountUUID
	CurrencyID() fcp.FinancialCurrencyUUID
	UserID() up.UserUUID
	SettlementAccountID() FinancialAccountUUID
	SettlementReference() org.OrgUUID // Clearing and Settlement. MoneySettlementReference can be any org or society user.
	SettlementInterval() protocol.Duration

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
