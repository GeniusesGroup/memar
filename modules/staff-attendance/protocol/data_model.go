/* For license and copyright information please see the LEGAL file in the code repository */

package sap

import (
	"libgo/protocol"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	StaffID() sp.StaffUUID          //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Enter
	Type_Exit
	Type_ManualEnter
	Type_ManualExit
	Type_Start
	Type_End
)
