/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// FinancialTransactionReference indicate the domain record data fields.
// FinancialTransactionReference store the secondary index that complicated than regular indexes.
// Use version to save multi transactions for the same reference.
type FinancialTransactionReference interface {
	ReferenceID() [16]byte         // any domain base on FinancialTransaction_Type
	SenderAccountID() [16]byte     // financial-account domain
	SenderAccountOffset() uint64   //
	ReceiverAccountID() [16]byte   // financial-account domain. or AccountPartyID
	ReceiverAccountOffset() uint64 //
	Time() protocol.Time           // save time
}

type FinancialTransactionReference_StorageServices interface {
	Save(ftr FinancialTransactionReference) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(referenceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(referenceID [16]byte, vo protocol.VersionOffset) (ftr FinancialTransactionReference, nv protocol.NumberOfVersion, err protocol.Error)
}
