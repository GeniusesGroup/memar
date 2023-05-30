/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// Reaction store user reaction to any content in the application such as laws, comments, products, ...
// It is graph data structure that UserID is PrimaryNode and ReactionTo is SecondaryNode of node sides.
// It is also time series data that store user reaction in time if any changes to reaction occurred.
type Reaction interface {
	UserID() UserUUID               //
	ReactionTo() [16]byte           // any domain.
	Type() rune                     // any unicode emoji character as old fashion rate(5 star) or like||dislike or ...
	Status() Reaction_Status        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

// Reaction_Status indicate Reaction record status
type Reaction_Status uint8

// Reaction status
const (
	Reaction_Status_Unset  Reaction_Status = 0
	Reaction_Status_Hidden Reaction_Status = (1 << iota) // to indicate just peer can access the interest chains.
	Reaction_Status_Blocked
)

// Query by day??
