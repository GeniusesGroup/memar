/* For license and copyright information please see the LEGAL file in the code repository */

package rp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel store user reaction to any content in the application such as laws, comments, products, ...
// It is graph data structure that UserID is PrimaryNode and ReactionTo is SecondaryNode of node sides.
// It is also time series data that store user reaction in time if any changes to reaction occurred.
type DataModel interface {
	UserID() up.UserUUID
	ReactionTo() [16]byte // any domain.
	Type() rune           // any unicode emoji character as old fashion rate(5 star) or like||dislike or ...
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// Query by day??
