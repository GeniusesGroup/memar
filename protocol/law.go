/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// LawUUID
type LawUUID = protocol.UUID

// Law give users the ability to vote to others and it allows them to make propositions on certain issues
type Law interface {
	LawID() LawUUID                 // to track changes in a law
	OrgID() up.UserUUID             //
	UserID() up.UserUUID            // Law suggester
	Language() protocol.Language    // base language
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

// TODO:::
// 	- If someone were to give their vote to another user not because they think that they are more knowledgeable on a subject
// 	  but because they received some sort of benefit, the election would lose purity
// 	- Normal elections allow citizens to keep their political preferences private whereas
// 	  LiquidFeedback demonstrates transparency when it comes to this in order to make sure users are who they say they are.
// 	- Schulze mathematical method: https://en.wikipedia.org/wiki/Schulze_method
// 	-
