/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// TODO::: need domain or any fields here to support for Numbers Authority (GOD mode)? e.g. [IANA](https://iana.org/)

type DataModel interface {
	UserID() up.UserUUID     //
	OrgID() org.OrgUUID      //
	ProviderID() org.OrgUUID //
	Number() string          // like PhoneNumber
	// Number() uint64          // without country code e.g. {(00)98-}912-345-6789
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID // Request RecordID to prove how this object created in the chain of other objects.
}

// Status indicate UserNumber record status
type Status qsp.Quiddity_Status

const (
	Status_Approved = Status(qsp.Quiddity_Status_FreeFlag << iota)
	// Status_Hidden		in this case user can't login by number
)

/*
	Errors
*/
