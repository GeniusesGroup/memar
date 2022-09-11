/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/earth"
	"github.com/GeniusesGroup/libgo/time/utc"
)

type StaffMission interface {
	StaffID() [16]byte          // staff domain
	Day() utc.DayElapsed        //
	DayHours() earth.DayHours   //
	Type() StaffMission_Type    //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type StaffMission_Type uint8

const (
	StaffMission_Type_Unset StaffMission_Type = iota
	StaffMission_Type_Meeting
	StaffMission_Type_Negotiation
	StaffMission_Type_Deal
	StaffMission_Type_Study
	// StaffMission_Type_
)
