/* For license and copyright information please see the LEGAL file in the code repository */

package cttp

import (
	"libgo/protocol"

	ctp "org/modules/contract-template/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Tag is any text with hashtag in the contract template text, can't use by old fashion way to assign by users.
type DataModel interface {
	ContractTemplateID() ctp.ContractTemplateUUID //
	Tag() string                                  //
	Status() Status                               //
	SaveTime() protocol.Time                      //
	RequestID() urp.UserRequestUUID               //
}

type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
