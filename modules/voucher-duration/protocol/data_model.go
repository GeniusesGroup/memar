/* For license and copyright information please see the LEGAL file in the code repository */

package vdp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID      //
	Each() uint8                    // Each time use
	Epoch() VoucherDuration_Epoch   //
	Duration() protocol.Duration    // from Epoch()
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type VoucherDuration_Epoch uint8

const (
	VoucherDuration_Epoch_Unset VoucherDuration_Epoch = iota
	VoucherDuration_Epoch_IssueDate
	VoucherDuration_Epoch_LastUse
)
