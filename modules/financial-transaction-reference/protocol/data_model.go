/* For license and copyright information please see the LEGAL file in the code repository */

package ftrp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
)

// DataModel indicate the domain record data fields.
// Use version to save multi transactions for the same reference.
// It can't be changed after registered for any reason. Referencing must be automatic process.
type DataModel interface {
	ReferenceID() protocol.UUID                      // any domain(Budget, Contract, Invoice, Order) base on FinancialTransaction_Type
	SenderAccountID() fap.FinancialAccountUUID       //
	SenderAccountOffset() protocol.NumberOfVersion   //
	ReceiverAccountID() fap.FinancialAccountUUID     //
	ReceiverAccountOffset() protocol.NumberOfVersion //
	SaveTime() protocol.Time                         //
}
