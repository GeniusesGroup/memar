/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

type Field_SeatID interface {
	SeatID() SeatID
}

// seat number
type SeatID uint64
