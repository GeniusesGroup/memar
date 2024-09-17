/* For license and copyright information please see the LEGAL file in the code repository */

package osup

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fcp "org/modules/financial-currency/protocol"
	org "org/modules/org/protocol"
)

// DataModel is fixed salary that use in roles salary rules to calculate each staff salary.
type DataModel interface {
	OrgID() org.OrgUUID
	CurrencyID() fcp.FinancialCurrencyUUID
	Amount() protocol.MoneyAmount

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
