/* For license and copyright information please see the LEGAL file in the code repository */

package ftrp

import (
	"libgo/protocol"
	fap "org/modules/financial-account/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel store the secondary index that complicated than regular indexes.
// Use version to save multi transactions for the same reference.
type DataModel interface {
	ReferenceID() protocol.UUID // any domain base on FinancialTransaction_Type
	SenderAccountID() fap.FinancialAccountUUID
	SenderAccountOffset() uint64                 //
	ReceiverAccountID() fap.FinancialAccountUUID // financial-account domain. or AccountPartyID
	ReceiverAccountOffset() uint64               //
	SaveTime() protocol.Time                     //
}
