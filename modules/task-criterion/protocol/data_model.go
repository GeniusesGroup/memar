/* For license and copyright information please see the LEGAL file in the code repository */

package tcp

import (
	"libgo/protocol"

	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// معیار سنجش

// Story points are units of measure for expressing an estimate of the overall effort required
// to fully implement a product backlog item or any other piece of work.
// Teams assign story points relative to work complexity, the amount of work, and risk or uncertainty.
// https://www.atlassian.com/agile/project-management/estimation

// DataModel indicate the domain record data fields.
// a basis for comparison; a reference point against which other things can be evaluated
// the ideal in terms of which something can be judged
type DataModel interface {
	TaskID() tp.TaskUUID            //
	Type() Type                     //
	Point() int64                   // can be any data e.g. percent, star, ...
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Progress
	Type_Probability_Win
	Type_Probability_Failure
	Type_StoryPoint // Agile/Scrum
	Type_Risk       // TODO::: risk rate is calculated data or ... ?
)
