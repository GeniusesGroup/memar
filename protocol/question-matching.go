/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionMatching indicate the domain record data fields.
type QuestionMatching interface {
	QuestionID() QuestionUUID       //
	Matches() []QuestionOptionUUID  //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}
