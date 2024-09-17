/* For license and copyright information please see the LEGAL file in the code repository */

package org

type TimeType uint8

const (
	TimeType_Unset TimeType = iota

	TimeType_Start
	TimeType_End
	TimeType_ManualStart
	TimeType_ManualEnd
)
