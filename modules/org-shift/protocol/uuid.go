/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"libgo/protocol"
)

type ShiftUUID = protocol.UUID

type Type uint8

const (
	Type_Unset Type = iota
	Type_Strict
	Type_Float
)
