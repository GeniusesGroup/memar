/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskCriterion indicate the domain record data fields.
// a basis for comparison; a reference point against which other things can be evaluated
// the ideal in terms of which something can be judged
type TaskCriterion interface {
	TaskID() TaskUUID               //
	Type() TaskCriterion_Type       //
	Point() int64                   // can be any data e.g. percent, star, ...
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type TaskCriterion_Type uint8

const (
	TaskCriterion_Type_Unset TaskCriterion_Type = iota
	TaskCriterion_Type_Progress
	TaskCriterion_Type_Probability_Win
	TaskCriterion_Type_Probability_Failure
	TaskCriterion_Type_StoryPoint // Agile/Scrum
	TaskCriterion_Type_Risk       // TODO::: risk rate is calculated data or ... ?
)
