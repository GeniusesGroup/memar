/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// FinancialTransactionReference indicate the domain record data fields.
// FinancialTransactionReference store the secondary index that complicated than regular indexes.
// Use version to save multi transactions for the same reference.
type FinancialTransactionReference interface {
	ReferenceID() protocol.UUID // any domain base on FinancialTransaction_Type
	SenderAccountID() FinancialAccountUUID
	SenderAccountOffset() uint64             //
	ReceiverAccountID() FinancialAccountUUID // financial-account domain. or AccountPartyID
	ReceiverAccountOffset() uint64           //
	Time() protocol.Time                     // save time
}

type FinancialTransactionReference_StorageServices interface {
	Save(dm FinancialTransactionReference) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(referenceID protocol.UUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(referenceID protocol.UUID, vo protocol.VersionOffset) (dm FinancialTransactionReference, nv protocol.NumberOfVersion, err protocol.Error)
}
