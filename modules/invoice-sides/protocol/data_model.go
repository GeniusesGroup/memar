/* For license and copyright information please see the LEGAL file in the code repository */

package isp

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID      //
	UserID() up.UserUUID            //
	Type() Type                     //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Seller Type = iota
	Type_Customer
	Type_Agent
	Type_Franchise
)

type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
