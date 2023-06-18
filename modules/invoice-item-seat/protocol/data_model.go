/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// It can also use to order buyers e.g. patient in doctor clinic.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID      //
	ProductID() pp.ProductUUID      //
	SeatID() uint64                 // seat number
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_Voided = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
