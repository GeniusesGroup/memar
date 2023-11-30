/* For license and copyright information please see the LEGAL file in the code repository */

package uoaip

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel cache all foreign fundamental user data
type DataModel interface {
	UserID() up.UserUUID
	OrgID() up.UserUUID
	Gender() string              // In ISO format
	PassportID() string          // If exist mean user have that country Nationality
	Surname() string             // FirstName
	MiddleName() string          //
	GivenName() string           // LastName
	Nickname() string            //
	TaxID() string               //
	Picture() string             // picture url
	Bio() string                 //
	Location() string            //
	PostalCode() string          //
	DateOfBirth() protocol.Time  //
	PlaceOfBirth() string        //
	VerifiedDate() protocol.Time // If !=0 user got famous blue badge(tick) like instagram, twitter,...

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
