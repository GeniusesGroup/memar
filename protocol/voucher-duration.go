/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherDuration indicate the domain record data fields.
type VoucherDuration interface {
	VoucherID() VoucherUUID         //
	Each() uint8                    // Each time use
	Epoch() VoucherDuration_Epoch   //
	Duration() protocol.Duration    // from Epoch()
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherDuration_StorageServices interface {
	Save(dm VoucherDuration) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID, Each uint8) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, Each uint8, vo protocol.VersionOffset) (dm VoucherDuration, nv protocol.NumberOfVersion, err protocol.Error)
}

type VoucherDuration_Epoch uint8

const (
	VoucherDuration_Epoch_Unset VoucherDuration_Epoch = iota
	VoucherDuration_Epoch_IssueDate
	VoucherDuration_Epoch_LastUse
)
