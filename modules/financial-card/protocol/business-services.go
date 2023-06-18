/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"libgo/iso"
	"libgo/protocol"
)

type BS_Register_Request interface {
	AccountID() [16]byte
	CardNumber() iso.Card
	ExpireDate() protocol.Time
	CVC() uint16
}

type BS_Get_Request interface {
	AccountID() [16]byte
	VersionOffset() protocol.VersionOffset
}
type BS_Get_Response interface {
	FinancialCard
	Numbers() uint64
}
