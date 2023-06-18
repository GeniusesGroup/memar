/* For license and copyright information please see the LEGAL file in the code repository */

package fai

import (
	"libgo/protocol"
)

type (
	BS_Register_Request interface {
		AccountID() [16]byte
		ID() string
	}
)

type (
	BS_Get_Request interface {
		AccountID() [16]byte
		VersionOffset() protocol.VersionOffset
	}
	BS_Get_Response interface {
		FinancialAccountID
		Numbers() uint64
	}
)
