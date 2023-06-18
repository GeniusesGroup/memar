/* For license and copyright information please see the LEGAL file in the code repository */

package brip

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	ip "org/modules/invoice/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID        //
	InvoiceID() ip.InvoiceUUID      //
	Type() Type                     //
	Status() BudgetInvoice_Status   //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type BudgetInvoice_Status qsp.Quiddity_Status

type Type uint8

const (
	Type_Unset Type = iota
	Type_Supporter
	Type_Sponsor
)
