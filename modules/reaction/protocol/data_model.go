/* For license and copyright information please see the LEGAL file in the code repository */

package rp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel store user reaction to any content in the application such as laws, comments, products, ...
// It is graph data structure that UserID is PrimaryNode and ReactionTo is SecondaryNode of node sides.
// It is also time series data that store user reaction in time if any changes to reaction occurred.
type DataModel interface {
	UserID() up.UserUUID            //
	ReactionTo() [16]byte           // any domain.
	Type() rune                     // any unicode emoji character as old fashion rate(5 star) or like||dislike or ...
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// Status indicate Reaction record status
type Status uint8

// Reaction status
const (
	Status_Unset  Status = 0
	Status_Hidden Status = (1 << iota) // to indicate just peer can access the interest chains.
	Status_Blocked
)

// Query by day??
