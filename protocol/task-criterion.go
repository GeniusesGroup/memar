/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// معیار سنجش

// Story points are units of measure for expressing an estimate of the overall effort required
// to fully implement a product backlog item or any other piece of work.
// Teams assign story points relative to work complexity, the amount of work, and risk or uncertainty.
// https://www.atlassian.com/agile/project-management/estimation

// TaskCriterion indicate the domain record data fields.
// a basis for comparison; a reference point against which other things can be evaluated
// the ideal in terms of which something can be judged
type TaskCriterion interface {
	TaskID() TaskUUID               //
	Type() TaskCriterion_Type       //
	Point() int64                   // can be any data e.g. percent, star, ...
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
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
