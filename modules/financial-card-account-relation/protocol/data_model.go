/* For license and copyright information please see the LEGAL file in the code repository */

package fcarp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	fcp "org/modules/financial-card/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CardID() fcp.FinancialCardUUID       //
	AccountID() fap.FinancialAccountUUID //
	Priority() uint64                    //
	Status() Status                      //
	SaveTime() protocol.Time             //
	RequestID() urp.UserRequestUUID      //
}

type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
