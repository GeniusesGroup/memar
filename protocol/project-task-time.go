/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProjectTaskTime indicate the domain record data fields.
type ProjectTaskTime interface {
	TaskID() [16]byte           // project-task domain
	Type() ProjectTaskTime_Type //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}

type ProjectTaskTime_Type uint8

const (
	ProjectTaskTime_Type_Unset ProjectTaskTime_Type = iota
	ProjectTaskTime_Type_ManualStart
	ProjectTaskTime_Type_ManualTemporaryEnd
	ProjectTaskTime_Type_ManualEnd
	ProjectTaskTime_Type_Start
	ProjectTaskTime_Type_TemporaryEnd
	ProjectTaskTime_Type_End
)
