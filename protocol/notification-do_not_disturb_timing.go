/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/earth"
	"github.com/GeniusesGroup/libgo/time/utc"
)

type NotificationDoNotDisturbTimings interface {
	NotificationID() [16]byte   //
	Day() utc.DayElapsed        //
	DayHours() earth.DayHours   // what hours in a day notification not serve
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
