/* For license and copyright information please see the LEGAL file in the code repository */

package faip

import (
	"libgo/iso"
	"libgo/protocol"
)

type BS_Register_Request interface {
	AccountID() [16]byte
	IBAN() iso.IBAN
}

type BS_Get_Request interface {
	AccountID() [16]byte
	VersionOffset() protocol.VersionOffset
}
type BS_Get_Response interface {
	FinancialAccountIBAN
	Numbers() uint64
}
